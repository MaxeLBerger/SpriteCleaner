"""
Background Removal Script for PNG Images
This script removes backgrounds from PNG images using the rembg library.
It preserves the original subject and makes the background transparent.
"""

import os
import sys
from pathlib import Path
from rembg import remove, new_session
from PIL import Image
import argparse


def remove_background_from_file(input_path, output_path, model="u2net"):
    """
    Remove background from a single image file.
    
    Args:
        input_path (str): Path to input image
        output_path (str): Path to save output image
        model (str): Model to use for background removal (default: u2net)
    """
    try:
        print(f"Processing: {input_path}")
        
        # Open the image
        with open(input_path, 'rb') as input_file:
            input_data = input_file.read()
        
        # Remove background (without alpha matting to avoid compatibility issues)
        output_data = remove(input_data)
        
        # Save the output
        with open(output_path, 'wb') as output_file:
            output_file.write(output_data)
        
        print(f"✓ Saved: {output_path}")
        return True
        
    except Exception as e:
        print(f"✗ Error processing {input_path}: {str(e)}")
        return False


def remove_background_from_folder(input_folder, output_folder, model="u2net"):
    """
    Remove background from all PNG images in a folder.
    
    Args:
        input_folder (str): Path to input folder
        output_folder (str): Path to output folder
        model (str): Model to use for background removal
    """
    input_path = Path(input_folder)
    output_path = Path(output_folder)
    
    # Create output folder if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Get all PNG files
    png_files = list(input_path.glob('*.png'))
    
    if not png_files:
        print(f"No PNG files found in {input_folder}")
        return
    
    print(f"\nFound {len(png_files)} PNG file(s) to process")
    print(f"Model: {model}")
    print("-" * 50)
    
    # Create a session for better performance when processing multiple images
    session = new_session(model)
    
    success_count = 0
    fail_count = 0
    
    for png_file in png_files:
        output_file = output_path / f"{png_file.stem}_no_bg.png"
        
        try:
            with open(png_file, 'rb') as input_file:
                input_data = input_file.read()
            
            # Remove background using the session (without alpha matting to avoid compatibility issues)
            output_data = remove(input_data, session=session)
            
            with open(output_file, 'wb') as out_file:
                out_file.write(output_data)
            
            print(f"✓ {png_file.name} -> {output_file.name}")
            success_count += 1
            
        except Exception as e:
            print(f"✗ Error processing {png_file.name}: {str(e)}")
            fail_count += 1
    
    print("-" * 50)
    print(f"\nProcessing complete!")
    print(f"✓ Success: {success_count}")
    print(f"✗ Failed: {fail_count}")


def main():
    parser = argparse.ArgumentParser(
        description="Remove backgrounds from PNG images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process single file
  python remove_background.py -i input.png -o output.png
  
  # Process all PNGs in a folder
  python remove_background.py -i ./assets/dogs -o ./output
  
  # Use a different model
  python remove_background.py -i ./assets/dogs -o ./output -m u2netp

Available models:
  - u2net (default): General use, high quality
  - u2netp: Lightweight, faster
  - u2net_human_seg: Optimized for humans
  - isnet-general-use: New high quality model
  - birefnet-general: Latest, very high quality
  - birefnet-general-lite: Lighter version of birefnet
        """
    )
    
    parser.add_argument(
        '-i', '--input',
        required=True,
        help='Input file or folder path'
    )
    
    parser.add_argument(
        '-o', '--output',
        required=True,
        help='Output file or folder path'
    )
    
    parser.add_argument(
        '-m', '--model',
        default='u2net',
        choices=['u2net', 'u2netp', 'u2net_human_seg', 'isnet-general-use', 
                 'birefnet-general', 'birefnet-general-lite', 'silueta'],
        help='Model to use for background removal (default: u2net)'
    )
    

    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    
    # Check if input exists
    if not input_path.exists():
        print(f"Error: Input path '{args.input}' does not exist")
        sys.exit(1)
    
    # Process based on whether input is file or folder
    if input_path.is_file():
        if input_path.suffix.lower() != '.png':
            print("Error: Input file must be a PNG image")
            sys.exit(1)
        
        output_path = Path(args.output)
        if output_path.is_dir():
            output_path = output_path / f"{input_path.stem}_no_bg.png"
        
        remove_background_from_file(
            str(input_path),
            str(output_path),
            args.model
        )
    
    elif input_path.is_dir():
        remove_background_from_folder(
            str(input_path),
            args.output,
            args.model
        )
    
    else:
        print(f"Error: '{args.input}' is neither a file nor a directory")
        sys.exit(1)


if __name__ == "__main__":
    main()
