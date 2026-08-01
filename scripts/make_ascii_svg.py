import sys
import os
from PIL import Image

RAMP = " .`:-=+*cs#%@"  # Bright (sparse) -> Dark (dense)

def image_to_ascii_grid(image_path, width=95):
    img = Image.open(image_path).convert("L")
    w, h = img.size
    aspect_ratio = h / w
    # Monospace characters are roughly 1.9x taller than wide
    height = int(width * aspect_ratio * 0.52)
    img_resized = img.resize((width, height), Image.Resampling.LANCZOS)
    
    grid = []
    ramp_len = len(RAMP)
    for y in range(height):
        row = []
        for x in range(width):
            pixel = img_resized.getpixel((x, y))
            # 255 (brightest) -> index 0 (' ')
            # 0 (darkest) -> index ramp_len - 1 ('@')
            index = int((255 - pixel) / 255.0 * (ramp_len - 1))
            index = max(0, min(ramp_len - 1, index))
            row.append(RAMP[index])
        grid.append("".join(row))
    return grid

def generate_ascii_svg(grid, output_path="avi-ascii.svg"):
    num_rows = len(grid)
    num_cols = len(grid[0]) if num_rows > 0 else 0
    
    font_size = 9.5
    char_width = 5.8
    line_height = 11.2
    padding_x = 16
    padding_y = 20
    
    svg_width = int(num_cols * char_width + padding_x * 2)
    svg_height = int(num_rows * line_height + padding_y * 2 + 10)
    
    total_duration = 3.2  # seconds for full print
    row_dur = 0.12
    
    svg_lines = []
    svg_lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">')
    svg_lines.append('<style>')
    svg_lines.append('  .bg { fill: #0d1117; rx: 8px; }')
    svg_lines.append('  .ascii-text { font-family: ui-monospace, SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace; font-size: 9.5px; fill: #8b949e; white-space: pre; }')
    svg_lines.append('  .cursor { fill: #58a6ff; }')
    svg_lines.append('</style>')
    
    # Clip paths definitions for SMIL row wipes
    svg_lines.append('<defs>')
    for i in range(num_rows):
        start_time = round((i / max(1, num_rows - 1)) * (total_duration - row_dur), 2)
        svg_lines.append(f'  <clipPath id="row-clip-{i}">')
        svg_lines.append(f'    <rect x="0" y="0" width="0" height="{svg_height}">')
        svg_lines.append(f'      <animate attributeName="width" from="0" to="{svg_width}" begin="{start_time}s" dur="{row_dur}s" fill="freeze"/>')
        svg_lines.append('    </rect>')
        svg_lines.append('  </clipPath>')
    svg_lines.append('</defs>')
    
    # Background
    svg_lines.append(f'<rect class="bg" width="{svg_width}" height="{svg_height}" />')
    
    # Text group
    svg_lines.append('<g class="ascii-text">')
    for i, row in enumerate(grid):
        y_pos = padding_y + (i + 1) * line_height
        start_time = round((i / max(1, num_rows - 1)) * (total_duration - row_dur), 2)
        
        # Escape HTML entities
        escaped_row = row.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace(' ', '&#160;')
        
        svg_lines.append(f'  <g clip-path="url(#row-clip-{i})">')
        svg_lines.append(f'    <text x="{padding_x}" y="{y_pos}">{escaped_row}</text>')
        svg_lines.append('  </g>')
        
        # Optional block cursor riding the wipe edge
        svg_lines.append(f'  <rect class="cursor" x="{padding_x}" y="{y_pos - 8}" width="6" height="10" opacity="0">')
        svg_lines.append(f'    <animate attributeName="x" from="{padding_x}" to="{padding_x + svg_width}" begin="{start_time}s" dur="{row_dur}s" fill="freeze"/>')
        svg_lines.append(f'    <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.01;0.95;1" begin="{start_time}s" dur="{row_dur + 0.05}s" fill="freeze"/>')
        svg_lines.append('  </rect>')
        
    svg_lines.append('</g>')
    svg_lines.append('</svg>')
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))
    print(f"ASCII SVG written to {output_path}")

if __name__ == "__main__":
    input_img = "source-prepped.png" if os.path.exists("source-prepped.png") else "source-photo.jpg"
    grid = image_to_ascii_grid(input_img, width=90)
    generate_ascii_svg(grid, "avi-ascii.svg")
