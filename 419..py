import pygame
import sys
import time
import random

pygame.init()

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("419")

font = pygame.font.SysFont("Arial", 60)#font chữ ae lên google tải thay file đuôi .ttf là giống trên video nha!!

title_font = pygame.font.SysFont("Arial", 36, bold=True)

lyrics = [
    "Cho anh mien man them mot chut thoi",
    "419 xin em them mot phut thoi",
    "SH Italy sau nhieu ngay leu heo tren Cub coi",
    "Vay thi doi gi nua toi day di anh muon duoc mut moi",
    "O kia nhu nao Sao nho Sao nho",
    "Sao lai khong follow nhau nho Nhau nho",
    "Xinh gai tinh quai thi thom anh cai",
    "Deo hieu la yeu nguoi tu bao gio"
] #Code này thay lời được nhé ae, muốn bài gì thì thay vào @Hexw_

SONG_TITLE = "Nhu Nao Cung Đuoc"  # bạn đổi tên tuỳ ý

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 80)
PINK = (255, 150, 200)
word_delay = 0.29

meme = pygame.image.load("meo..jpg")
meme = pygame.transform.scale(meme, (300, 300))

def render_text_multiline(text, font, color, max_width):
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    if current_line:
        lines.append(current_line.strip())
    return [font.render(line, True, color) for line in lines]


hearts = []
for _ in range(12):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    speed = random.uniform(0.3, 1.0)
    size = random.randint(20, 35)
    color = random.choice([RED, PINK, WHITE])
    hearts.append([x, y, speed, size, color])

def draw_heart(surface, x, y, size, color):
    r = size // 2
    pygame.draw.circle(surface, color, (x - r, y - r), r)
    pygame.draw.circle(surface, color, (x + r, y - r), r)
    points = [(x - size, y - r), (x, y + size), (x + size, y - r)]
    pygame.draw.polygon(surface, color, points)

for line in lyrics:
    words = line.split()
    displayed = ""

    for word in words:
        displayed += word + " "
        start_time = time.time()

        while time.time() - start_time < word_delay:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill(BLACK)

            text_surfaces = render_text_multiline(displayed.strip(), font, WHITE, WIDTH - 400)
            y = HEIGHT // 3
            for ts in text_surfaces:
                rect = ts.get_rect(center=(WIDTH//2 - 150, y))
                screen.blit(ts, rect)
                y += ts.get_height() + 10

            screen.blit(meme, (WIDTH - 320, HEIGHT//2 - 150))

            title_surface = title_font.render(SONG_TITLE, True, WHITE)
            title_rect = title_surface.get_rect(center=(WIDTH - 170, HEIGHT//2 + 180))
            screen.blit(title_surface, title_rect)

            for h in hearts:
                draw_heart(screen, int(h[0]), int(h[1]), h[3], h[4])
                h[1] -= h[2] 
                if h[1] < -50: 
                    h[0] = random.randint(0, WIDTH)
                    h[1] = HEIGHT + 50
                    h[2] = random.uniform(0.3, 1.0)
                    h[3] = random.randint(20, 35)
                    h[4] = random.choice([RED, PINK, WHITE])

            pygame.display.flip()

time.sleep(4.7)
pygame.quit()
sys.exit()
