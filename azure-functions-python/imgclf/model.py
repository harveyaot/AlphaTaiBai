import torch, torchvision
from torch import nn

img_hidden_sz = 512 
num_image_embeds = 5

#?? 8907
n_classes = 8790
img_embed_pool_type = 'avg'

class ImageEncoder18(nn.Module):
    def __init__(self):
        super(ImageEncoder18, self).__init__()
        model = torchvision.models.resnet18(pretrained=True)
        modules = list(model.children())[:-2]
        self.model = nn.Sequential(*modules)

        pool_func = (
            nn.AdaptiveAvgPool2d
            if img_embed_pool_type == "avg"
            else nn.AdaptiveMaxPool2d
        )

        if num_image_embeds in [1, 2, 3, 5, 7]:
            self.pool = pool_func((num_image_embeds, 1))
        elif num_image_embeds == 4:
            self.pool = pool_func((2, 2))
        elif num_image_embeds == 6:
            self.pool = pool_func((3, 2))
        elif num_image_embeds == 8:
            self.pool = pool_func((4, 2))
        elif num_image_embeds == 9:
            self.pool = pool_func((3, 3))

    def forward(self, x):
        # Bx3x224x224 -> Bx512x7x7 -> Bx512xN -> BxNx512
        out = self.pool(self.model(x))
        out = torch.flatten(out, start_dim=2)
        out = out.transpose(1, 2).contiguous()
        return out  # BxNx2048


class ImageClf18(nn.Module):
    def __init__(self):
        super(ImageClf18, self).__init__()
        self.img_encoder = ImageEncoder18()
        self.clf = nn.Linear(img_hidden_sz * num_image_embeds, n_classes)

    def forward(self, x):
        x = self.img_encoder(x)
        x = torch.flatten(x, start_dim=1)
        out = self.clf(x)
        return out