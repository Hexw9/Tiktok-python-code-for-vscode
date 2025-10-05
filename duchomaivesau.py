import pygame
import sys
import time
import random

pygame.init()

WIDTH, HEIGHT = 1000, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Du Cho Mai Ve Sau")

font = pygame.font.SysFont("Arial", 60, bold=True)
title_font = pygame.font.SysFont("Comic Sans MS", 28, bold=True)


lyrics = [
    [
        "Du cho mai ve sau",
        "Minh khong ben canh nhau",
        "Lam tim anh quan dau",
        "Anh trong ngong bao nhieu lau",
        "Du vuong van u sau",
        "Mua thu co phai mau",
        "Anh van muon yeu em"
    ],
    [
        "Bau troi dem khong may khong sao",
        "Trang treo tren cao khi long anh van nho nhung em nhieu",
        "Anh lam sao co the ngung suy nghi den doi moi em du chi mot giay"
    ]
]

SONG_TITLE = "Du Cho Mai Ve Sau"

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 60, 80)

meme = pygame.image.load("meo..jpg") #Đoạn này bỏ ảnh thì anh em bỏ ảnh trong file vscode hoặc python và nhớ là thay meo..jpg thành tên ảnh anh em cần nha
meme = pygame.transform.scale(meme, (300, 300))

stars = []
for _ in range(60):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    radius = random.randint(1, 3)
    speed = random.uniform(0.2, 1.2)
    stars.append([x, y, radius, speed])

def draw_stars():
    for s in stars:
        s[1] += s[3]
        if s[1] > HEIGHT:
            s[0] = random.randint(0, WIDTH - 350)
            s[1] = -5
            s[3] = random.uniform(0.2, 1.2)
        pygame.draw.circle(screen, WHITE, (int(s[0]), int(s[1])), s[2])

def draw_heart(surface, x, y, size, color):
    r = size // 2
    pygame.draw.circle(surface, color, (x - r, y - r), r)
    pygame.draw.circle(surface, color, (x + r, y - r), r)
    points = [(x - size, y - r), (x, y + size), (x + size, y - r)]
    pygame.draw.polygon(surface, color, points)

def wrap_text(text, font, max_width):
    words = text.split(" ")
    lines = []
    current = ""
    for w in words:
        test = (current + " " + w).strip()
        if font.size(test)[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines

clock = pygame.time.Clock()

for stanza in lyrics:
    for line in stanza:
        displayed = ""
        for ch in line:
            displayed += ch
            t0 = time.time()
            while time.time() - t0 < 0.05:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                screen.fill(BLACK)
                draw_stars()

                max_text_width = WIDTH - (350 + 40) 
                lines = wrap_text(displayed, font, max_text_width)

                line_height = font.size("Tg")[1]
                total_h = len(lines) * line_height + (len(lines)-1) * 10

                y = HEIGHT // 2 - total_h // 2
                for ln in lines:
                    ts = font.render(ln, True, WHITE)
                    rect = ts.get_rect(center=( (WIDTH - 350) // 2, y))
                    screen.blit(ts, rect)
                    y += line_height + 10

                screen.blit(meme, (WIDTH - 350, HEIGHT//2 - 150))
                title_surface = title_font.render(SONG_TITLE, True, WHITE)
                title_rect = title_surface.get_rect(center=(WIDTH - 200, HEIGHT//2 + 180))
                screen.blit(title_surface, title_rect)

                pygame.display.flip()
                clock.tick(57)

        hold_before_next = 0.5
        t_hold = time.time()
        while time.time() - t_hold < hold_before_next:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            screen.fill(BLACK)
            draw_stars()
            max_text_width = WIDTH - (350 + 40)
            lines = wrap_text(displayed, font, max_text_width)
            line_height = font.size("Tg")[1]
            total_h = len(lines) * line_height + (len(lines)-1) * 10
            y = HEIGHT // 2 - total_h // 2
            for ln in lines:
                ts = font.render(ln, True, WHITE)
                rect = ts.get_rect(center=((WIDTH - 350) // 2, y))
                screen.blit(ts, rect)
                y += line_height + 10
            screen.blit(meme, (WIDTH - 350, HEIGHT//2 - 150))
            title_surface = title_font.render(SONG_TITLE, True, WHITE)
            title_rect = title_surface.get_rect(center=(WIDTH - 200, HEIGHT//2 + 180))
            screen.blit(title_surface, title_rect)
            pygame.display.flip()
            clock.tick(60)

    time.sleep(3)

end_time = time.time()
while time.time() - end_time < 5:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(BLACK)
    draw_stars()
    draw_heart(screen, WIDTH//2 - 60, HEIGHT//2, 50, RED)
    draw_heart(screen, WIDTH//2 + 60, HEIGHT//2, 50, RED)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
