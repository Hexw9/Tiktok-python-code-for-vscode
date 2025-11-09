import pygame
import sys
import time
import random
import cv2
import numpy as np


pygame.init()
WIDTH, HEIGHT = 1300, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sobad")

font = pygame.font.SysFont("Courier New", 60, bold=True)

lyrics = [
    ("You're the sunshine of my lifeeeeeeeee", 450, 3300),
    ("i just wanna see", 350, 1500),
    ("how beautiful you are", 350, 2000),
    ("You know that i see it", 400, 1200),
    ("i know you're a STAR", 300, 2500),
]

WHITE = (255, 255, 255)
WORD_DELAY_DEFAULT = 400
LINE_DELAY_DEFAULT = 1000

clock = pygame.time.Clock()

def draw_scanlines(surface):
    for y in range(0, HEIGHT, 4):
        pygame.draw.line(surface, (20, 20, 20), (0, y), (WIDTH, y))

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

video_path = "flower.mp4"
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("❌ Không mở được video:", video_path)
    sys.exit()

current_line = 0
displayed_text = ""
last_word_time = pygame.time.get_ticks()
word_index = 0
line_done = False

line_text, WORD_DELAY, LINE_DELAY = lyrics[current_line]
words = line_text.split()

def draw_lyrics(surface, text):
    lines = wrap_text(text, font, WIDTH - 100)
    y = HEIGHT // 2 - len(lines) * font.get_height() // 2
    for l in lines:
        text_surface = font.render(l, True, WHITE)
        rect = text_surface.get_rect(center=(WIDTH // 2, y))
        surface.blit(text_surface, rect)
        y += font.get_height() + 10

while True:
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = cap.read()
    frame = cv2.resize(frame, (WIDTH, HEIGHT))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_surface = pygame.surfarray.make_surface(np.flipud(np.rot90(frame)))
    screen.blit(frame_surface, (0, 0))

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

        line_text, WORD_DELAY, LINE_DELAY = lyrics[current_line] if len(lyrics[current_line]) == 3 else (
            lyrics[current_line][0],
            WORD_DELAY_DEFAULT,
            LINE_DELAY_DEFAULT
        )
        displayed_text = ""
        words = line_text.split()
        word_index = 0
        line_done = False
        last_word_time = now

    draw_lyrics(screen, displayed_text)

    draw_scanlines(screen)

    pygame.display.flip()
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            pygame.quit()
            sys.exit()

pygame.time.delay(2000)
cap.release()
pygame.quit()
sys.exit()
