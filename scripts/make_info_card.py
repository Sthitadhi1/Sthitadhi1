import os
import sys

def generate_info_card(output_path="info-card.svg"):
    is_static = os.getenv("STATIC", "0") == "1"

    width = 490
    height = 560
    
    # Information data
    data = [
        {"key": "OS", "val": "GitHub Terminal v2.4 (x86_64)"},
        {"key": "Host", "val": "Cloud & AI Infrastructure"},
        {"key": "Kernel", "val": "Python 3.12 / Rust / Go / C++"},
        {"key": "Uptime", "val": "5+ years in Software Development"},
        {"key": "Shell", "val": "zsh / bash / powershell"},
        {"key": "Now", "val": "Building Intelligent Agents & Scalable Systems"},
        {"key": "Prev", "val": "Full Stack & ML Systems Engineer"},
        {"key": "Stack", "val": "Python, TypeScript, React, PyTorch, Docker"},
        {"key": "Highlights", "val": "Open Source Contributor • AI Systems • Web Architecture"},
        {"key": "Location", "val": "San Francisco, CA / Remote"},
        {"key": "Status", "val": "🟢 Open to Collaborations & New Projects"},
    ]

    svg_lines = []
    svg_lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg_lines.append('<style>')
    svg_lines.append('  .card-bg { fill: #0d1117; rx: 8px; stroke: #30363d; stroke-width: 1px; }')
    svg_lines.append('  .title-bar { fill: #161b22; rx: 8px 8px 0 0; }')
    svg_lines.append('  .title-text { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 13px; fill: #8b949e; font-weight: 600; }')
    svg_lines.append('  .dot-red { fill: #ff5f56; }')
    svg_lines.append('  .dot-yellow { fill: #ffbd2e; }')
    svg_lines.append('  .dot-green { fill: #27c93f; }')
    svg_lines.append('  .prompt { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 13px; fill: #58a6ff; font-weight: bold; }')
    svg_lines.append('  .key { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 12.5px; fill: #79c0ff; font-weight: 600; }')
    svg_lines.append('  .val { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 12.5px; fill: #c9d1d9; }')
    svg_lines.append('  .accent { fill: #d2a8ff; font-weight: 600; }')
    
    if not is_static:
        svg_lines.append('  @keyframes fadeInSlide {')
        svg_lines.append('    from { opacity: 0; transform: translateY(12px); }')
        svg_lines.append('    to { opacity: 1; transform: translateY(0); }')
        svg_lines.append('  }')
        svg_lines.append('  .anim-line { opacity: 0; animation: fadeInSlide 0.4s ease-out forwards; }')
    else:
        svg_lines.append('  .anim-line { opacity: 1; }')
        
    svg_lines.append('</style>')

    # Card background
    svg_lines.append(f'<rect class="card-bg" width="{width}" height="{height}" />')
    
    # Title bar
    svg_lines.append(f'<path d="M 0 0 h {width} a 8 8 0 0 1 8 8 v 28 h -{width+8} v -28 a 8 8 0 0 1 8 -8 z" fill="#161b22"/>')
    # Terminal Window Dots
    svg_lines.append('<circle class="dot-red" cx="20" cy="18" r="5.5" />')
    svg_lines.append('<circle class="dot-yellow" cx="36" cy="18" r="5.5" />')
    svg_lines.append('<circle class="dot-green" cx="52" cy="18" r="5.5" />')
    svg_lines.append(f'<text class="title-text" x="72" y="22">avi@github ~ whoami</text>')

    # Banner / Command Line
    start_y = 65
    line_spacing = 38

    # Command line
    delays = 0.1
    anim_style = f'style="animation-delay: {delays:.2f}s;"' if not is_static else ''
    svg_lines.append(f'<g class="anim-line" {anim_style}>')
    svg_lines.append(f'  <text class="prompt" x="24" y="{start_y}">avi@github ~ $ neofetch</text>')
    svg_lines.append('</g>')

    # Rows
    current_y = start_y + 35
    for i, item in enumerate(data):
        delays = 0.2 + (i * 0.12)
        anim_style = f'style="animation-delay: {delays:.2f}s;"' if not is_static else ''
        svg_lines.append(f'<g class="anim-line" {anim_style}>')
        svg_lines.append(f'  <text class="key" x="24" y="{current_y}">{item["key"]}:</text>')
        # Calculate key padding
        key_width = len(item["key"]) * 9 + 35
        svg_lines.append(f'  <text class="val" x="{key_width}" y="{current_y}">{item["val"]}</text>')
        svg_lines.append('</g>')
        current_y += line_spacing - 6

    # Bottom color palette bar (neofetch style)
    color_bar_y = current_y + 12
    colors = ["#161b22", "#f85149", "#7ee787", "#e3b341", "#79c0ff", "#d2a8ff", "#56d4dd", "#c9d1d9"]
    delays += 0.2
    anim_style = f'style="animation-delay: {delays:.2f}s;"' if not is_static else ''
    svg_lines.append(f'<g class="anim-line" {anim_style}>')
    x_pos = 24
    for col in colors:
        svg_lines.append(f'  <rect x="{x_pos}" y="{color_bar_y}" width="22" height="14" fill="{col}" rx="3"/>')
        x_pos += 26
    svg_lines.append('</g>')

    svg_lines.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))
    print(f"Info card SVG generated to {output_path}")

if __name__ == "__main__":
    generate_info_card("info-card.svg")
