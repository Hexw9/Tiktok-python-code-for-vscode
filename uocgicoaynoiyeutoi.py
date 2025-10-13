import pygame, sys, time, random, math

pygame.init()
WIDTH, HEIGHT = 1200,600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("yeuem?")

font = pygame.font.SysFont("Ariel", 70, bold=True)
logo_font = pygame.font.SysFont("Courier New", 20)

lyrics = [
    ("", 0.25,1.7),
    ("Nho thuong nhau chi lam trai tim dau", 0.2, 0.5),
    ("buoc di ma chang nho ten anh", 0.2, 0.5),
    ("Hua chi ba loi nham nhi xa xam", 0.2, 0.5),
    ("Roi em cung quay lung vi em het thuong anh", 0.2, 0.3),
    ("Khoc di em nhoe het mascara", 0.2, 0.5),
    ("Anh da nguoc len cao tai sao chang the yeu anh", 0.16, 0.5),
    ("Em noi rang anh rat tot babe a..", 0.2, 0.5),
    ("Nhung anh khong the ep buoc mot nguoi chang yeu anh",0.13, 0.5),
    ("Chang yeu anh chang yeu anh..", 0.23, 0.5),
    ("Anh la tro dua vui khi em bop nat tim anh", 0.14, 0.5),
    ("Anh lam nguoi ton thuong boi nhung suy nghi trong anh", 0.14, 0.5),
]

BLACK = (0, 0, 0)
WHITE = (245, 240, 240)
LOGO_COLOR = (160, 160, 160)

particles = []
for _ in range(50):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    speed = random.uniform(0.2, 0.8)
    size = random.randint(2, 5)
    alpha = random.randint(100, 220)
    particles.append([x, y, speed, size, alpha])

circle_effect = []

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

line_index, word_index = 0, 0
clock = pygame.time.Clock()
running = True
last_word_time = time.time()
start_time = time.time()

def clamp(val):
    return max(0, min(255, int(val)))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    t = time.time() - start_time

    pulse = 10 + 8 * math.sin(t * 1.5)
    red   = 10 + 15 * math.sin(t * 0.8)
    blue  = 15 + 25 * math.sin(t * 1.2)
    color_bg = (clamp(red + pulse), clamp(pulse // 3), clamp(blue + pulse))
    screen.fill(color_bg)

    for p in particles:
        x, y, speed, size, alpha = p
        color = (255, 180, 220, alpha)
        pygame.draw.circle(screen, color, (int(x), int(y)), size)
        p[1] -= speed
        p[0] += math.sin(t + x * 0.01) * 0.3
        if p[1] < -5:
            p[0] = random.randint(0, WIDTH)
            p[1] = HEIGHT + 5
            p[2] = random.uniform(0.2, 0.8)
            p[3] = random.randint(2, 5)
            p[4] = random.randint(100, 220)

    for c in circle_effect[:]:
        cx, cy, r, life = c
        life -= 1
        r += 10
        alpha = max(0, int(255 * (life / 30)))
        color = (255, 180, 220, alpha)
        surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.circle(surf, color, (cx, cy), int(r), 3)
        screen.blit(surf, (0, 0))
        if life <= 0:
            circle_effect.remove(c)
        else:
            c[2], c[3] = r, life

    if line_index < len(lyrics):
        line, word_delay, line_delay = lyrics[line_index]
        words = line.split()

        if time.time() - last_word_time > word_delay and word_index < len(words):
            word_index += 1
            last_word_time = time.time()
            circle_effect.append([WIDTH//2, HEIGHT//2, 50, 30])

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
