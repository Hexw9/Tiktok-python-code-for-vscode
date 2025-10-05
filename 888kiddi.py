import pygame, sys, time, random

pygame.init()
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("888-Kiddi")

font = pygame.font.SysFont("Arial", 60, bold=True)
logo_font = pygame.font.SysFont("Courier New", 20)

lyrics = [
    (" ",0.25,3),
    ("Niu lay doi canh tay", 0.25, 0.2),
    ("Du anh cung da thua biet em se doi thay", 0.15, 1),
    ("Anh cung dau biet dau tai sao moi thu lai xay ra the nay", 0.2, 1.6),
    ("Paranoid", 0.35, 0.5),
    ("Moi Chuyen roi se qua thoi", 0.28, 1.4),
    ("Ngam doi moi", 0.30, 1.2),
    ("Gio cung chang phai cua anh", 0.25, 1.5),
]


BLACK = (0, 0, 0)
WHITE = (230, 230, 230)
RED   = (200, 0, 0)
LOGO_COLOR = (180, 180, 180)

blood_drops = []

fog = []
for i in range(8):
    fog.append([random.randint(0, WIDTH), random.randint(0, HEIGHT),
                random.randint(80, 200), random.randint(40, 100), random.randint(1, 3)])

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

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    for fx in fog:
        rect = pygame.Surface((fx[2], fx[3]), pygame.SRCALPHA)
        rect.fill((200, 200, 200, 30))
        screen.blit(rect, (fx[0], fx[1]))
        fx[0] -= fx[4]
        if fx[0] + fx[2] < 0:
            fx[0] = WIDTH
            fx[1] = random.randint(0, HEIGHT)

    if line_index < len(lyrics):
        line, word_delay, line_delay = lyrics[line_index]
        words = line.split()

        if time.time() - last_word_time > word_delay and word_index < len(words):
            word_index += 1
            for _ in range(random.randint(0, 2)):
                blood_drops.append([random.randint(WIDTH//2-200, WIDTH//2+200), HEIGHT//2, 0])
            last_word_time = time.time()

        wrapped = wrap_text(words[:word_index], font, WIDTH * 0.5)

        y_start = HEIGHT //2.1
        for row, line_words in enumerate(wrapped):
            line_text = " ".join(line_words)
            text_surface = font.render(line_text, True, WHITE)
            rect = text_surface.get_rect(center=(WIDTH//2, y_start + row*50))
            screen.blit(text_surface, rect)

        if word_index == len(words):
            if time.time() - last_word_time > line_delay:
                line_index += 1
                word_index = 0
                last_word_time = time.time()

    for drop in blood_drops:
        pygame.draw.rect(screen, RED, (drop[0], drop[1]+drop[2], 3, 8))
        drop[2] += 3
    blood_drops = [d for d in blood_drops if d[1]+d[2] < HEIGHT]

    for _ in range(80):
        x = random.randint(0, WIDTH-1)
        y = random.randint(0, HEIGHT-1)
        color = (random.randint(80, 200),) * 3
        screen.set_at((x, y), color)

    logo_text = "@hexw_ - @hex2101"
    logo_surface = logo_font.render(logo_text, True, LOGO_COLOR)
    logo_rect = logo_surface.get_rect(center=(WIDTH-600, HEIGHT-15))
    screen.blit(logo_surface, logo_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
