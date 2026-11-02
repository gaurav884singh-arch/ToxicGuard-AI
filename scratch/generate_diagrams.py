from PIL import Image, ImageDraw, ImageFont
import os

FONT_PATH = "C:\\Windows\\Fonts\\times.ttf"
FONT_BOLD_PATH = "C:\\Windows\\Fonts\\timesbd.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "C:\\Windows\\Fonts\\arial.ttf"
    FONT_BOLD_PATH = "C:\\Windows\\Fonts\\arialbd.ttf"

def draw_arrow(draw, start, end, color="#1e3a8a", width=2):
    draw.line([start, end], fill=color, width=width)
    x1, y1 = start
    x2, y2 = end
    # Arrowhead
    if x1 == x2: # vertical
        if y2 > y1: # down
            draw.polygon([(x2-5, y2-8), (x2+5, y2-8), (x2, y2)], fill=color)
        else: # up
            draw.polygon([(x2-5, y2+8), (x2+5, y2+8), (x2, y2)], fill=color)
    elif y1 == y2: # horizontal
        if x2 > x1: # right
            draw.polygon([(x2-8, y2-5), (x2-8, y2+5), (x2, y2)], fill=color)
        else: # left
            draw.polygon([(x2+8, y2-5), (x2+8, y2+5), (x2, y2)], fill=color)

def generate_fig3_1():
    img = Image.new("RGB", (900, 360), "#ffffff")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_BOLD_PATH, 14)
    font_sub = ImageFont.truetype(FONT_PATH, 12)

    boxes_top = [
        ("Requirement\ngathering & analysis", 40, 40, 200, 110),
        ("System design\n(Architecture & DB)", 260, 40, 420, 110),
        ("Frontend dev\n(React, Tailwind)", 480, 40, 640, 110),
        ("Backend dev\n(FastAPI, JWT)", 700, 40, 860, 110),
    ]

    boxes_bot = [
        ("Deployment &\nfinal review", 40, 220, 200, 290),
        ("Testing &\ndebugging", 260, 220, 420, 290),
        ("Database creation\n& linking (SQLite)", 480, 220, 640, 290),
        ("Model training &\nNLP pipeline", 700, 220, 860, 290),
    ]

    # Draw top boxes
    for text, x1, y1, x2, y2 in boxes_top:
        draw.rectangle([x1, y1, x2, y2], fill="#f0f7ff", outline="#1d4ed8", width=2)
        lines = text.split("\n")
        w1 = draw.textlength(lines[0], font=font)
        draw.text((x1 + (x2-x1-w1)/2, y1 + 14), lines[0], fill="#0f172a", font=font)
        w2 = draw.textlength(lines[1], font=font_sub)
        draw.text((x1 + (x2-x1-w2)/2, y1 + 36), lines[1], fill="#334155", font=font_sub)

    # Top arrows
    draw_arrow(draw, (200, 75), (260, 75))
    draw_arrow(draw, (420, 75), (480, 75))
    draw_arrow(draw, (640, 75), (700, 75))

    # Down arrow on right
    draw_arrow(draw, (780, 110), (780, 220))

    # Draw bottom boxes
    for text, x1, y1, x2, y2 in boxes_bot:
        draw.rectangle([x1, y1, x2, y2], fill="#f0f7ff", outline="#1d4ed8", width=2)
        lines = text.split("\n")
        w1 = draw.textlength(lines[0], font=font)
        draw.text((x1 + (x2-x1-w1)/2, y1 + 14), lines[0], fill="#0f172a", font=font)
        w2 = draw.textlength(lines[1], font=font_sub)
        draw.text((x1 + (x2-x1-w2)/2, y1 + 36), lines[1], fill="#334155", font=font_sub)

    # Bottom arrows (right to left)
    draw_arrow(draw, (700, 255), (640, 255))
    draw_arrow(draw, (480, 255), (420, 255))
    draw_arrow(draw, (260, 255), (200, 255))

    img.save(r"c:\Users\gaura\OneDrive\Desktop\Minor Project\docs\images\fig3_1_flowchart.png", dpi=(300, 300))
    print("Generated fig3_1_flowchart.png")

