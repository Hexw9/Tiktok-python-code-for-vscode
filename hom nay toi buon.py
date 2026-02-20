import sys
import time
import random
import pygame
import os
from PIL import Image

pygame.init()
WIDTH, HEIGHT = 1250, 725
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("gs")
clock = pygame.time.Clock()

font_path = os.path.join(os.getcwd(), "DFVN-Excalifont.ttf")
font = pygame.font.Font(font_path, 30)

lyrics = [
    ("...", 300, 1000, (255, 255, 255)),
    ("Thương cho mối tình của tôi chẳng có vui..", 350, 250, (255, 255, 255)),
    ("Hỡi em này tôi rất yêu em", 375, 500, (255, 80, 80)),
    ("Sao , em lại ra đi?",750, 2500, (255, 255, 255)),
    ("Chờ .. những giấc mơ qua hay chờ..", 600, 500, (255, 80, 80)),
    ("hình bóng ai kia theo mùa", 450, 500, (180, 180, 180)),
    ("yêu dấu nay mang nỗi sầu", 450, 2650, (255, 255, 255)),
    ("Đợi .. một tiếng yêu đã thân thuộc", 600, 1200, (255, 255, 255)),
    ("Mà bỗng nghe sao xa lạ", 500, 1200, (255, 80, 80)),
    ("Như ngày hôm nay", 590, 1000, (255, 255, 255)),
]
gif_path = os.path.join(os.getcwd(), "eye.gif")
gif = Image.open(gif_path)

gif_frames = []

try:
    while True:
        frame = gif.convert("RGB")

        w, h = frame.size
        scale = min(WIDTH / w, HEIGHT / h)
        new_w = int(w * scale)
        new_h = int(h * scale)

        frame = frame.resize((new_w, new_h))
        frame = pygame.image.fromstring(frame.tobytes(), frame.size, "RGB")

        surf = pygame.Surface((WIDTH, HEIGHT))
        surf.fill((0, 0, 0))

        x = (WIDTH - new_w) // 2
        y = (HEIGHT - new_h) // 2
        surf.blit(frame, (x, y))

        gif_frames.append(surf)

        gif.seek(gif.tell() + 1)

except EOFError:
    pass

gif_index = 0

class Sparkle:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.alpha = random.randint(80, 180)
        self.alpha_dir = random.choice([-1, 1]) * random.randint(2, 5)
        self.angle = random.randint(0, 360)
        self.rot_speed = random.uniform(-0.4, 0.4)
        self.speed_x = random.uniform(-0.2, 0.2)
        self.speed_y = random.uniform(-0.2, 0.2)

    def update(self):
        self.alpha += self.alpha_dir
        if self.alpha < 60 or self.alpha > 200:
            self.alpha_dir *= -1

        self.angle = (self.angle + self.rot_speed) % 360
        self.x += self.speed_x
        self.y += self.speed_y

        if self.x < -self.size: self.x = WIDTH + self.size
        if self.x > WIDTH + self.size: self.x = -self.size
        if self.y < -self.size: self.y = HEIGHT + self.size
        if self.y > HEIGHT + self.size: self.y = -self.size

    def draw(self, surface):
        surf = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
        cx, cy = self.size, self.size
        color = (255, 255, 255, self.alpha)

        points = [
            (cx, cy - self.size),
            (cx + self.size//3, cy - self.size//3),
            (cx + self.size, cy),
            (cx + self.size//3, cy + self.size//3),
            (cx, cy + self.size),
            (cx - self.size//3, cy + self.size//3),
            (cx - self.size, cy),
            (cx - self.size//3, cy - self.size//3),
        ]

        pygame.draw.polygon(surf, color, points)
        surf = pygame.transform.rotate(surf, self.angle)
        rect = surf.get_rect(center=(self.x, self.y))
        surface.blit(surf, rect)

sparkles = [
    Sparkle(random.randint(0, WIDTH),
            random.randint(0, HEIGHT),
            random.randint(2, 5))
    for _ in range(40)
]

def draw_scanlines(surface):
    for y in range(0, HEIGHT, 2):
        pygame.draw.line(surface, (20, 20, 20), (0, y), (WIDTH, y))


def wrap_text(text, font, max_width):
    words = text.split(" ")
    lines, current = [], ""

    for w in words:
        test = current + w + " "
        if font.size(test)[0] <= max_width:
            current = test
        else:
            lines.append(current.strip())
            current = w + " "

    if current:
        lines.append(current.strip())

    return lines


def draw_lyrics(surface, text, color):
    lines = wrap_text(text, font, WIDTH-450)
    y = HEIGHT // 1.2 - len(lines) * font.get_height() // 2

    for l in lines:
        text_surface = font.render(l, True, color)
        rect = text_surface.get_rect(center=(WIDTH // 2, y))
        surface.blit(text_surface, rect)
        y += font.get_height() + 10

current_line = 0
displayed_text = ""
last_word_time = pygame.time.get_ticks()
word_index = 0
line_done = False

line_text, WORD_DELAY, LINE_DELAY, current_color = lyrics[current_line]
words = line_text.split()
running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(gif_frames[gif_index], (0, 0))
    gif_index = (gif_index + 1) % len(gif_frames)

    now = pygame.time.get_ticks()
    if not line_done and now - last_word_time >= WORD_DELAY:
        displayed_text += words[word_index] + " "
        word_index += 1
        last_word_time = now

        if word_index >= len(words):
            line_done = True
            line_end_time = now

    if line_done and now - line_end_time >= LINE_DELAY:
        current_line += 1
        if current_line >= len(lyrics):
            break

        line_text, WORD_DELAY, LINE_DELAY, current_color = lyrics[current_line]
        displayed_text = ""
        words = line_text.split()
        word_index = 0
        line_done = False
        last_word_time = now

    for s in sparkles:
        s.update()
        s.draw(screen)

    draw_lyrics(screen, displayed_text, current_color)
    draw_scanlines(screen)

    pygame.display.flip()
    clock.tick(20)

pygame.quit()
sys.exit()