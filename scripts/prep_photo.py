import sys
import os
from PIL import Image, ImageEnhance
try:
    import cv2
    import numpy as np
    HAS_OPENCV = True
except ImportError:
    HAS_OPENCV = False

def prep_photo(input_path="source-photo.jpg", output_path="source-prepped.png"):
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        sys.exit(1)
        
    img = Image.open(input_path).convert("L")
    
    if HAS_OPENCV:
        # Convert PIL to numpy array
        img_np = np.array(img)
        
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(img_np)
        
        # Slight gamma adjustment / brightness boosting for highlights
        enhanced = np.clip(enhanced * 1.1 + 10, 0, 255).astype(np.uint8)
        
        img = Image.fromarray(enhanced)
    else:
        # Fallback using PIL ImageEnhance
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.8)
        
    img.save(output_path)
    print(f"Prepped photo saved to {output_path}")

if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "source-photo.jpg"
    prep_photo(input_file)
