import pygame, sys, time, random, math

pygame.init()
WIDTH, HEIGHT = 1200,600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("888 - Love Mode")

font = pygame.font.SysFont("MS Gothic", 64, bold=True)
logo_font = pygame.font.SysFont("Courier New", 20)

lyrics = [
    ("Best decision of life", 0.25,0.5),
    ("Betting the love for you ride", 0.25, 0.5),
    ("You're gonna be the way i try", 0.15, 1),
    ("あ な た を 幸 せ に し た い。", 0.2, 0.9),
    ("You know that my husband", 0.35, 0.5),
    ("Our love is so perfect", 0.28, 1),
    ("No need for dessert and", 0.30, 0.9),
    ("Our love is still spinning", 0.25, 0.9),
    ("Hello my pisces man", 0.25, 0.9),
    ("Even though a part 10", 0.25, 0.9),
    ("So good in my present", 0.25, 0.9),
    ("Crazy love no reason.", 0.30, 1),
]

BLACK = (0, 0, 0)
WHITE = (245, 240, 240)
RED = (255, 90, 120)
PINK = (255, 160, 200)
LIGHT_PINK = (255, 200, 230)
LOGO_COLOR = (180, 180, 180)

hearts = []
for _ in range(30):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    speed = random.uniform(0.2, 0.9)
    size = random.randint(15, 35)
    color = random.choice([RED, PINK, LIGHT_PINK])
    alpha = random.randint(120, 220)
    hearts.append([x, y, speed, size, color, alpha])

def draw_heart(surface, x, y, size, color, alpha):
    heart_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
    r = size // 2
    pygame.draw.circle(heart_surface, color + (alpha,), (r, r), r)
    pygame.draw.circle(heart_surface, color + (alpha,), (r + r, r), r)
    points = [(0, r), (r, size + r), (size * 2, r)]
    pygame.draw.polygon(heart_surface, color + (alpha,), points)
    surface.blit(heart_surface, (x - size, y - size))

def wrap_text(words, font, max_width):
    lines, current = [], []
    for w in words:
        test_line = " ".join(current + [w])
        if font.size(test_line)[0] <= max_width:
            current.append(w)
        else:
            lines.append(current)
            current = [w]
    if current:
        lines.append(current)
    return lines

def draw_gradient(surface, t):
    color_top = (
        max(0, min(255, int(50 + 80 * math.sin(t * 0.2)))),
        max(0, min(255, int(0 + 40 * math.sin(t * 0.3)))),
        max(0, min(255, int(50 + 60 * math.sin(t * 0.25))))
    )
    color_bottom = (
        max(0, min(255, int(120 + 100 * math.sin(t * 0.15 + 1)))),
        max(0, min(255, int(30 + 40 * math.sin(t * 0.2 + 1.5)))),
        max(0, min(255, int(80 + 90 * math.sin(t * 0.1 + 2))))
    )

    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(color_top[0] * (1 - ratio) + color_bottom[0] * ratio)
        g = int(color_top[1] * (1 - ratio) + color_bottom[1] * ratio)
        b = int(color_top[2] * (1 - ratio) + color_bottom[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))


line_index, word_index = 0, 0
clock = pygame.time.Clock()
running = True
last_word_time = time.time()
start_time = time.time()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    t = time.time() - start_time
    draw_gradient(screen, t)

    for h in hearts:
        draw_heart(screen, int(h[0]), int(h[1]), h[3], h[4], h[5])
        h[1] -= h[2]
        h[0] += math.sin(pygame.time.get_ticks() * 0.001 + h[0] * 0.01) * 0.5
        if h[1] < -50:
            h[0] = random.randint(0, WIDTH)
            h[1] = HEIGHT + 50
            h[2] = random.uniform(0.2, 0.9)
            h[3] = random.randint(15, 35)
            h[4] = random.choice([RED, PINK, LIGHT_PINK])
            h[5] = random.randint(100, 220)

    if line_index < len(lyrics):
        line, word_delay, line_delay = lyrics[line_index]
        words = line.split()

        if time.time() - last_word_time > word_delay and word_index < len(words):
            word_index += 1
            last_word_time = time.time()

        wrapped = wrap_text(words[:word_index], font, WIDTH * 0.6)
        y_start = HEIGHT // 2
        for row, line_words in enumerate(wrapped):
            line_text = " ".join(line_words)
            text_surface = font.render(line_text, True, WHITE)
            rect = text_surface.get_rect(center=(WIDTH // 2, y_start + row * 80))
            screen.blit(text_surface, rect)

        if word_index == len(words):
            if time.time() - last_word_time > line_delay:
                line_index += 1
                word_index = 0
                last_word_time = time.time()

    logo_text = "@hexw_ - @hex2101 "
    logo_surface = logo_font.render(logo_text, True, LOGO_COLOR)
    logo_rect = logo_surface.get_rect(center=(WIDTH - 600, HEIGHT - 15))
    screen.blit(logo_surface, logo_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
