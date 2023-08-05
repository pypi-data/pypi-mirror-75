import torch
from torch.utils.data import DataLoader
from torchvision.datasets.coco import CocoDetection
import matplotlib.pyplot as plt

from jcopdl.utils.exception import AnnotationError


class CocoDetectionDataset(CocoDetection):
    def __init__(self, root, annFile, device, transforms=None, bbox_format="voc"):
        super().__init__(root, annFile)
        self.transforms = transforms
        self.bbox_format = bbox_format
        self.classes_to_idx = {item["name"]: item["id"] for item in self.coco.cats.values()}
        self.classes = list(self.classes_to_idx)
        self.device = device

    def __getitem__(self, index):
        image_id = self.ids[index]
        image = self._get_image(image_id)
        annots = self._get_annots(image_id)

        if self.transforms is not None:
            try:
                sample = self.transforms(image=image, bboxes=annots["boxes"], labels=annots["labels"])
                image = sample["image"]
                annots["boxes"] = sample["bboxes"]
                annots["labels"] = sample["labels"]
            except ValueError:
                raise AnnotationError(f"Bounding box out of bound. Please fix annotation on image_id {image_id}")

        if self.bbox_format == "voc":
            annots["boxes"] = [self._coco_to_voc(box) for box in annots["boxes"]]

        image = torch.FloatTensor(image).permute(2, 0, 1)
        annots["boxes"] = torch.FloatTensor(annots["boxes"]).to(self.device)
        annots["labels"] = torch.LongTensor(annots["labels"]).to(self.device)
        return image, annots

    def _get_image(self, image_id):
        path = self.coco.loadImgs(image_id)[0]['file_name']
        image = plt.imread(f"{self.root}/{path}")
        return image

    def _get_annots(self, image_id):
        annot_ids = self.coco.getAnnIds(imgIds=image_id)
        annots = self.coco.loadAnns(annot_ids)
        return {
            "id": annot_ids,
            "image_id": image_id,
            "labels": [ann["category_id"] for ann in annots],
            "segmentation": [ann["segmentation"] for ann in annots],
            "boxes": [ann["bbox"] for ann in annots],
            "ignore": [ann["ignore"] for ann in annots],
            "iscrowd": [ann["iscrowd"] for ann in annots],
            "area": [ann["area"] for ann in annots]
        }

    @staticmethod
    def _coco_to_voc(bbox):
        x1, y1, w, h = bbox
        return x1, y1, x1 + w, y1 + h


class CocoDetectionDataloader(DataLoader):
    def __init__(self, dataset, batch_size=1, shuffle=False, drop_last=False):
        super().__init__(dataset, batch_size, shuffle, collate_fn=self.collate, num_workers=0, drop_last=drop_last)
        self.device = dataset.device

    def collate(self, batch):
        images, annots = zip(*batch)
        images = torch.stack(list(images)).to(self.device)
        return images, list(annots)
