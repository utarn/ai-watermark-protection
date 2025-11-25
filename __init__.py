"""
AI Watermark Fighter

A tool for protecting images from watermarks by adding and removing white canvas areas.
"""

__version__ = "1.0.0"
__author__ = "AI Watermark Fighter Team"

from .app import expand_image, crop_image
from .cli import main, process_enlarge_images, process_restore_images

__all__ = [
    "expand_image",
    "crop_image",
    "main",
    "process_enlarge_images",
    "process_restore_images"
]