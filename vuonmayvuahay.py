import pygame
import sys
import time
import math

pygame.init()

WIDTH, HEIGHT = 1500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hien chu tung tu + Trai tim")

font = pygame.font.SysFont("Arial", 80)

lyrics = [
    "Thon thuc em da biet bao nhieu ngay",
    "Nguoi den ben co trong doi nay",
    "Tung thuoc phim cu nhu sum vay",
    "Cau Chuyen ta dang trong day?",
    "Nang lay di trai tim toi roi",
    "Dao buoc quanh co sao boi hoi?",
    "Cam giac nhu da co co hoi",
    "Doi loi yeu anh con chua noi!!"
]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (220, 20, 60)

word_delay = 0.3

def draw_heart(surface, x, y, size, color):
    """Vẽ trái tim đơn giản bằng 2 circle + 1 tam giác"""
    top_radius = size // 2
    pygame.draw.circle(surface, color, (x - top_radius, y), top_radius)
    pygame.draw.circle(surface, color, (x + top_radius, y), top_radius)
    points = [
        (x - size, y), 
        (x + size, y), 
        (x, y + size * 1.5)
    ]
    pygame.draw.polygon(surface, color, points)

for line in lyrics:
    words = line.split()
    displayed = ""

    for word in words:
        displayed += word + " "
        start_time = time.time()
        showing = True
        while showing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill(BLACK)
            text_surface = font.render(displayed.strip(), True,(255,255,255))
            rect = text_surface.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(text_surface, rect)
            blink = int(time.time() * 2) % 2 
            if blink:
                draw_heart(screen, WIDTH//2, HEIGHT - 100, 40, RED)

            pygame.display.flip()

            if time.time() - start_time > word_delay:
                showing = False

    time.sleep(0.6)

pygame.quit()
sys.exit()