def generate_fig3_2():
    img = Image.new("RGB", (900, 480), "#ffffff")
    draw = ImageDraw.Draw(img)
    font_title = ImageFont.truetype(FONT_BOLD_PATH, 15)
    font_bold = ImageFont.truetype(FONT_BOLD_PATH, 13)
    font_norm = ImageFont.truetype(FONT_PATH, 12)

    # Frontend container
    draw.rectangle([30, 30, 260, 450], outline="#475569", width=2)
    draw.text((80, 40), "Frontend (View)", fill="#0f172a", font=font_title)

    frontend_sub = [
        "Landing & Login Pages",
        "Community Social Feed",
        "Live Toxicity Analyzer",
        "Admin Review Queue",
        "Analytics Dashboard"
    ]
    for i, title in enumerate(frontend_sub):
        y = 80 + i * 72
        draw.rectangle([45, y, 245, y + 54], fill="#f8fafc", outline="#64748b", width=1)
        w = draw.textlength(title, font=font_bold)
        draw.text((45 + (200-w)/2, y + 18), title, fill="#1e293b", font=font_bold)

    # Backend container
    draw.rectangle([340, 30, 580, 450], outline="#475569", width=2)
    draw.text((360, 40), "FastAPI Backend (Controller)", fill="#0f172a", font=font_title)

    backend_sub = [
        "Authentication & JWT Handling",
        "Inference & Preprocessing Gateway",
        "Three-Tier Moderation Policy",
        "Admin Queue & Override Handlers",
        "Telemetry Analytics Aggregation"
    ]
    for i, title in enumerate(backend_sub):
        y = 80 + i * 72
        draw.rectangle([355, y, 565, y + 54], fill="#f8fafc", outline="#64748b", width=1)
        w = draw.textlength(title, font=font_bold)
        draw.text((355 + (210-w)/2, y + 18), title, fill="#1e293b", font=font_bold)

    # External Models & DB
    # DL Box
    draw.rectangle([660, 80, 870, 230], fill="#fefce8", outline="#ca8a04", width=2)
    draw.text((680, 95), "Deep Learning Engine", fill="#854d0e", font=font_title)
    draw.text((675, 125), "- Slang Preprocessor (50+)", fill="#713f12", font=font_norm)
    draw.text((675, 148), "- Conv1D Feature Extractor", fill="#713f12", font=font_norm)
    draw.text((675, 171), "- Bidirectional LSTM Context", fill="#713f12", font=font_norm)
    draw.text((675, 194), "- 6x Independent Sigmoid Heads", fill="#713f12", font=font_norm)

    # DB Box
    draw.rectangle([660, 290, 870, 440], fill="#fef2f2", outline="#dc2626", width=2)
    draw.text((685, 305), "SQLite Database", fill="#991b1b", font=font_title)
    draw.text((680, 335), "(SQLAlchemy ORM)", fill="#b91c1c", font=font_bold)
    draw.text((675, 365), "- Users Table (Auth/RBAC)", fill="#7f1d1d", font=font_norm)
    draw.text((675, 388), "- Comments Table (Scores)", fill="#7f1d1d", font=font_norm)
    draw.text((675, 411), "- Moderation Logs Audit Trail", fill="#7f1d1d", font=font_norm)

    # Interconnecting arrows
    # Frontend <-> Backend
    draw_arrow(draw, (260, 160), (340, 160))
    draw.text((272, 140), "HTTP/REST", fill="#475569", font=font_norm)
    draw_arrow(draw, (340, 320), (260, 320))
    draw.text((275, 300), "JSON Data", fill="#475569", font=font_norm)

    # Backend <-> DL
    draw_arrow(draw, (580, 145), (660, 145))
    draw.text((595, 125), "Tokenized", fill="#ca8a04", font=font_norm)
    draw_arrow(draw, (660, 175), (580, 175))
    draw.text((592, 182), "6x Probs", fill="#ca8a04", font=font_norm)

    # Backend <-> DB
    draw_arrow(draw, (580, 365), (660, 365))
    draw.text((600, 345), "ORM Queries", fill="#dc2626", font=font_norm)
    draw_arrow(draw, (660, 395), (580, 395))
    draw.text((605, 402), "Records", fill="#dc2626", font=font_norm)

    img.save(r"c:\Users\gaura\OneDrive\Desktop\Minor Project\docs\images\fig3_2_architecture.png", dpi=(300, 300))
    print("Generated fig3_2_architecture.png")

generate_fig3_1()
generate_fig3_2()
