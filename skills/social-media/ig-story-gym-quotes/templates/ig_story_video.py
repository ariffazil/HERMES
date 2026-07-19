#!/usr/bin/env python3
"""
IG Story Video Generator v2 — Gym Motivational Quote
Gym photo bg + dark overlay + animated text + bass beat.
Output: 1080x1920 MP4, ~8 seconds, with audio.
"""

import os
import random
import subprocess
import shutil
import wave
import numpy as np
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ═══════════════════════════════════════════════════════════════
# QUOTES
# ═══════════════════════════════════════════════════════════════
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
    ("I hated every minute of training, but I said, dont quit. Suffer now and live the rest of your life as a champion.", "Muhammad Ali", "The Greatest"),
    ("The successful warrior is the average man, with laser-like focus.", "Bruce Lee", "Martial Artist"),
    ("You have power over your mind, not outside events.", "Marcus Aurelius", "Roman Emperor"),
    ("No citizen has a right to be an amateur in the matter of physical training.", "Socrates", "Philosopher"),
    ("The more you sweat in training, the less you bleed in combat.", "Richard Marcinko", "Navy SEAL"),
    ("Fall seven times, stand up eight.", "Japanese Proverb", "Bushido"),
    ("The body achieves what the mind believes.", "Napoleon Hill", "Author"),
    ("Motivation is what gets you started. Habit is what keeps you going.", "Jim Rohn", "Philosopher"),
    ("Everybody wants to be a bodybuilder, but nobody wants to lift no heavy-ass weights.", "Ronnie Coleman", "8x Mr. Olympia"),
    ("There are no shortcuts. Everything is reps, reps, reps.", "Arnold Schwarzenegger", "7x Mr. Olympia"),
    ("Suffer the pain of discipline or suffer the pain of regret.", "Jim Rohn", "Philosopher"),
]

MUSIC_SUGGESTIONS = [
    ("Hype", ["Eye of the Tiger - Survivor", "Lose Yourself - Eminem", "Till I Collapse - Eminem"]),
    ("Grind", ["HUMBLE. - Kendrick Lamar", "Power - Kanye West", "Stronger - Kanye West"]),
    ("Mindset", ["Started From the Bottom - Drake", "Champion - Kanye West", "Unstoppable - Sia"]),
    ("Beast Mode", ["X Gon Give It to Ya - DMX", "Jumpman - Drake & Future", "Blinding Lights - The Weeknd"]),
]

BG_IMAGES = ['/tmp/gym_bg_1.jpg', '/tmp/gym_bg_2.jpg', '/tmp/gym_bg_3.jpg', '/tmp/gym_bg_4.jpg']


