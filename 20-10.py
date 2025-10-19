import pygame, sys, time, math, random

pygame.init()
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("20/10 - Gui me yeu")

font = pygame.font.SysFont("Segoe UI Emoji", 50, bold=True, italic=True)
small_font = pygame.font.SysFont("Segoe UI Emoji", 26, italic=True)

lyrics = [(" ", 0.03, 1),
    ("Nay day la vay,", 0.07, 0.07),
    ("Nay day la voc,", 0.07, 0.071),
    ("Nay day la nhung doa hoa 🌸", 0.05, 0.071),
    ("He sang roi day,", 0.03, 0.071),
    ("Nang trong bo vay,", 0.05, 0.071),
    ("Ca mot vuon hoa nhi,", 0.07, 0.071),
    ("Dua vui cung gio,", 0.07, 0.071),
    ("Nua vui cung la,", 0.07, 0.071),
    ("Nua vui cung nhung khuc ca 🎶", 0.05, 0.071),
    ("Chuc cac ban nu 20/10 vui ve va xinh dep hon tung ngay nhe 💐", 0.07, 1),
]

background_colors = [
    (180, 120, 150),
    (160, 100, 130),
    (190, 130, 160),
    (150, 90, 120),
    (170, 110, 140)
]

hearts = []
for _ in range(30):
    x = random.randint(0, WIDTH)
    y = random.randint(-HEIGHT, HEIGHT)
    size = random.randint(10, 20)
    speed = random.uniform(0.3, 0.8)
    hearts.append([x, y, size, speed])

def draw_heart(surface, x, y, size, color):
    points = []
    for t in range(0, 360, 10):
        rad = math.radians(t)
        X = 16 * math.sin(rad) ** 3
        Y = 13 * math.cos(rad) - 5 * math.cos(2 * rad) - 2 * math.cos(3 * rad) - math.cos(4 * rad)
        points.append((x + X * size / 20, y - Y * size / 20))
    pygame.draw.polygon(surface, color, points)

def draw_soft_background(surface, color1, color2):
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))

def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = " ".join(current_line + [word])
        if font.size(test_line)[0] <= max_width-300:
            current_line.append(word)
        else:
            lines.append(" ".join(current_line))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))
    return lines

# Hạt sáng quanh chữ
class GlowParticle:
    def __init__(self, x, y):
        self.x = x + random.randint(-50, 50)
        self.y = y + random.randint(-30, 30)
        self.size = random.randint(2, 5)
        self.life = random.uniform(0.8, 1.5)
        self.birth = time.time()
        self.color = (255, random.randint(180, 220), random.randint(200, 255))

    def draw(self, surface):
        elapsed = time.time() - self.birth
        if elapsed < self.life:
            alpha = int(255 * (1 - elapsed / self.life))
            glow = pygame.Surface((self.size * 4, self.size * 4), pygame.SRCALPHA)
            pygame.draw.circle(glow, (*self.color, alpha), (self.size * 2, self.size * 2), self.size)
            surface.blit(glow, (self.x - self.size * 2, self.y - self.size * 2))
            return True
        return False

clock = pygame.time.Clock()
line_index = 0
char_index = 0
last_update = time.time()
waiting = False
wait_start = 0
particles = []

current_color = random.choice(background_colors)
next_color = random.choice(background_colors)

note = "💗 Chuc cac chi em phu nu 20/10 that hanh phuc 💗"

highlight_words = ["hoa", "vay", "nang", "gio", "vui"]

running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_soft_background(screen, current_color, next_color)

    for heart in hearts:
        heart[1] -= heart[3]
        if heart[1] < -20:
            heart[0] = random.randint(0, WIDTH)
            heart[1] = HEIGHT + random.randint(0, 200)
        draw_heart(screen, heart[0], heart[1], heart[2], (255, 150, 170))

    now = time.time()
    text, speed, delay = lyrics[line_index]

    if waiting:
        if now - wait_start > delay:
            waiting = False
            char_index = 0
            line_index = (line_index + 1) % len(lyrics)
            current_color = next_color
            next_color = random.choice(background_colors)
        else:
            pass
    else:
        if now - last_update > speed:
            if char_index < len(text):
                char_index += 1
            else:
                waiting = True
                wait_start = now
            last_update = now

    visible_text = text[:char_index]
    wrapped_lines = wrap_text(visible_text, font, WIDTH - 100)
    total_height = len(wrapped_lines) * font.get_linesize()
    y_start = HEIGHT // 2 - total_height // 2

    if any(word in text.lower() for word in highlight_words):
        for _ in range(4):
            x = WIDTH // 2 + random.randint(-200, 200)
            y = y_start + random.randint(-40, 40)
            particles.append(GlowParticle(x, y))

    for p in particles[:]:
        if not p.draw(screen):
            particles.remove(p)

    for i, line in enumerate(wrapped_lines):
        text_surface = font.render(line, True, (255, 235, 245))
        text_rect = text_surface.get_rect(center=(WIDTH // 2, y_start + i * font.get_linesize()))
        screen.blit(text_surface, text_rect)

    note_surface = small_font.render(note, True, (255, 220, 230))
    note_rect = note_surface.get_rect(center=(WIDTH // 2, HEIGHT - 50))
    screen.blit(note_surface, note_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
