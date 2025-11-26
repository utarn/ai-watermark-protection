#!/usr/bin/env python3
"""
Command Line Interface for AI Watermark Fighter

This module provides CLI commands for batch processing images with enlarge and restore operations.
Each process outputs files with the same name and appropriate suffix:
- enlarge operation: filename-enlarge.ext
- restore operation: filename-restore.ext
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional
from PIL import Image

from app import expand_image, crop_image


def get_output_path(input_path: Path, suffix: str) -> Path:
    """
    Generate output path with the given suffix.

    Args:
        input_path: Path to input file
        suffix: Suffix to add (e.g., '-enlarge', '-restore')

    Returns:
        Path with suffix added before the file extension
    """
    stem = input_path.stem
    suffix_path = input_path.parent / f"{stem}{suffix}{input_path.suffix}"
    return suffix_path


def save_image_with_suffix(image: Image.Image, input_path: Path, suffix: str, output_dir: Optional[Path] = None, output_format: str = None) -> Path:
    """
    Save PIL Image with specified suffix and format.

    Args:
        image: PIL Image to save
        input_path: Original input file path
        suffix: Suffix to add to filename
        output_dir: Optional output directory (defaults to same directory as input)
        output_format: Optional output format ('PNG', 'JPG', 'WEBP')

    Returns:
        Path to the saved file
    """
    if output_dir is None:
        output_dir = input_path.parent

    # Determine output format and file extension
    if output_format:
        output_format = output_format.upper()
        if output_format == 'JPG':
            extension = '.jpg'
        elif output_format == 'PNG':
            extension = '.png'
        elif output_format == 'WEBP':
            extension = '.webp'
        else:
            output_format = 'PNG'
            extension = '.png'
    else:
        # Use original format if no output format specified
        if input_path.suffix.lower() in ['.png']:
            output_format = 'PNG'
            extension = '.png'
        elif input_path.suffix.lower() in ['.jpg', '.jpeg']:
            output_format = 'JPEG'
            extension = '.jpg'
        else:
            output_format = 'PNG'
            extension = '.png'

    # Generate output path with correct extension
    stem = input_path.stem
    output_path = output_dir / f"{stem}{suffix}{extension}"

    # Save image in the specified format
    if output_format == 'PNG':
        image.save(output_path, 'PNG')
    elif output_format in ['JPEG', 'JPG']:
        # Convert to RGB for JPEG
        if image.mode in ['RGBA', 'LA']:
            # Create white background
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'RGBA':
                background.paste(image, mask=image.split()[-1])  # Use alpha channel as mask
            else:
                background.paste(image)
            background.save(output_path, 'JPEG', quality=95)
        else:
            image.save(output_path, 'JPEG', quality=95)
    elif output_format == 'WEBP':
        # Handle transparency for WebP
        if image.mode in ['RGBA', 'LA']:
            image.save(output_path, 'WEBP', quality=95, lossless=False)
        else:
            image.save(output_path, 'WEBP', quality=95, lossless=False)
    else:
        # Default to PNG for unsupported formats
        png_path = output_path.with_suffix('.png')
        image.save(png_path, 'PNG')
        output_path = png_path

    return output_path


def process_enlarge_images(input_paths: List[Path], output_dir: Optional[Path] = None, output_format: str = None) -> List[Path]:
    """
    Process multiple images with enlarge operation.

    Args:
        input_paths: List of input image paths
        output_dir: Optional output directory
        output_format: Optional output format ('PNG', 'JPG', 'WEBP')

    Returns:
        List of successful output paths
    """
    successful_outputs = []

    for input_path in input_paths:
        try:
            # Load image
            with Image.open(input_path) as img:
                # Process image
                enlarged_img = expand_image(img)

                # Save with suffix and format
                output_path = save_image_with_suffix(enlarged_img, input_path, '-enlarge', output_dir, output_format)
                successful_outputs.append(output_path)
                print(f"✓ Processed: {input_path} -> {output_path}")

        except Exception as e:
            print(f"✗ Error processing {input_path}: {e}", file=sys.stderr)
            continue

    return successful_outputs


def process_restore_images(input_paths: List[Path], output_dir: Optional[Path] = None, output_format: str = None) -> List[Path]:
    """
    Process multiple images with restore operation.

    Args:
        input_paths: List of input image paths
        output_dir: Optional output directory
        output_format: Optional output format ('PNG', 'JPG', 'WEBP')

    Returns:
        List of successful output paths
    """
    successful_outputs = []

    for input_path in input_paths:
        try:
            # Load image
            with Image.open(input_path) as img:
                # Process image
                restored_img = crop_image(img)

                # Save with suffix and format
                output_path = save_image_with_suffix(restored_img, input_path, '-restore', output_dir, output_format)
                successful_outputs.append(output_path)
                print(f"✓ Processed: {input_path} -> {output_path}")

        except Exception as e:
            print(f"✗ Error processing {input_path}: {e}", file=sys.stderr)
            continue

    return successful_outputs


def collect_image_paths(input_spec: str) -> List[Path]:
    """
    Collect image paths from input specification.
    Supports individual files, directories, and glob patterns.

    Args:
        input_spec: Input specification (file, directory, or glob pattern)

    Returns:
        List of image file paths
    """
    input_path = Path(input_spec)

    if input_path.is_file():
        # Single file
        return [input_path]
    elif input_path.is_dir():
        # Directory - find all images
        image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif', '.webp'}
        return [p for p in input_path.rglob('*') if p.suffix.lower() in image_extensions]
    else:
        # Try glob pattern
        try:
            import glob
            matches = glob.glob(input_spec)
            return [Path(m) for m in matches if Path(m).is_file()]
        except Exception:
            return []


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="AI Watermark Fighter CLI - Process images with enlarge and restore operations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Enlarge a single image
  python -m ai_watermark_fighter enlarge image.jpg

  # Enlarge multiple images to output directory
  python -m ai_watermark_fighter enlarge *.jpg --output-dir ./processed

  # Restore enlarged images
  python -m ai_watermark_fighter restore image-enlarge.jpg

  # Process all images in a directory
  python -m ai_watermark_fighter enlarge ./images/ --output-dir ./output
        """
    )

    parser.add_argument(
        'operation',
        choices=['enlarge', 'restore'],
        help='Operation to perform'
    )

    parser.add_argument(
        'input',
        nargs='+',
        help='Input files, directories, or glob patterns'
    )

    parser.add_argument(
        '--output-dir', '-o',
        type=Path,
        help='Output directory (defaults to same directory as input files)'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output'
    )

    parser.add_argument(
        '--format', '-f',
        choices=['PNG', 'JPG', 'WEBP'],
        help='Output format for processed images (default: original format)'
    )

    args = parser.parse_args()

    # Validate output directory
    if args.output_dir:
        args.output_dir.mkdir(parents=True, exist_ok=True)

    # Collect all input paths
    all_input_paths = []
    for spec in args.input:
        paths = collect_image_paths(spec)
        if paths:
            all_input_paths.extend(paths)
        else:
            print(f"Warning: No files found for '{spec}'", file=sys.stderr)

    if not all_input_paths:
        print("Error: No input files found", file=sys.stderr)
        sys.exit(1)

    if args.verbose:
        print(f"Found {len(all_input_paths)} images to process")
        if args.output_dir:
            print(f"Output directory: {args.output_dir}")

    # Process based on operation
    if args.operation == 'enlarge':
        successful_outputs = process_enlarge_images(all_input_paths, args.output_dir, args.format)
    else:  # restore
        successful_outputs = process_restore_images(all_input_paths, args.output_dir, args.format)

    # Summary
    print(f"\nProcessing complete!")
    print(f"Successfully processed: {len(successful_outputs)}/{len(all_input_paths)} files")

    if successful_outputs:
        print("Output files:")
        for output_path in successful_outputs:
            print(f"  {output_path}")

    # Exit with error code if some files failed
    if len(successful_outputs) < len(all_input_paths):
        sys.exit(1)


if __name__ == '__main__':
    main()