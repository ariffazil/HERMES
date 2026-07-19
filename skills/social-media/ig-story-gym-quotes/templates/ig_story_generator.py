#!/usr/bin/env python3
"""
IG Story Generator v2 — Gym Motivational Quotes
Real gym photo background + dark overlay + clean elegant typography.
Simple. No chaos. Professional.
"""

import os
import random
import subprocess
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter

QUOTES = [
    ("The iron never lies to you. Two hundred pounds is always two hundred pounds.", "Henry Rollins", "Writer & Lifter"),
    ("Strength does not come from physical capacity. It comes from an indomitable will.", "Mahatma Gandhi", "Leader of India"),
    ("The last three or four reps is what makes the muscle grow.", "Arnold Schwarzenegger", "7x Mr. Olympia"),
    ("Discipline is the bridge between goals and accomplishment.", "Jim Rohn", "Philosopher"),
    ("The pain you feel today will be the strength you feel tomorrow.", "Arnold Schwarzenegger", "7x Mr. Olympia"),
    ("Hard work beats talent when talent doesn't work hard.", "Tim Notke", "Coach"),
    ("Success is usually the culmination of controlling failure.", "Sylvester Stallone", "Rocky Balboa"),
    ("If you want something you've never had, you must be willing to do something you've never done.", "Thomas Jefferson", "3rd US President"),
    ("The mind is the limit.", "Arnold Schwarzenegger", "7x Mr. Olympia"),
    ("A champion is someone who gets up when he can't.", "Jack Dempsey", "Boxing Legend"),
    ("Your body can stand almost anything. It's your mind that you have to convince.", "Andrew Murphy", "Ultra Runner"),
    ("Great spirits have always encountered violent opposition from mediocre minds.", "Albert Einstein", "Physicist"),
    ("He who has a why to live can bear almost any how.", "Friedrich Nietzsche", "Philosopher"),
    ("What stands in the way becomes the way.", "Marcus Aurelius", "Roman Emperor"),
    ("We are what we repeatedly do. Excellence is not an act, but a habit.", "Aristotle", "Philosopher"),
    ("It is not the mountain we conquer, but ourselves.", "Sir Edmund Hillary", "Mount Everest"),
    ("Do not pray for an easy life; pray for the strength to endure a difficult one.", "Bruce Lee", "Martial Artist"),
    ("I hated every minute of training, but I said, 'Don't quit. Suffer now and live the rest of your life as a champion.'", "Muhammad Ali", "The Greatest"),
    ("The successful warrior is the average man, with laser-like focus.", "Bruce Lee", "Martial Artist"),
    ("You have power over your mind, not outside events.", "Marcus Aurelius", "Roman Emperor"),
    ("No citizen has a right to be an amateur in the matter of physical training.", "Socrates", "Philosopher"),
    ("The more you sweat in training, the less you bleed in combat.", "Richard Marcinko", "Navy SEAL"),
    ("Fall seven times, stand up eight.", "Japanese Proverb", "Bushido"),
    ("The body achieves what the mind believes.", "Napoleon Hill", "Author"),
    ("The resistance you fight in the gym builds the character you need in life.", "Arnold Schwarzenegger", "7x Mr. Olympia"),
    ("Motivation is what gets you started. Habit is what keeps you going.", "Jim Rohn", "Philosopher"),
    ("The clock is ticking. Are you becoming the person you want to be?", "Greg Plitt", "Fitness Icon"),
    ("Suffer the pain of discipline or suffer the pain of regret.", "Jim Rohn", "Philosopher"),
    ("Everybody wants to be a bodybuilder, but nobody wants to lift no heavy-ass weights.", "Ronnie Coleman", "8x Mr. Olympia"),
    ("There are no shortcuts. Everything is reps, reps, reps.", "Arnold Schwarzenegger", "7x Mr. Olympia"),
]

MUSIC_SUGGESTIONS = [
    ("Hype", ["Eye of the Tiger — Survivor", "Lose Yourself — Eminem", "Till I Collapse — Eminem", "Remember the Name — Fort Minor"]),
    ("Grind", ["HUMBLE. — Kendrick Lamar", "Power — Kanye West", "Stronger — Kanye West", "Can't Hold Us — Macklemore"]),
    ("Mindset", ["Started From the Bottom — Drake", "All I Do Is Win — DJ Khaled", "Champion — Kanye West", "Unstoppable — Sia"]),
    ("Beast Mode", ["X Gon' Give It to Ya — DMX", "Jumpman — Drake & Future", "Blinding Lights — The Weeknd", "Thunder — Imagine Dragons"]),
]