def generate_beat(output_path, duration=8, bpm=130):
    """Generate dark bass-heavy beat using numpy + wave."""
    sr = 44100
    t = np.linspace(0, duration, sr * duration)
    beat_interval = 60 / bpm

    # Kick drum (low freq burst on beats)
    kick = np.zeros_like(t)
    for i in range(int(duration / beat_interval)):
        start = int(i * beat_interval * sr)
        end = min(start + int(0.15 * sr), len(t))
        kick_t = np.linspace(0, 0.15, end - start)
        kick[start:end] = 0.7 * np.sin(2 * np.pi * 55 * kick_t) * np.exp(-12 * kick_t)

    # Hi-hat (noise burst every half beat)
    hihat = np.zeros_like(t)
    for i in range(int(duration / (beat_interval / 2))):
        start = int(i * (beat_interval / 2) * sr)
        end = min(start + int(0.04 * sr), len(t))
        hihat_t = np.linspace(0, 0.04, end - start)
        hihat[start:end] = 0.15 * np.random.randn(end - start) * np.exp(-40 * hihat_t)

    # Sub bass
    sub = 0.12 * np.sin(2 * np.pi * 40 * t) + 0.08 * np.sin(2 * np.pi * 60 * t)

    # Mix + fade out
    mix = kick + hihat + sub
    fade_out = np.ones_like(t)
    fade_out[-sr:] = np.linspace(1, 0, sr)
    mix *= fade_out
    mix = mix / np.max(np.abs(mix)) * 0.85

    # Write WAV
    audio = (mix * 32767).astype(np.int16)
    with wave.open(output_path, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(audio.tobytes())

    print(f"Beat: {output_path} ({os.path.getsize(output_path)} bytes, {duration}s, BPM {bpm})")


def create_frames(quote, author, era, frames_dir, num_frames=240):
    """Generate animation frames with fade-in quote."""
    W, H = 1080, 1920
    os.makedirs(frames_dir, exist_ok=True)

    # Load background
    bg_path = random.choice([p for p in BG_IMAGES if os.path.exists(p)])
    bg_raw = Image.open(bg_path).convert('RGB').resize((W, H), Image.LANCZOS)
    bg_raw = bg_raw.filter(ImageFilter.GaussianBlur(radius=3))

    # Dark overlay
    overlay = Image.new('RGB', (W, H), (0, 0, 0))
    mask = Image.new('L', (W, H))
    mask_draw = ImageDraw.Draw(mask)
    for y in range(H):
        dist = abs(y - H * 0.45) / H
        opacity = int(180 - 80 * dist)
        mask_draw.line([(0, y), (W, y)], fill=max(100, min(200, opacity)))
    bg = Image.composite(overlay, bg_raw, mask)

    # Fonts
    try:
        font_quote = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
        font_author = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
        font_era = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
        font_watermark = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    except:
        font_quote = ImageFont.load_default()
        font_author = font_era = font_watermark = font_quote

    # Word-wrap
    tmp_draw = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    words = quote.split()
    lines, current_line = [], ""
    for word in words:
        test = f"{current_line} {word}".strip()
        bbox = tmp_draw.textbbox((0, 0), test, font=font_quote)
        if bbox[2] - bbox[0] <= W - 140:
            current_line = test
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    line_height = 66
    total_h = len(lines) * line_height
    quote_y = (H - total_h) // 2 - 40
    author_y = quote_y + total_h + 50

    # Generate frames
    for fi in range(num_frames):
        img = bg.copy()
        draw = ImageDraw.Draw(img)

        # Animation: fade in 30-90, hold 90-210, fade out 210-240
        if fi < 30:
            alpha = 0
        elif fi < 90:
            alpha = (fi - 30) / 60
        elif fi < 210:
            alpha = 1.0
        else:
            alpha = max(0, 1.0 - (fi - 210) / 30)

        if alpha > 0:
            slide = int((1 - alpha) * 30)
            for i, line in enumerate(lines):
                y = quote_y + i * line_height + slide
                draw.text((W//2 + 2, y + 2), line, font=font_quote, fill=(0, 0, 0), anchor='mm')
                c = int(255 * alpha)
                draw.text((W//2, y), line, font=font_quote, fill=(c, c, c), anchor='mm')

            gc = (int(197*alpha), int(165*alpha), int(114*alpha))
            draw.line([(W//2 - 80, author_y - 20), (W//2 + 80, author_y - 20)], fill=gc, width=1)
            draw.text((W//2, author_y), f"— {author}", font=font_author, fill=gc, anchor='mm')
            gr = int(136 * alpha)
            draw.text((W//2, author_y + 36), era, font=font_era, fill=(gr, gr, gr), anchor='mm')

        draw.text((W//2, H - 80), "@syedos", font=font_watermark, fill='#444444', anchor='mm')
        img.save(os.path.join(frames_dir, f'frame_{fi:04d}.png'), 'PNG')

    print(f"Frames: {num_frames} in {frames_dir}")


def create_video(frames_dir, beat_path, output_path, fps=30):
    """Combine frames + beat into MP4."""
    cmd = [
        'ffmpeg', '-y',
        '-framerate', str(fps),
        '-i', os.path.join(frames_dir, 'frame_%04d.png'),
        '-i', beat_path,
        '-c:v', 'libx264', '-preset', 'fast', '-crf', '23', '-pix_fmt', 'yuv420p',
        '-c:a', 'aac', '-b:a', '128k',
        '-shortest', '-movflags', '+faststart',
        output_path
    ]
    subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    print(f"Video: {output_path} ({os.path.getsize(output_path)} bytes)")


def get_daily_quote():
    idx = datetime.now().timetuple().tm_yday % len(QUOTES)
    return QUOTES[idx]


def get_music_suggestion():
    cat = random.choice(MUSIC_SUGGESTIONS)
    return cat[0], random.choice(cat[1])


if __name__ == '__main__':
    quote, author, era = get_daily_quote()
    mood, song = get_music_suggestion()
    today = datetime.now().strftime('%Y-%m-%d')

    frames_dir = '/tmp/ig_frames'
    beat_path = '/tmp/ig_beat.wav'
    video_path = f'/tmp/ig_story_{today}.mp4'

    print("=== BEAT ===")
    generate_beat(beat_path)

    print("=== FRAMES ===")
    create_frames(quote, author, era, frames_dir)

    print("=== VIDEO ===")
    create_video(frames_dir, beat_path, video_path)

    shutil.rmtree(frames_dir, ignore_errors=True)

    print(f"\n=== DONE ===")
    print(f"QUOTE: {quote}")
    print(f"AUTHOR: {author} ({era})")
    print(f"VIDEO: {video_path}")
