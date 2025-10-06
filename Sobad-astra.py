import pygame
import sys
import time
import random
import math

pygame.init()

WIDTH, HEIGHT = 1200, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sobad")

font = pygame.font.SysFont("Courier New", 60, bold=True)

lyrics = [
    "Gio ta da chia xa",
    "Tinh day sau giac mo chua thanh",
    "Em chang con la nhung bong hoa",
    "La vong tay em am dau anh a",
    "Dung cu mai gian hon",
    "De long dau don khong tin vao tinh yeu",
    "Thoi nhe anh oi",
    "Dung om lay chung cho rieng minh"
]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

WORD_DELAY = 300 
LINE_DELAY = 600  

clock = pygame.time.Clock()

def draw_scanlines(surface):

    for y in range(0, HEIGHT, 4):
        pygame.draw.line(surface, (20, 20, 20), (0, y), (WIDTH, y))


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


        pygame.display.flip()

        pygame.time.delay(WORD_DELAY)

   
    pygame.time.delay(LINE_DELAY)

pygame.time.delay(3000)
pygame.quit()
sys.exit()
