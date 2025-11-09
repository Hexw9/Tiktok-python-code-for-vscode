import pygame, sys, random, math, time

pygame.init()
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Khong thoi gian")

font = pygame.font.SysFont("Courier New", 58, bold=True)
clock = pygame.time.Clock()

lyrics = [
    ("Doi tay di tim hoi am", 50, 1),
    ("Doi mi den mau vuong van", 50, 2),
    ("La giay phut anh nhan ra , anh nhan ra, anh nhan ra..", 50, 1),
    ("Khi the gian ngung xoay vong", 50, 1),
    ("Theo chiec kim dong ho", 50, 1),
    ("Hai trai tim cung dan lay nhau , minh chua thay dau bao gio", 50, 1),
    ("Binh yen hoa ra la nhu the", 50, 1),
    ("Ngay dem khong con voi chia doi mat troi ngung roi", 50, 1),
    ("La giay phut ben canh em khong thoi gian nhu ngung troi", 50, 1),
    ("!HexX!", 30, 0.8),
]

WHITE, BLACK = (255, 255, 255), (0, 0, 0)

def draw_scanlines(surface):
    for y in range(0, HEIGHT, 10):
        pygame.draw.line(surface, (20, 20, 20), (0, y), (WIDTH, y))

def generate_static_surface():
    surf = pygame.Surface((WIDTH, HEIGHT))
    surf.set_alpha(50)
    return surf

def update_static_surface(surf):
    arr = pygame.surfarray.pixels3d(surf)
    arr[:] = (random.randint(0, 25),) * 3
    for _ in range(1000):
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)
        bright = random.randint(180, 255)
        arr[x, y] = (bright, bright, bright)
    del arr

def generate_stars(n=50):
    return [[random.randint(0, WIDTH), random.randint(0, HEIGHT), random.uniform(1, 2)] for _ in range(n)]

def update_stars(surface, stars):
    for s in stars:
        brightness = 180 + random.randint(-30, 30)
        color = (brightness, brightness, 255)
        pygame.draw.circle(surface, color, (int(s[0]), int(s[1])), int(s[2]))

def generate_hearts(n=10):
    hearts = []
    for _ in range(n):
        x = random.randint(0, WIDTH)
        y = random.randint(HEIGHT//2, HEIGHT)
        size = random.uniform(6, 10)
        speed = random.uniform(0.1, 0.4)
        hearts.append([x, y, size, speed])
    return hearts

def draw_heart(surface, x, y, size, color):
    t = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
    pygame.draw.circle(t, color, (size//2, size//2), size//2)
    pygame.draw.circle(t, color, (size + size//2, size//2), size//2)
    points = [(0, size//2), (size, size*1.8), (size*2, size//2)]
    pygame.draw.polygon(t, color, points)
    surface.blit(t, (x - size, y - size))

def update_hearts(surface, hearts):
    for h in hearts:
        draw_heart(surface, h[0], h[1], h[2], (255, 130, 180, 130))
        h[1] -= h[3]
        if h[1] < -10:
            h[0] = random.randint(0, WIDTH)
            h[1] = HEIGHT + random.randint(0, 50)

def draw_song_info(surface):
    overlay = pygame.Surface((330, 90), pygame.SRCALPHA)
    pygame.draw.rect(overlay, (10, 10, 10, 180), (0, 0, 330, 90), border_radius=12)
    pygame.draw.circle(overlay, (255, 180, 220), (40, 45), 25)
    pygame.draw.rect(overlay, (0, 0, 0), (30, 30, 6, 30))
    pygame.draw.rect(overlay, (0, 0, 0), (44, 30, 6, 30))
    title_font = pygame.font.SysFont("Arial", 28, bold=True)
    artist_font = pygame.font.SysFont("Arial", 24)
    title = title_font.render("Khong thoi gian", True, (255, 200, 220))
    artist = artist_font.render("Duong Domic", True, (230, 230, 250))
    overlay.blit(title, (80, 18))
    overlay.blit(artist, (80, 50))
    surface.blit(overlay, (40, HEIGHT - 110))

def wrap_text(text, font, max_width):
    words = text.split(" ")
    lines, current = [], ""
    for w in words:
        test_line = current + w + " "
        if font.size(test_line)[0] <= max_width - 300:
            current = test_line
        else:
            lines.append(current.strip())
            current = w + " "
    if current:
        lines.append(current.strip())
    return lines

static_layer = generate_static_surface()
scanline_layer = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
draw_scanlines(scanline_layer)
stars = generate_stars()
hearts = generate_hearts()

current_line, letter_index = 0, 0
last_char_time = time.time()
hold_start = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()

    screen.fill((10, 0, 20))

    update_static_surface(static_layer)
    screen.blit(static_layer, (0, 0))
    update_stars(screen, stars)
    update_hearts(screen, hearts)
    screen.blit(scanline_layer, (0, 0))

    pink_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pink_overlay.fill((255, 120, 180, 25))
    screen.blit(pink_overlay, (0, 0))

    if current_line < len(lyrics):
        text, delay, hold_time = lyrics[current_line]
        now = time.time()
        if letter_index < len(text) and now - last_char_time > delay / 1000.0:
            letter_index += 1
            last_char_time = now
        if letter_index == len(text):
            if hold_start is None:
                hold_start = now
            elif now - hold_start >= hold_time:
                current_line += 1
                letter_index = 0
                hold_start = None

        displayed = text[:letter_index]
        lines = wrap_text(displayed, font, WIDTH - 100)
        y = HEIGHT // 2 - len(lines) * font.get_height() // 2

    if current_line < len(lyrics):
        text, delay, hold_time = lyrics[current_line]
        now = time.time()
        if letter_index < len(text) and now - last_char_time > delay / 1000.0:
            letter_index += 1
            last_char_time = now
        if letter_index == len(text):
            if hold_start is None:
                hold_start = now
            elif now - hold_start >= hold_time:
                current_line += 1
                letter_index = 0
                hold_start = None

        displayed = text[:letter_index]
        lines = wrap_text(displayed, font, WIDTH - 100)
        y = HEIGHT // 2 - len(lines) * font.get_height() // 2

        for l in lines:
            main_color = (255, 230, 255)
            glow_color = (160, 0, 255)
            glow_intensity = 1 

            text_surface = font.render(l, True, main_color)
            glow_surface = font.render(l, True, glow_color)

            for i in range(1, glow_intensity + 1):
                alpha = max(10, 180 - i * 18)
                blurred = pygame.Surface(glow_surface.get_size(), pygame.SRCALPHA)
                glow = glow_color + (alpha,)
                blurred.fill((0, 0, 0, 0))
                blurred.blit(glow_surface, (0, 0))
                blurred.set_alpha(alpha)
                screen.blit(
                    blurred,
                    (
                        WIDTH // 2 - text_surface.get_width() // 2 - i // 2,
                        y - i // 2,
                    ),
                )

            rect = text_surface.get_rect(center=(WIDTH // 2, y + font.get_height() // 2))
            screen.blit(text_surface, rect)
            y += font.get_height() + 10

    draw_song_info(screen)
    pygame.display.flip()
    clock.tick(60)
