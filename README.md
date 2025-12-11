# SpriteCleaner - Background Removal Tool

Python script that removes backgrounds from PNG images using AI (rembg library), making them transparent.

![Before & After Comparison](comparison/comparison_grid.png)

## Installation

```bash
pip install -r requirements.txt
```

**Dependencies:**
- `rembg[cpu]>=2.0.69` - AI background removal library
- `Pillow>=10.0.0` - Image processing

## Usage

### Process a Single File
```bash
python remove_background.py -i input.png -o output.png
```

### Process All PNGs in a Folder
```bash
python remove_background.py -i ./input -o ./output
```
Output files are saved with `_no_bg` suffix (e.g., `dog_no_bg.png`)

### Use Different AI Models
```bash
python remove_background.py -i input.png -o output.png -m u2netp
```

## Available Models

- `u2net` (default) - General use, high quality
- `u2netp` - Lightweight, faster processing
- `u2net_human_seg` - Optimized for humans
- `isnet-general-use` - High quality alternative
- `birefnet-general` - Very high quality
- `birefnet-general-lite` - Lighter version of birefnet
- `silueta` - Additional option

**Note:** First run downloads the selected model (~176MB for u2net) and caches it locally.

## Command Options

```
-i, --input     Input PNG file or folder path (required)
-o, --output    Output file or folder path (required)
-m, --model     AI model to use (default: u2net)
-h, --help      Show help and examples
```

## Comparison Tool

Generate visual comparisons of the 5 included template images:

```bash
cd comparison
python compare_images.py
```

**Generates:**
- `comparison_grid.png` - Visual grid showing before/after for all 5 images
- `comparison.html` - Interactive HTML viewer with side-by-side comparisons

**Template images included:**
- Black Cocker Spaniel
- Border Collie
- German Shepherd
- Golden Retriever
- Siberian Husky

## Requirements

- Python 3.7+
- Windows/Linux/Mac
