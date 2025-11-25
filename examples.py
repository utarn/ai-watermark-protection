#!/usr/bin/env python3
"""
Example usage of AI Watermark Fighter

This script demonstrates how to use the AI Watermark Fighter programmatically
for both single file and batch processing operations.
"""

import sys
from pathlib import Path
from PIL import Image

# Import the functions
from app import expand_image, crop_image
from cli import save_image_with_suffix, get_output_path


def example_single_file():
    """Example: Process a single image file"""
    print("=== Single File Processing Example ===")

    # Create a sample image if none exists
    sample_path = Path("sample_image.png")
    if not sample_path.exists():
        # Create a simple 200x200 blue square as sample
        sample_img = Image.new('RGB', (200, 200), (0, 100, 255))
        sample_img.save(sample_path)
        print(f"Created sample image: {sample_path}")

    try:
        # Enlarge the image
        with Image.open(sample_path) as img:
            enlarged = expand_image(img)
            enlarged_path = save_image_with_suffix(enlarged, sample_path, '-enlarge')
            print(f"Enlarged: {enlarged_path}")

        # Restore the enlarged image
        with Image.open(enlarged_path) as img:
            restored = crop_image(img)
            restored_path = save_image_with_suffix(restored, enlarged_path, '-restore')
            print(f"Restored: {restored_path}")

        print("✓ Single file processing completed successfully")

    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)


def example_batch_processing():
    """Example: Process multiple images"""
    print("\n=== Batch Processing Example ===")

    # Create some sample images
    sample_dir = Path("sample_images")
    sample_dir.mkdir(exist_ok=True)

    sample_files = []
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # Red, Green, Blue

    for i, color in enumerate(colors):
        sample_path = sample_dir / f"sample_{i+1}.png"
        if not sample_path.exists():
            sample_img = Image.new('RGB', (150, 150), color)
            sample_img.save(sample_path)
            print(f"Created sample image: {sample_path}")
        sample_files.append(sample_path)

    try:
        # Process all images with enlarge
        for input_path in sample_files:
            with Image.open(input_path) as img:
                enlarged = expand_image(img)
                enlarged_path = save_image_with_suffix(enlarged, input_path, '-enlarge')
                print(f"Enlarged: {input_path} -> {enlarged_path}")

        print("✓ Batch processing completed successfully")

    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)


def example_output_filename_generation():
    """Example: Show how output filenames are generated"""
    print("\n=== Output Filename Generation Example ===")

    test_files = [
        "image.jpg",
        "photo.png",
        "picture.jpeg",
        "diagram.webp",
        "screenshot.tif"
    ]

    for filename in test_files:
        path = Path(filename)
        enlarge_output = get_output_path(path, '-enlarge')
        restore_output = get_output_path(path, '-restore')

        print(f"Input:  {filename}")
        print(f"Enlarge: {enlarge_output}")
        print(f"Restore: {restore_output}")
        print()


if __name__ == '__main__':
    print("AI Watermark Fighter - Usage Examples")
    print("=" * 40)

    # Run examples
    example_single_file()
    example_batch_processing()
    example_output_filename_generation()

    print("\nExamples completed!")
    print("\nTo use the CLI:")
    print("  python -m ai_watermark_fighter enlarge image.jpg")
    print("  python -m ai_watermark_fighter restore image-enlarge.jpg")
    print("\nOr after installation:")
    print("  ai-watermark-fighter enlarge *.jpg --output-dir ./processed")