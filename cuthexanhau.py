import pygame
import sys
import time
import random
import math

pygame.init()

WIDTH, HEIGHT = 1200, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cu The Xa Nhau")

font = pygame.font.SysFont("Courier New", 48, bold=True)

lyrics = [
    "Cu the xa nhau, anh khong luyen tiec gi",
    "Se mat bao lau, em thoi uot dam doi mi",
    "Noi nho keo den, xa roi anh co phai la sai",
    "Hom qua hai ta, lo say bye la bye",
    "Chet roi! Minh da noi chia tay nguoi ta mat roi!",
    "Nguoi dong y ngay khi em cat loi",
    "Vay la anh da het yeu em lau lam roi"
]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

WORD_DELAY = 300  
LINE_DELAY = 600 

clock = pygame.time.Clock()

def draw_scanlines(surface):
    """Sọc ngang retro"""
    for y in range(0, HEIGHT, 4):
        pygame.draw.line(surface, (20, 20, 20), (0, y), (WIDTH, y))

def fisheye_surface(surface):
    arr = pygame.surfarray.array3d(surface)
    new_surf = pygame.Surface((WIDTH, HEIGHT))
    cx, cy = WIDTH // 2, HEIGHT // 2
    radius = min(cx, cy)
    for x in range(WIDTH):
        for y in range(HEIGHT):
            dx = (x - cx) / radius
            dy = (y - cy) / radius
            r = math.sqrt(dx*dx + dy*dy)
            if r == 0:
                nx, ny = cx, cy
            else:
                nr = math.atan(r) / (math.pi/2)
                nx = int(cx + dx * nr * radius)
                ny = int(cy + dy * nr * radius)
            if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
                new_surf.set_at((x, y), arr[nx][ny])
    return new_surf

def wrap_text(text, font, max_width):
    words = text.split(" ")
    lines, current = [], ""
    for w in words:
        test_line = current + w + " "
        if font.size(test_line)[0] <= max_width-300:
            current = test_line
        else:
            lines.append(current.strip())
            current = w + " "
    if current:
        lines.append(current.strip())
    return lines

for line in lyrics:
    displayed = ""
    words = line.split(" ")

    for word in words:
        displayed += word + " "

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)

        lines = wrap_text(displayed, font, WIDTH - 100)
        y = HEIGHT // 2 - len(lines) * font.get_height() // 2
        for l in lines:
            text_surface = font.render(l, True, WHITE)
            rect = text_surface.get_rect(center=(WIDTH//2, y))
            screen.blit(text_surface, rect)
            y += font.get_height() + 10

        draw_scanlines(screen)

        distorted = fisheye_surface(screen)
        screen.blit(distorted, (0, 0))

        pygame.display.flip()

        pygame.time.delay(WORD_DELAY)

    pygame.time.delay(LINE_DELAY)

pygame.time.delay(3000)
pygame.quit()
sys.exit()
