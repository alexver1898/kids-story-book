import gradio as gr
import random
import io
from PIL import Image, ImageDraw, ImageFont
import os
import textwrap
import math

# ─── STORY THEMES ───
THEMES = {
    "Space Adventure": {
        "colors": [(10, 10, 50), (30, 30, 80), (60, 40, 120)],
        "accent": (255, 215, 0),
    },
    "Jungle Explorers": {
        "colors": [(20, 60, 20), (40, 100, 30), (60, 140, 50)],
        "accent": (255, 200, 50),
    },
    "Ocean Deep": {
        "colors": [(10, 30, 70), (20, 60, 110), (40, 100, 160)],
        "accent": (0, 255, 200),
    },
    "Dinosaur World": {
        "colors": [(50, 70, 30), (100, 120, 50), (160, 140, 60)],
        "accent": (255, 100, 50),
    },
    "Magic Forest": {
        "colors": [(40, 15, 60), (80, 30, 100), (140, 60, 180)],
        "accent": (255, 200, 255),
    },
}

# ─── STORIES ───
STORIES = {
    "Space Adventure": {
        "title": "The Little Star Who Wanted to Shine",
        "pages": [
            "Little Luna was a tiny star in the big, dark sky. But she felt too small to shine like the others.",
            '"I wish I could glow like the Great Sun," Luna sighed. A friendly comet named Comet swooshed by.',
            '"You don\'t need to be big to shine bright," said Comet. "Even the smallest stars make the night beautiful."',
            "That night, Luna tried her best. She twinkled and sparkled with all her might.",
            "Down on Earth, a little girl looked up and smiled. 'Look, Mom! That little star is the prettiest one!'",
            "Luna realized — you don't need to be the biggest. You just need to be YOU. And she shone brighter than ever.",
        ],
        "moral": "You are already enough. Shine your own light.",
        "char": "star",
    },
    "Jungle Explorers": {
        "title": "Milo the Brave Monkey",
        "pages": [
            "Milo was a little monkey who lived in the big jungle. Everyone else seemed braver than him.",
            "His friend Pippa the parrot could fly high. His cousin Rocco could swing fast. Milo just watched.",
            "One day, the jungle river rose high. A little bunny was stuck on a rock, too scared to cross.",
            "Milo was scared too. But he grabbed a vine and swung — THUMP — right onto the rock.",
            "He held out his paw. 'Grab my hand!' The bunny jumped, and they both swung to safety together.",
            "Back on land, everyone cheered. Milo learned: being brave isn't not being scared — it's helping anyway.",
        ],
        "moral": "Bravery is doing the right thing, even when you're scared.",
        "char": "monkey",
    },
    "Ocean Deep": {
        "title": "Finn the Curious Fish",
        "pages": [
            "Finn was a tiny fish with BIG questions. 'What's above the water?' he asked. No one knew.",
            "His friends said, 'Don't go up there — it's dangerous!' But Finn couldn't stop wondering.",
            "One day, he swam up and up, through the blue water toward the light.",
            "POP! He broke the surface. He saw the sun, the sky, and a huge ship sailing by.",
            "A friendly seagull landed nearby. 'First time?' she asked. 'Welcome to the world above!'",
            "Finn dove back down, his heart full of wonder. He told everyone: 'There's so much more out there!'",
        ],
        "moral": "Curiosity leads to amazing discoveries. Never stop wondering.",
        "char": "fish",
    },
    "Dinosaur World": {
        "title": "Daisy the Tiny Dino",
        "pages": [
            "Daisy was the smallest dinosaur in the valley. The big dinos stomped and roared over her head.",
            "When the herd played games, Daisy was always left out. 'You're too little,' they'd say.",
            "One day, a big rock rolled down and blocked the path to the watering hole. No one could move it.",
            "Daisy looked closer. She saw the rock was wedged against a small pebble. She kicked the pebble away.",
            "CRACK! The big rock shifted and the path was clear! Everyone stared in surprise.",
            '"Being small means you see things others miss," Daisy smiled. And from that day, she was their secret hero.',
        ],
        "moral": "Your size doesn't define your strength. Small can be mighty.",
        "char": "dino",
    },
    "Magic Forest": {
        "title": "The Glowbug Who Lost Her Light",
        "pages": [
            "Bella was a glowbug who lit up the magic forest every night. But one evening, her light went out.",
            "She tried shaking, wiggling, and even doing a little dance. Nothing. Her bottom just wouldn't glow.",
            '"Without my light, I\'m just a bug," she cried. A wise old owl hooted softly.',
            '"Your light isn\'t in your tail, little one. It\'s in your heart. Show kindness — that\'s real light."',
            "Bella helped a lost caterpillar find its way home. She shared her berries with a hungry squirrel.",
            "And then — FWOOM — her glow returned, brighter than ever. Because kindness lights up everything.",
        ],
        "moral": "Your kindness is the brightest light you have.",
        "char": "bug",
    },
}


