import pygame, sys, time, random

pygame.init()
WIDTH, HEIGHT = 1300,800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ngu di em oi")

font = pygame.font.SysFont("Arial",80, bold=True)
logo_font = pygame.font.SysFont("Courier New", 20)

lyrics = [
    ("Gio di qua roi day", 0.25,1),
    ("Troi chang con may bay", 0.27, 1.8),
    ("Pho dang yen binh di vao trong giac say", 0.32, 2.8),
    ("Biet em dang lam chi", 0.3, 1),
    ("Tung giot buon tren mi", 0.3,1),
    ("Thoi thi xoa bong dang da khien em nhu vay", 0.28, 1.4),
    ("  ", 0.30,5),
]

BLACK = (0, 0, 0)
WHITE = (230, 230, 230)
LOGO_COLOR = (180, 180, 180)
CIRCLE_COLORS = [(255, 255, 255, 80), (200, 0, 0, 80), (150, 150, 150, 80)]


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


circles = []
def add_circle():
    x = WIDTH // 2
    y = HEIGHT // 2
    color = random.choice(CIRCLE_COLORS)
    circles.append([x, y, 0, color]) 

line_index, word_index = 0, 0
clock = pygame.time.Clock()
running = True
last_word_time = time.time()
last_circle_time = time.time()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

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
            rect = text_surface.get_rect(center=(WIDTH // 2, y_start + row * 70))
            screen.blit(text_surface, rect)

        if word_index == len(words):
            if time.time() - last_word_time > line_delay:
                line_index += 1
                word_index = 0
                last_word_time = time.time()
    if time.time() - last_circle_time > 0.6:
        add_circle()
        last_circle_time = time.time()

    for c in circles[:]:
        x, y, r, color = c
        surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.circle(surface, color, (x, y), r, 4)
        screen.blit(surface, (0, 0))
        c[2] += 5
        if c[2] > 600:
            circles.remove(c)

    logo_text = "@hexw_ - @hex2101"
    logo_surface = logo_font.render(logo_text, True, LOGO_COLOR)
    logo_rect = logo_surface.get_rect(center=(WIDTH - 700, HEIGHT - 15))
    screen.blit(logo_surface, logo_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
