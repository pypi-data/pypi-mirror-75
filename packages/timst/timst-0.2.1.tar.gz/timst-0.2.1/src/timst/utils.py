# Utils

import torch
import logging
import numpy as np

from PIL import Image
from torchvision import transforms

log = logging.getLogger(__name__)


def load_image(path, max_size=400, shape=None):
    """Load images and pre-process

    Parameters
    ----------
        path : str
            Path to the images
        max_size : float
            Define the size of the images
        shape : float
            Shape of the images
    """
    image = Image.open(path).convert("RGB")
    if max(image.size) > max_size:
        size = max_size
    else:
        size = max(image.size)
    if shape is not None:
        size = shape
    in_transform = transforms.Compose(
        [
            transforms.Resize(size),
            transforms.ToTensor(),
            transforms.Normalize(
                (0.485, 0.456, 0.406), (0.229, 0.224, 0.225)
            ),
        ]
    )
    image = in_transform(image)[:3, :, :].unsqueeze(0)
    return image


def get_features(image, model, layers=None):
    """Get the feature of the `input`/`style` image.

    Parameters
    ----------
        image : jpg
            Input/Style image
        model : cnn
            Neural Network Model
        layers : tensor
            Layers defining the Model
        """
    if layers is None:
        layers = {
            "0": "conv1_1",
            "5": "conv2_1",
            "10": "conv3_1",
            "19": "conv4_1",
            "28": "conv5_1",
            "21": "conv4_2",
        }
    features = {}
    for name, layer in model._modules.items():
        image = layer(image)
        if name in layers:
            features[layers[name]] = image
    return features


def gram_matrix(tensor):
    """Extracting the features of the images by computing
    the correlations.

    Parameters
    ----------
        tensor : tensor
            Tensor containg the information on the images
    """
    batch_size, depth, height, width = tensor.shape
    tensor = tensor.view(depth, -1)
    tensor = torch.mm(tensor, tensor.t())
    return tensor


def imconvert(tensor):
    """Convert tensors back to images.

    Parameters
    ----------
        tensor : tensor
            Tensor containing the information on the
            styled image
    """
    tensor = tensor.cpu().clone().detach()
    tensor = tensor.numpy().squeeze()
    tensor = tensor.transpose(1, 2, 0)
    arraym = np.array((0.229, 0.224, 0.225))
    arrayn = np.array((0.485, 0.456, 0.406))
    tensor = tensor * arraym + arrayn
    tensor = tensor.clip(0, 1)
    return tensor
