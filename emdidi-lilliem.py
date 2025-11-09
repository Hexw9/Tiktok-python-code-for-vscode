import pygame, sys, random, math, time

pygame.init()
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("em di di")

font = pygame.font.SysFont("Courier New", 58, bold=True)
clock = pygame.time.Clock()

lyrics = [
    (" ", 80, 2.2),
    ("Em nhu anh sao dang bay tren cao", 30, 0.8),
    ("Anh chi thay em o trong chiem bao", 30, 0.8),
    ("khong the nho em vi tim dang dau", 30, 0.8),
    ("Yeu mai luon la trong bao lau?", 30, 0.8),
    ("Anh bi so voi nhung loi hua", 30, 0.8),
    ("Hai ta xa tu ngay mua ...", 30, 0.8),
    ("Em co nho ve ngay xua ...", 30, 0.9),
    ("anh nghi la chang con nua", 30, 0.8),
    ("!HexX!", 30, 0.8),
]

WHITE, BLACK = (255, 255, 255), (0, 0, 0)


def draw_scanlines(surface):
    for y in range(0, HEIGHT, 3):
        pygame.draw.line(surface, (15, 15, 15), (0, y), (WIDTH, y))

def generate_static_surface():
    surf = pygame.Surface((WIDTH, HEIGHT))
    surf.set_alpha(80)
    return surf

def update_static_surface(surf):
    arr = pygame.surfarray.pixels3d(surf)
    arr[:] = (random.randint(0, 60),) * 3
    for _ in range(3500):  # mật độ nhiễu vừa phải
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)
        bright = random.randint(180, 255)
        arr[x, y] = (bright, bright, bright)
    del arr

def generate_stars(n=40):
    stars = []
    for _ in range(n):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        size = random.uniform(1.5, 2.5)
        speed = random.uniform(0.5, 1.2)
        stars.append([x, y, size, speed])
    return stars

def update_stars(surface, stars):
    for s in stars:
        s[1] += s[3]
        if s[1] > HEIGHT:
            s[0] = random.randint(0, WIDTH)
            s[1] = random.randint(-20, 0)
        pygame.draw.circle(surface, (255, 255, 255), (int(s[0]), int(s[1])), int(s[2]))
def generate_rain(n=80):
    rain = []
    for _ in range(n):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        length = random.randint(8, 15)
        speed = random.uniform(3, 7)
        rain.append([x, y, length, speed])
    return rain
def update_rain(surface, rain):
    for drop in rain:
        x, y, length, speed = drop
        end_y = y + length
        pygame.draw.line(surface, (255, 255, 255), (x, y), (x, end_y), 1)
        drop[1] += speed
        if drop[1] > HEIGHT:
            drop[0] = random.randint(0, WIDTH)
            drop[1] = random.randint(-20, 0)-
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
def draw_song_info(surface):
    overlay = pygame.Surface((330, 90), pygame.SRCALPHA)
    pygame.draw.rect(overlay, (0, 0, 0, 160), (0, 0, 330, 90), border_radius=10)-
    pygame.draw.circle(overlay, (255, 255, 255), (40, 45), 25)
    pygame.draw.rect(overlay, (0, 0, 0), (30, 30, 6, 30))
    pygame.draw.rect(overlay, (0, 0, 0), (44, 30, 6, 30))
    title_font = pygame.font.SysFont("Arial", 28, bold=True)
    artist_font = pygame.font.SysFont("Arial", 24)
    title = title_font.render("Em Di Di", True, (255, 230, 200))
    artist = artist_font.render("Lil Liem", True, (230, 230, 230))

    overlay.blit(title, (80, 18))
    overlay.blit(artist, (80, 50))
    surface.blit(overlay, (40, HEIGHT - 110))
static_layer = generate_static_surface()
scanline_layer = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
draw_scanlines(scanline_layer)
stars = generate_stars()
rain = generate_rain()
running = True
current_line = 0
letter_index = 0
last_char_time = time.time()
hold_start = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BLACK)
    update_static_surface(static_layer)
    screen.blit(static_layer, (0, 0))
    update_stars(screen, stars)
    screen.blit(scanline_layer, (0, 0))
    update_rain(screen, rain)

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
            color = (255, 255, 255) if random.random() > 0.05 else (200, 200, 200)
            text_surface = font.render(l, True, color)
            rect = text_surface.get_rect(center=(WIDTH // 2, y))
            screen.blit(text_surface, rect)
            y += font.get_height() + 10

    draw_song_info(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
