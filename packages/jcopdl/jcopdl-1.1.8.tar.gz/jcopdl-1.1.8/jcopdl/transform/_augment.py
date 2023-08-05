class Standardize:
    """Standardize image using Standard Scaling."""

    def __init__(self, normalize=True):
        self.normalize = normalize

    def __call__(self, x):
        bs, c = x.shape[:2]
        tmp = x.view(bs, c, -1)
        mean, std = tmp.mean(2, keepdims=True), tmp.std(2, keepdims=True)
        x = (x - mean) / (std + 1e-6)

        if self.normalize:
            x = (x + 5) / 10
            x = x.clamp_(0, 1)
        return x
