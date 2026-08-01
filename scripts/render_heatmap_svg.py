import os
import sys
import json
from datetime import datetime

PALETTE = [
    "#161b22",  # 0: none
    "#0e4429",  # 1: low
    "#006d32",  # 2: medium-low
    "#26a641",  # 3: medium-high
    "#39d353",  # 4: high
    "#69f0a0",  # 5: neon top end
]

MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def render_heatmap_svg(json_path="data/contributions.json", output_path="contrib-heatmap.svg"):
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found. Run fetch_contributions.py first.")
        sys.exit(1)

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    username = data.get("username", "sthitadhi").lower()
    days = data.get("days", [])
    total_contribs = data.get("total_contributions", 0)
    current_streak = data.get("current_streak", 0)
    longest_streak = data.get("longest_streak", 0)

    width = 860
    height = 230
    
    box_size = 11
    box_gap = 4
    col_width = box_size + box_gap
    row_height = box_size + box_gap
    
    start_x = 45
    start_y = 65
    
    weeks = [[] for _ in range(53)]
    
    if days:
        first_date = datetime.strptime(days[0]["date"], "%Y-%m-%d")
        first_weekday = first_date.weekday() # 0 = Monday, 6 = Sunday
        # Adjust so Sunday = 0
        first_weekday = (first_weekday + 1) % 7
        
        day_idx = 0
        for w in range(53):
            for r in range(7):
                if w == 0 and r < first_weekday:
                    weeks[w].append(None)
                elif day_idx < len(days):
                    weeks[w].append(days[day_idx])
                    day_idx += 1
                else:
                    weeks[w].append(None)

    svg_lines = []
    svg_lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg_lines.append('<style>')
    svg_lines.append('  .bg { fill: #0d1117; rx: 8px; stroke: #30363d; stroke-width: 1px; }')
    svg_lines.append('  .title { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 14px; fill: #58a6ff; font-weight: bold; }')
    svg_lines.append('  .sub { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 12px; fill: #8b949e; }')
    svg_lines.append('  .label { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 10px; fill: #7d8590; }')
    svg_lines.append('  .stat-val { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 13px; fill: #39d353; font-weight: bold; }')
    svg_lines.append('  .stat-key { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 12px; fill: #8b949e; }')
    svg_lines.append('  @keyframes diagonalSlide {')
    svg_lines.append('    from { opacity: 0; transform: translate(-8px, -8px) scale(0.8); }')
    svg_lines.append('    to { opacity: 1; transform: translate(0, 0) scale(1); }')
    svg_lines.append('  }')
    svg_lines.append('  .box { opacity: 0; animation: diagonalSlide 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards; }')
    svg_lines.append('</style>')

    # Background
    svg_lines.append(f'<rect class="bg" width="{width}" height="{height}" />')

    # Header Title
    svg_lines.append(f'<text class="title" x="20" y="32">{username}@github ~ $ ./contributions.sh</text>')
    svg_lines.append(f'<text class="sub" x="{width - 240}" y="32">{total_contribs:,} contributions in past year</text>')

    # Month labels
    last_month = -1
    for w in range(53):
        for d in weeks[w]:
            if d:
                dt = datetime.strptime(d["date"], "%Y-%m-%d")
                if dt.month != last_month and w < 52:
                    last_month = dt.month
                    m_name = MONTH_NAMES[dt.month - 1]
                    mx = start_x + w * col_width
                    svg_lines.append(f'<text class="label" x="{mx}" y="{start_y - 10}">{m_name}</text>')
                break

    # Day of week labels (Mon, Wed, Fri)
    day_labels = [("", 0), ("Mon", 1), ("", 2), ("Wed", 3), ("", 4), ("Fri", 5), ("", 6)]
    for lbl, r in day_labels:
        if lbl:
            ly = start_y + r * row_height + 9
            svg_lines.append(f'<text class="label" x="15" y="{ly}">{lbl}</text>')

    # Calendar Grid Cells
    for w in range(53):
        for r in range(7):
            day = weeks[w][r]
            x = start_x + w * col_width
            y = start_y + r * row_height
            
            if day:
                level = day.get("level", 0)
                if level >= len(PALETTE):
                    level = len(PALETTE) - 1
                color = PALETTE[level]
                
                diag = w + r
                delay = round((diag / 60.0) * 1.4, 3)
                
                tooltip_text = f'{day["count"]} contributions on {day["date"]}'
                
                svg_lines.append(
                    f'<rect class="box" x="{x}" y="{y}" width="{box_size}" height="{box_size}" '
                    f'fill="{color}" rx="2" style="animation-delay: {delay}s;">'
                    f'<title>{tooltip_text}</title></rect>'
                )
            else:
                svg_lines.append(
                    f'<rect x="{x}" y="{y}" width="{box_size}" height="{box_size}" fill="#161b22" rx="2" opacity="0.3"/>'
                )

    # Footer: Stats & Legend
    footer_y = start_y + 7 * row_height + 25
    
    # Stats
    svg_lines.append(f'<text class="stat-key" x="20" y="{footer_y}">Current Streak: <tspan class="stat-val">{current_streak} days</tspan></text>')
    svg_lines.append(f'<text class="stat-key" x="200" y="{footer_y}">Longest Streak: <tspan class="stat-val">{longest_streak} days</tspan></text>')

    # Legend (Less -> More)
    legend_start_x = width - 160
    svg_lines.append(f'<text class="label" x="{legend_start_x - 32}" y="{footer_y - 2}">Less</text>')
    for i, col in enumerate(PALETTE):
        lx = legend_start_x + i * (box_size + 3)
        svg_lines.append(f'<rect x="{lx}" y="{footer_y - 11}" width="{box_size}" height="{box_size}" fill="{col}" rx="2"/>')
    svg_lines.append(f'<text class="label" x="{legend_start_x + len(PALETTE) * (box_size + 3) + 4}" y="{footer_y - 2}">More</text>')

    svg_lines.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))
    print(f"Heatmap SVG re-generated to {output_path}")

if __name__ == "__main__":
    render_heatmap_svg()
