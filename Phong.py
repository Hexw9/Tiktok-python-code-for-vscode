import sys
import time
import random
import pygame
import os

pygame.init()
WIDTH, HEIGHT = 1200, 675
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Phong")
clock = pygame.time.Clock()

def load_font(path, size=40):
    return pygame.font.Font(os.path.join(os.getcwd(), path), size)

lyrics = [
    (".", 0.0000000000000000001, 0.00000000000000000000000000000001, (0,0,0), (WIDTH//2, HEIGHT//2), "DFVN Cactus Jack.otf"),
    (".", 0.0000000000000000001, 0.000000000000000000001, (0,0,0), (WIDTH//2, HEIGHT//2), "DFVN Cactus Jack.otf"),
    (".", 0.0000000000000001, 0.000000000000000000000001, (0,0,0), (WIDTH//2, HEIGHT//2), "DFVN Cactus Jack.otf"),
    (".", 0.0000000000000001, 0.00000000000000000000000001, (0,0,0), (WIDTH//2, HEIGHT//2), "DFVN Cactus Jack.otf"),
    (".", 0.0000000000000000001, 0.00000000000000000000000000000001, (0,0,0), (WIDTH//2, HEIGHT//2), "DFVN Cactus Jack.otf"),
    (".", 0.0000000000000000001, 0.000000000000000000001, (0,0,0), (WIDTH//2, HEIGHT//2), "DFVN Cactus Jack.otf"),
    (".", 0.0000000000000001, 0.000000000000000000000001, (0,0,0), (WIDTH//2, HEIGHT//2), "DFVN Cactus Jack.otf"),
    (".", 0.0000000000000001, 0.00000000000000000000000001, (0,0,0), (WIDTH//2, HEIGHT//2), "DFVN Cactus Jack.otf"),
    (".", 0.0000000000000000001, 0.00000000000000000000000000000001, (0,0,0), (WIDTH//2, HEIGHT//2), "DFVN Cactus Jack.otf"),
    ("Lang nghe cau hat diu dang", 200, 750, (255,255,255), (WIDTH//1.1, HEIGHT//1.1), "DFVN-DarumadropOne.ttf"),
    ("Em dang hat nhe nhang em muon quay lwng", 150, 400, (255,255,255), (WIDTH//1, HEIGHT//2), "DFVN Fashion Wacks.otf"),
    ("De nhin thay vung troi", 200, 750, (0,0,0), (WIDTH//2.3, HEIGHT//2), "DFVN Fashion Wacks.otf"),
    ("Yeu Kieu nhat tran doi", 200, 750, (0,0,0), (WIDTH//2.5, HEIGHT//2), "DFVN-FreckleFace.ttf"),
    ("Tinh treo tren noc tran nha", 200, 300, (0,0,0), (WIDTH//3.7, HEIGHT//1.05), "Oswald-VariableFont_wght.ttf"),
    ("Nghe khong giong that tha", 200, 750, (0,0,0), (WIDTH//1.05, HEIGHT//1.3), "Oswald-VariableFont_wght.ttf"),
    ("Em noi di ra em ay chi vi", 200, 200, (255,255,255), (WIDTH//1.3, HEIGHT//2), "ArchivoBlack-Regular.ttf"),
    ("Nghe li tri tham thi", 150, 1500, (255,255,255), (WIDTH//1.9, HEIGHT//1.6), "RubikBurned-Regular.ttf"),
    ("Van co don minh em", 200, 500, (0,0,0), (WIDTH//2.5, HEIGHT//2), "BubblegumSans-Regular.ttf"),
    ("Nhung sao anh lai chang chiu duoc", 200, 500, (0,0,0), (WIDTH//2.5, HEIGHT//2), "BubblegumSans-Regular.ttf"),
    ("Anh dung di", 200, 500, (0,0,0), (WIDTH//2.5, HEIGHT//2), "BubblegumSans-Regular.ttf"),
    ("Dung de em mot minh o day", 200, 50000000000, (0,0,0), (WIDTH//2.5, HEIGHT//2), "BubblegumSans-Regular.ttf"),
]

bg_folder = "bg2"
bg_images = []
for i in range(len(lyrics)):
    img = pygame.image.load(os.path.join(bg_folder, f"{i}.jpg")).convert()
    img = pygame.transform.scale(img, (WIDTH, HEIGHT))
    bg_images.append(img)
def draw_scanlines(surface):
    for y in range(0, HEIGHT, 4):
        pygame.draw.line(surface, (20,20,20), (0,y), (WIDTH,y))
def draw_left_wrap(surface, text, font, color, pos, max_width=300):
    words = text.split(" ")
    base_x, base_y = pos
    x = base_x
    y = base_y
    x_offsets = [0, 120, 40, 160, 80, 200, 60]
    line_index = 0
    for w in words:
        word_surf = font.render(w, True, color)
        w_width = word_surf.get_width()
        space = font.size(" ")[0]

        if x + w_width > base_x + max_width:
            line_index += 1
            y += font.get_height() + 6
            x = base_x + x_offsets[line_index % len(x_offsets)]

        surface.blit(word_surf, (x, y))
        x += w_width + space
current_line = 0
displayed_text = ""
word_index = 0
line_done = False
last_word_time = pygame.time.get_ticks()

line_text, WORD_DELAY, LINE_DELAY, color, pos, font_path = lyrics[0]
font = load_font(font_path)
words = line_text.split()

while True:
    screen.blit(bg_images[current_line], (0,0))
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

        line_text, WORD_DELAY, LINE_DELAY, color, pos, font_path = lyrics[current_line]
        font = load_font(font_path)
        displayed_text = ""
        words = line_text.split()
        word_index = 0
        line_done = False
        last_word_time = now

    draw_left_wrap(
        screen,
        displayed_text,
        font,
        color,
        (pos[0] - 260, pos[1] - 120)
    )

    draw_scanlines(screen)
    pygame.display.flip()
    clock.tick(23)

pygame.time.delay(2000)
pygame.quit()
sys.exit()