BG_IMAGES = ['/tmp/gym_bg_1.jpg', '/tmp/gym_bg_2.jpg', '/tmp/gym_bg_3.jpg', '/tmp/gym_bg_4.jpg']

BG_IDS = [
    'photo-1534438327276-14e5300c3a48',
    'photo-1517963879433-6ad2b056d712',
    'photo-1574680096145-d05b474e2155',
    'photo-1558611848-73f7eb4001a1',
]


def download_bg_if_missing():
    """Download gym backgrounds from Unsplash if missing."""
    for i, photo_id in enumerate(BG_IDS, 1):
        path = f'/tmp/gym_bg_{i}.jpg'
        if not os.path.exists(path):
            url = f'https://images.unsplash.com/{photo_id}?w=1080&h=1920&fit=crop&crop=center'
            subprocess.run(['curl', '-sL', '-o', path, url], check=True)
            print(f"Downloaded: {path} ({os.path.getsize(path)} bytes)")


def create_gym_quote_image(quote, author, era, output_path):
    """Create elegant IG Story: gym photo bg + dark overlay + clean quote."""
    W, H = 1080, 1920

    available = [p for p in BG_IMAGES if os.path.exists(p)]
    bg_path = random.choice(available)
    bg = Image.open(bg_path).convert('RGB')
    bg = bg.resize((W, H), Image.LANCZOS)
    bg = bg.filter(ImageFilter.GaussianBlur(radius=3))

    # Dark gradient overlay (center-heavy for text readability)
    overlay = Image.new('RGB', (W, H), (0, 0, 0))
    mask = Image.new('L', (W, H))
    mask_draw = ImageDraw.Draw(mask)
    for y in range(H):
        dist_from_center = abs(y - H * 0.45) / H
        opacity = int(180 - 80 * dist_from_center)
        opacity = max(100, min(200, opacity))
        mask_draw.line([(0, y), (W, y)], fill=opacity)
    bg = Image.composite(overlay, bg, mask)

    draw = ImageDraw.Draw(bg)

    try:
        font_quote = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
        font_author = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
        font_era = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
        font_watermark = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    except:
        font_quote = ImageFont.load_default()
        font_author = font_era = font_watermark = font_quote

    # Word-wrap quote
    words = quote.split()
    lines, current_line = [], ""
    max_width = W - 140
    for word in words:
        test_line = f"{current_line} {word}".strip()
        bbox = draw.textbbox((0, 0), test_line, font=font_quote)
        if bbox[2] - bbox[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    # Center quote
    line_height = 66
    total_text_height = len(lines) * line_height
    quote_y = (H - total_text_height) // 2 - 40

    for i, line in enumerate(lines):
        y = quote_y + i * line_height
        draw.text((W//2 + 2, y + 2), line, font=font_quote, fill='#000000', anchor='mm')
        draw.text((W//2, y), line, font=font_quote, fill='#FFFFFF', anchor='mm')

    # Author
    author_y = quote_y + total_text_height + 50
    draw.line([(W//2 - 80, author_y - 20), (W//2 + 80, author_y - 20)], fill='#C5A572', width=1)
    draw.text((W//2, author_y), f"— {author}", font=font_author, fill='#C5A572', anchor='mm')
    draw.text((W//2, author_y + 36), era, font=font_era, fill='#888888', anchor='mm')

    # Watermark
    draw.text((W//2, H - 80), "@syedos", font=font_watermark, fill='#444444', anchor='mm')

    bg.save(output_path, 'PNG', quality=95)
    print(f"Image saved: {output_path} ({os.path.getsize(output_path)} bytes)")
    return output_path


def get_daily_quote():
    day_of_year = datetime.now().timetuple().tm_yday
    idx = day_of_year % len(QUOTES)
    return QUOTES[idx]


def get_music_suggestion():
    category = random.choice(MUSIC_SUGGESTIONS)
    mood, songs = category
    song = random.choice(songs)
    return mood, song


if __name__ == '__main__':
    download_bg_if_missing()
    quote, author, era = get_daily_quote()
    mood, song = get_music_suggestion()
    today = datetime.now().strftime('%Y-%m-%d')
    output_path = f'/tmp/ig_story_{today}.png'
    create_gym_quote_image(quote, author, era, output_path)

    print(f"\n=== TODAY'S IG STORY ===")
    print(f"QUOTE: \"{quote}\"")
    print(f"AUTHOR: {author} ({era})")
    print(f"MUSIC: {mood} — {song}")
    print(f"IMAGE: {output_path}")
    print(f"=== READY TO POST ===")