def draw_page(story_key, page_idx, theme_key):
    theme = THEMES[theme_key]
    story = STORIES[story_key]
    text = story["pages"][page_idx]
    total = len(story["pages"])

    W, H = 800, 600
    img = Image.new("RGB", (W, H), theme["colors"][0])
    draw = ImageDraw.Draw(img)

    for i, color in enumerate(theme["colors"]):
        band_h = H // len(theme["colors"])
        draw.rectangle([0, i * band_h, W, (i + 1) * band_h], fill=color)

    for _ in range(random.randint(15, 30)):
        x, y = random.randint(0, W), random.randint(0, H // 2)
        r = random.randint(1, 3)
        draw.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, 180))

    draw_decorations(draw, W, H, theme_key)

    char_x, char_y = W // 2, H // 2 - 40
    draw_character(draw, char_x, char_y, story["char"], page_idx, W, H, theme)

    box_margin = 30
    box_top = H - 160
    draw.rounded_rectangle(
        [box_margin, box_top, W - box_margin, H - box_margin],
        radius=20, fill=(0, 0, 0, 160), outline=theme["accent"], width=2,
    )

    try:
        font_small = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", 16)
        font_text = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", 22)
    except:
        font_small = font_text = ImageFont.load_default()

    draw.text((W // 2, box_top + 10), f"{page_idx + 1} / {total}", fill=theme["accent"], anchor="mt", font=font_small)

    lines = textwrap.wrap(text, width=45)
    y_off = box_top + 36
    for line in lines:
        draw.text((W // 2, y_off), line, fill="white", anchor="mt", font=font_text)
        y_off += 30

    return img


def draw_decorations(draw, W, H, theme_key):
    if theme_key == "Space Adventure":
        draw.ellipse([W - 150, 30, W - 50, 130], fill=(200, 200, 100))
        draw.ellipse([W - 140, 40, W - 100, 80], fill=(180, 180, 80))
    elif theme_key == "Jungle Explorers":
        for x in [30, 70, 120, W - 100, W - 60]:
            draw.rectangle([x, H // 2 - 50, x + 10, H // 2 + 50], fill=(80, 40, 10))
            draw.ellipse([x - 30, H // 2 - 100, x + 40, H // 2 - 10], fill=(20, 100, 20))
    elif theme_key == "Ocean Deep":
        for _ in range(15):
            bx, by = random.randint(0, W), random.randint(0, H)
            br = random.randint(5, 15)
            draw.ellipse([bx - br, by - br, bx + br, by + br], outline=(100, 200, 255), width=1)
    elif theme_key == "Dinosaur World":
        draw.polygon([(W // 3, H // 2 + 50), (W // 2, H // 2 - 120), (2 * W // 3, H // 2 + 50)], fill=(100, 50, 20))
    elif theme_key == "Magic Forest":
        for _ in range(10):
            sx, sy = random.randint(0, W), random.randint(0, H // 2)
            sz = 6
            draw.polygon([
                (sx, sy - sz), (sx + 2, sy - 2), (sx + sz, sy),
                (sx + 2, sy + 2), (sx, sy + sz), (sx - 2, sy + 2),
                (sx - sz, sy), (sx - 2, sy - 2)
            ], fill=(255, 200, 255))


def draw_character(draw, x, y, char_type, page_idx, W, H, theme):
    y += page_idx * 5

    if char_type == "star":
        size = 35
        pts = []
        for i in range(10):
            a = i * 36 - 90
            r = size if i % 2 == 0 else size * 0.4
            pts.append((x + r * math.cos(math.radians(a)), y + r * math.sin(math.radians(a))))
        draw.polygon(pts, fill=(255, 255, 100), outline=(255, 200, 50), width=2)
        draw.ellipse([x - 10, y - 8, x - 4, y - 2], fill=(0, 0, 0))
        draw.ellipse([x + 4, y - 8, x + 10, y - 2], fill=(0, 0, 0))
        draw.arc([x - 8, y + 2, x + 8, y + 12], 0, 180, fill=(0, 0, 0), width=2)

    elif char_type == "monkey":
        draw.ellipse([x - 25, y - 30, x + 25, y + 10], fill=(140, 80, 40))
        draw.ellipse([x - 35, y + 5, x + 35, y + 50], fill=(120, 60, 30))
        draw.ellipse([x - 35, y - 25, x - 20, y - 10], fill=(180, 100, 50))
        draw.ellipse([x + 20, y - 25, x + 35, y - 10], fill=(180, 100, 50))
        draw.ellipse([x - 18, y - 20, x + 18, y + 5], fill=(200, 150, 100))
        draw.ellipse([x - 10, y - 15, x - 4, y - 8], fill=(0, 0, 0))
        draw.ellipse([x + 4, y - 15, x + 10, y - 8], fill=(0, 0, 0))
        draw.arc([x - 10, y - 5, x + 10, y + 5], 0, 180, fill=(0, 0, 0), width=2)
        draw.arc([x + 20, y + 20, x + 60, y + 60], 0, 180, fill=(120, 60, 30), width=4)

    elif char_type == "fish":
        draw.ellipse([x - 35, y - 20, x + 35, y + 20], fill=(50, 150, 200))
        draw.polygon([(x + 35, y - 15), (x + 60, y), (x + 35, y + 15)], fill=(50, 150, 200))
        draw.ellipse([x + 10, y - 8, x + 20, y + 2], fill="white")
        draw.ellipse([x + 13, y - 5, x + 18, y], fill=(0, 0, 0))
        draw.polygon([(x - 5, y - 20), (x + 5, y - 35), (x + 15, y - 20)], fill=(40, 120, 180))
        draw.arc([x + 5, y, x + 20, y + 8], 0, 180, fill=(0, 0, 0), width=2)

    elif char_type == "dino":
        draw.ellipse([x - 30, y, x + 30, y + 40], fill=(80, 160, 80))
        draw.ellipse([x - 40, y - 25, x - 5, y + 10], fill=(80, 160, 80))
        for sx in range(x - 20, x + 20, 10):
            draw.polygon([(sx, y + 5), (sx + 5, y - 15), (sx + 10, y + 5)], fill=(60, 120, 60))
        draw.ellipse([x - 30, y - 18, x - 22, y - 10], fill="white")
        draw.ellipse([x - 28, y - 16, x - 24, y - 12], fill=(0, 0, 0))
        draw.arc([x - 35, y - 8, x - 15, y + 5], 0, 180, fill=(0, 0, 0), width=2)
        draw.arc([x + 20, y + 5, x + 55, y + 30], 0, 160, fill=(80, 160, 80), width=8)

    elif char_type == "bug":
        draw.ellipse([x - 15, y - 20, x + 15, y + 5], fill=(80, 60, 100))
        draw.ellipse([x - 25, y - 30, x - 5, y - 10], fill=(180, 150, 200))
        draw.ellipse([x + 5, y - 30, x + 25, y - 10], fill=(180, 150, 200))
        draw.ellipse([x - 12, y + 2, x + 12, y + 20], fill=(255, 255, 150))
        draw.ellipse([x - 8, y - 16, x - 3, y - 10], fill=(0, 0, 0))
        draw.ellipse([x + 3, y - 16, x + 8, y - 10], fill=(0, 0, 0))
        draw.line([(x - 5, y - 20), (x - 10, y - 30)], fill=(80, 60, 100), width=2)
        draw.line([(x + 5, y - 20), (x + 10, y - 30)], fill=(80, 60, 100), width=2)

    draw.line([(0, y + 50), (W, y + 50)], fill=theme["accent"], width=2)


def generate_book(theme_key, child_name):
    story = STORIES[theme_key]
    pages = list(story["pages"])

    if child_name and child_name.strip():
        pages[0] = pages[0].replace("Luna", child_name).replace("Milo", child_name).replace("Finn", child_name).replace("Daisy", child_name).replace("Bella", child_name)

    images = []
    for i in range(len(pages)):
        img = draw_page(theme_key, i, theme_key)
        images.append(img)

    cover = images[0].copy()
    draw = ImageDraw.Draw(cover)
    draw.rectangle([(50, 300), (750, 500)], fill=(0, 0, 0, 180))

    try:
        ft = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", 36)
        fm = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", 20)
    except:
        ft = fm = ImageFont.load_default()

    suffix = f" for {child_name}" if child_name and child_name.strip() else ""
    draw.text((400, 340), story["title"] + suffix, fill="white", anchor="mt", font=ft)
    draw.text((400, 400), f"\u2728 {story['moral']} \u2728", fill=THEMES[theme_key]["accent"], anchor="mt", font=fm)

    images[0] = cover
    return images, story["title"], story["moral"]


# ─── GRADIO UI ───
css = """
.gradio-container { max-width: 950px; margin: auto; }
h1 { text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.5em; }
footer { text-align: center; color: #888; }
"""

with gr.Blocks(css=css, theme=gr.themes.Soft()) as demo:
    gr.Markdown("# \U0001F4DA Free Kids Story Book Generator")
    gr.Markdown("Pick a theme, add your child's name, and get a beautiful illustrated storybook with original art!")

    with gr.Row():
        with gr.Column(scale=1):
            theme_dropdown = gr.Dropdown(
                choices=list(STORIES.keys()),
                value="Space Adventure",
                label="\U0001F4D6 Choose a Story Theme",
            )
            child_name = gr.Textbox(
                label="\U0001F476 Your Child's Name (optional)",
                placeholder="e.g. Sofia",
                value="",
            )
            generate_btn = gr.Button("\u2728 Generate My Story Book", variant="primary", size="lg")

            with gr.Group():
                gr.Markdown("### \U0001F4D6 About this story")
                story_title = gr.Textbox(label="Title", interactive=False)
                story_moral = gr.Textbox(label="Moral", interactive=False)

        with gr.Column(scale=2):
            gallery = gr.Gallery(
                label="Your Story Book Pages",
                columns=2,
                rows=3,
                height="auto",
                object_fit="contain",
            )

    gr.Markdown("---")
    gr.Markdown(
        "Made with \u2764\ufe0f \u2014 Free for everyone. Runs entirely on Hugging Face Spaces. "
        "Each story has original illustrations and a positive moral lesson."
    )

    def on_generate(theme, name):
        images, title, moral = generate_book(theme, name)
        return images, title, moral

    generate_btn.click(
        fn=on_generate,
        inputs=[theme_dropdown, child_name],
        outputs=[gallery, story_title, story_moral],
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    demo.launch(server_port=port, server_name="0.0.0.0")
