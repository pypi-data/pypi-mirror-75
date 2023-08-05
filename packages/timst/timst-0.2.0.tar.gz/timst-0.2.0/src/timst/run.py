# This file should contain the main codes that controls the whole
# behaviour of the package.

import torch
import logging
import argparse
import matplotlib.pyplot as plt

from tqdm import trange
from torchvision import models
from timst.utils import imconvert
from timst.utils import load_image
from timst.utils import gram_matrix
from timst.utils import get_features

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
log = logging.getLogger(__name__)


def positive_int(value):
    """Checks if the given integer is positive.
    Parameters
    ----------
        value: int
            Input integer
    """
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(
            f"Negative values are not allowed: {ivalue}"
        )
    return ivalue


def args_parser():
    """Parse input arguments

    Parameters
    ==========
        image: jpg
            Input image to be style
        style: jpg
            Style to be applied to the input image
        niter: int
            Total number of iterations
    """
    parser = argparse.ArgumentParser(description="Image style transfer.")
    parser.add_argument("-i", "--image", help="Input image", required=True)
    parser.add_argument("-s", "--style", help="Style image", required=True)
    parser.add_argument("-n", "--niter", type=positive_int, help="Iteration")
    args = parser.parse_args()
    return args


def main():
    """Main function that controls the training"""
    args = args_parser()

    # Import Vgg pre-trained model
    vgg = models.vgg19(pretrained=True).features
    # Set grad to False
    for param in vgg.parameters():
        param.requires_grad_(False)
    # Check if GPU is available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    log.info("Checking GPU with CUDA.")
    log.info(f"Cuda Availability: {torch.cuda.is_available()}")
    vgg.to(device)

    # Mode to GPU if available
    content = load_image(args.image).to(device)
    style = load_image(args.style).to(device)

    style_features = get_features(style, vgg)
    content_features = get_features(content, vgg)
    style_grams = {
        layer: gram_matrix(style_features[layer]) for layer in style_features
    }
    # Start with content image for fast convergence
    # One can generate random image
    target = content.clone().requires_grad_(True).to(device)

    style_weights = {
        "conv1_1": 1.0,
        "conv2_1": 0.8,
        "conv3_1": 0.5,
        "conv4_1": 0.3,
        "conv5_1": 0.1,
    }
    content_weight = 1  # alpha
    style_weight = 5e6  # beta

    # Proceed to training
    optimizer = torch.optim.Adam([target], lr=0.003)

    # Total number of iterations
    if args.niter is None:
        steps = 2400
    else:
        steps = args.niter

    # Training
    with trange(steps) as iter_range:
        for i in iter_range:
            iter_range.set_description("Training")
            target_features = get_features(target, vgg)
            content_loss = torch.mean(
                (content_features["conv4_2"] - target_features["conv4_2"])
                ** 2
            )
            style_loss = 0
            for layer in style_weights:
                target_feature = target_features[layer]
                _, d, h, w = target_feature.shape
                target_gram = gram_matrix(target_feature)
                style_gram = style_grams[layer]
                layer_style_loss = style_weights[layer] * torch.mean(
                    (target_gram - style_gram) ** 2
                )
                style_loss += layer_style_loss / (d * h * w)
            total_loss = (
                style_weight * style_loss + content_weight * content_loss
            )
            optimizer.zero_grad()
            total_loss.backward()
            optimizer.step()
            iter_range.set_postfix(Loss=total_loss.item())
            plt.imsave("styled_image.jpg", imconvert(target))
