"""
Image Comparison Tool
Compares before and after images side-by-side for 5 different assets.
Generates both an HTML viewer and a comparison image grid.
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import base64
from io import BytesIO


def create_comparison_grid(input_folder, output_folder, comparison_output):
    """
    Create a visual comparison grid showing before and after images.
    
    Args:
        input_folder (str): Path to input folder with original images
        output_folder (str): Path to output folder with processed images
        comparison_output (str): Path to save the comparison grid
    """
    input_path = Path(input_folder)
    output_path = Path(output_folder)
    
    # Get the 5 template images from input
    template_images = [
        'black_cocker_spaniel_1.png',
        'border_collie_1.png',
        'german_sheperd_1.png',
        'golden_retriever_1.png',
        'siberian_husky_1.png'
    ]
    
    # Settings
    img_width = 300
    img_height = 300
    padding = 20
    title_height = 60
    label_height = 40
    
    # Calculate total grid size
    grid_width = (img_width * 2 + padding * 3)
    grid_height = (img_height + label_height + padding) * 5 + title_height + padding
    
    # Create blank canvas
    canvas = Image.new('RGB', (grid_width, grid_height), 'white')
    draw = ImageDraw.Draw(canvas)
    
    # Try to load a font, fallback to default
    try:
        title_font = ImageFont.truetype('arial.ttf', 36)
        header_font = ImageFont.truetype('arial.ttf', 20)
        label_font = ImageFont.truetype('arial.ttf', 16)
    except:
        title_font = ImageFont.load_default()
        header_font = ImageFont.load_default()
        label_font = ImageFont.load_default()
    
    # Draw title
    title = 'Before & After Comparison'
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(((grid_width - title_width) // 2, 20), title, fill='black', font=title_font)
    
    # Draw column headers
    y_pos = title_height
    draw.text((padding + img_width // 2 - 30, y_pos + 10), 'BEFORE', fill='black', font=header_font)
    draw.text((padding * 2 + img_width + img_width // 2 - 20, y_pos + 10), 'AFTER', fill='black', font=header_font)
    
    y_pos += label_height
    
    # Process each image pair
    for idx, template_name in enumerate(template_images):
        input_file = input_path / template_name
        output_file = output_path / f'{Path(template_name).stem}_no_bg.png'
        
        if not input_file.exists():
            print(f'Warning: {template_name} not found in input folder')
            continue
        
        if not output_file.exists():
            print(f'Warning: {output_file.name} not found in output folder')
            continue
        
        # Load and resize images
        before_img = Image.open(input_file)
        after_img = Image.open(output_file)
        
        # Resize maintaining aspect ratio
        before_img.thumbnail((img_width, img_height), Image.Resampling.LANCZOS)
        after_img.thumbnail((img_width, img_height), Image.Resampling.LANCZOS)
        
        # Create background for the 'after' image with checkered pattern
        checker_size = 20
        checker_bg = Image.new('RGB', (img_width, img_height), 'white')
        checker_draw = ImageDraw.Draw(checker_bg)
        
        for i in range(0, img_width, checker_size):
            for j in range(0, img_height, checker_size):
                if (i // checker_size + j // checker_size) % 2 == 0:
                    checker_draw.rectangle([i, j, i + checker_size, j + checker_size], fill='#E0E0E0')
        
        # Center images
        before_x = padding + (img_width - before_img.width) // 2
        before_y = y_pos + padding + (img_height - before_img.height) // 2
        
        after_x = padding * 2 + img_width + (img_width - after_img.width) // 2
        after_y = y_pos + padding + (img_height - after_img.height) // 2
        
        # Paste images
        canvas.paste(before_img, (before_x, before_y))
        checker_bg.paste(after_img, ((img_width - after_img.width) // 2, (img_height - after_img.height) // 2), after_img)
        canvas.paste(checker_bg, (padding * 2 + img_width, y_pos + padding))
        
        # Draw borders
        draw.rectangle([padding, y_pos + padding, padding + img_width, y_pos + padding + img_height], outline='#CCCCCC', width=2)
        draw.rectangle([padding * 2 + img_width, y_pos + padding, padding * 2 + img_width * 2, y_pos + padding + img_height], outline='#CCCCCC', width=2)
        
        # Draw label
        label = Path(template_name).stem.replace('_', ' ').title()
        label_y = y_pos + padding + img_height + 10
        label_bbox = draw.textbbox((0, 0), label, font=label_font)
        label_width = label_bbox[2] - label_bbox[0]
        draw.text(((grid_width - label_width) // 2, label_y), label, fill='black', font=label_font)
        
        y_pos += img_height + label_height + padding
        
        print(f' Added comparison for {template_name}')
    
    # Save the comparison grid
    canvas.save(comparison_output, 'PNG')
    print(f'\n Comparison grid saved to: {comparison_output}')
    

def create_html_comparison(input_folder, output_folder, html_output):
    """
    Create an HTML file with interactive before/after comparison.
    
    Args:
        input_folder (str): Path to input folder with original images
        output_folder (str): Path to output folder with processed images
        html_output (str): Path to save the HTML file
    """
    input_path = Path(input_folder)
    output_path = Path(output_folder)
    
    # Get the 5 template images
    template_images = [
        'black_cocker_spaniel_1.png',
        'border_collie_1.png',
        'german_sheperd_1.png',
        'golden_retriever_1.png',
        'siberian_husky_1.png'
    ]
    
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Before & After Comparison</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px 20px;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        h1 {
            text-align: center;
            color: white;
            font-size: 3em;
            margin-bottom: 40px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .comparison-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(600px, 1fr));
            gap: 30px;
            margin-bottom: 40px;
        }
        
        .comparison-item {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            transition: transform 0.3s ease;
        }
        
        .comparison-item:hover {
            transform: translateY(-5px);
        }
        
        .comparison-title {
            text-align: center;
            font-size: 1.5em;
            margin-bottom: 20px;
            color: #333;
            text-transform: capitalize;
        }
        
        .image-pair {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }
        
        .image-container {
            position: relative;
            overflow: hidden;
            border-radius: 8px;
            border: 2px solid #e0e0e0;
        }
        
        .image-container img {
            width: 100%;
            height: 300px;
            object-fit: contain;
            display: block;
        }
        
        .before-container {
            background: #f5f5f5;
        }
        
        .after-container {
            background: 
                repeating-linear-gradient(
                    45deg,
                    #f0f0f0,
                    #f0f0f0 10px,
                    #e0e0e0 10px,
                    #e0e0e0 20px
                );
        }
        
        .label {
            position: absolute;
            top: 10px;
            left: 10px;
            background: rgba(0, 0, 0, 0.7);
            color: white;
            padding: 5px 12px;
            border-radius: 4px;
            font-size: 0.9em;
            font-weight: bold;
        }
        
        @media (max-width: 768px) {
            .comparison-grid {
                grid-template-columns: 1fr;
            }
            
            h1 {
                font-size: 2em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1> Before & After Comparison</h1>
        <div class="comparison-grid">
'''
    
    # Add each comparison item
    for template_name in template_images:
        input_file = input_path / template_name
        output_file = output_path / f'{Path(template_name).stem}_no_bg.png'
        
        if not input_file.exists() or not output_file.exists():
            continue
        
        # Convert images to base64
        def img_to_base64(img_path):
            with open(img_path, 'rb') as f:
                img_data = f.read()
            return base64.b64encode(img_data).decode('utf-8')
        
        before_b64 = img_to_base64(input_file)
        after_b64 = img_to_base64(output_file)
        
        label = Path(template_name).stem.replace('_', ' ').title()
        
        html_content += f'''
            <div class="comparison-item">
                <div class="comparison-title">{label}</div>
                <div class="image-pair">
                    <div class="image-container before-container">
                        <div class="label">BEFORE</div>
                        <img src="data:image/png;base64,{before_b64}" alt="Before">
                    </div>
                    <div class="image-container after-container">
                        <div class="label">AFTER</div>
                        <img src="data:image/png;base64,{after_b64}" alt="After">
                    </div>
                </div>
            </div>
'''
    
    html_content += '''
        </div>
    </div>
</body>
</html>
'''
    
    # Save HTML file
    with open(html_output, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f' HTML comparison saved to: {html_output}')


def main():
    """Main function to create comparisons."""
    print('=' * 60)
    print('IMAGE COMPARISON TOOL')
    print('=' * 60)
    
    # Define paths
    input_folder = 'input'
    output_folder = 'output'
    comparison_image = 'comparison_grid.png'
    comparison_html = 'comparison.html'
    
    print('\nGenerating comparison visualizations...\n')
    
    # Create comparison grid
    print('Creating comparison grid image...')
    create_comparison_grid(input_folder, output_folder, comparison_image)
    
    print('\nCreating HTML comparison viewer...')
    create_html_comparison(input_folder, output_folder, comparison_html)
    
    print('\n' + '=' * 60)
    print('COMPARISON COMPLETE!')
    print('=' * 60)
    print(f'\nGenerated files:')
    print(f'   {comparison_image} - Grid comparison image')
    print(f'   {comparison_html} - Interactive HTML viewer')
    print(f'\nTo view the HTML comparison, open: {comparison_html}')
    print()


if __name__ == '__main__':
    main()
