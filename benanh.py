import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 1200, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Karaoke Romantic Retro")

font = pygame.font.SysFont("Courier New", 60, bold=True)

lyrics = [
    "Toi chi muon o ben nang",
    "Vi co mui huong nong ngat ngay",
    "Em da di roi, de lai cho anh ca vuon hoa",
    "Biet se som thoi chang con ai ke canh ben ta",
    "Muon o ben em, tam hon anh vuot ngan phong ba",
    "Chang the quen em, du thoi gian voi vang nhanh qua",
    "Nhung nho nhung xua, dong day trong anh nhu vuon hoa"
]

line_delays = [1000, 1500, 1500, 1000, 1000, 1000, 1500]
WORD_DELAY = 200

WHITE = (255, 255, 255)
PINK = (255, 180, 180)

class FloatingObject:
    def __init__(self, x, y, size, color, speed, alpha=180):
        self.x, self.y, self.size = x, y, size
        self.color, self.speed, self.alpha = color, speed, alpha
    def move(self): self.y -= self.speed
    def draw(self, surf):
        bubble = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
        pygame.draw.circle(bubble, (*self.color, self.alpha), (self.size, self.size), self.size)
        surf.blit(bubble, (int(self.x-self.size), int(self.y-self.size)))

floating_objects = []

background = pygame.Surface((WIDTH, HEIGHT))
for y in range(HEIGHT):
    color = (255, int(100 + 55 * y/HEIGHT), int(150 + 50 * y/HEIGHT))
    pygame.draw.line(background, color, (0, y), (WIDTH, y))
for y in range(0, HEIGHT, 4):
    pygame.draw.line(background, (255, 200, 200), (0, y), (WIDTH, y))

def wrap_text(text, font, max_width):
    words, lines, current = text.split(" "), [], ""
    for w in words:
        test = current + w + " "
        if font.size(test)[0] <= max_width - 300: current = test
        else: lines.append(current.strip()); current = w + " "
    if current: lines.append(current.strip())
    return lines

def render_glow(surface, text, font, x, y, color, glow, r=5):
    for dx in range(-r, r+1):
        for dy in range(-r, r+1):
            if dx*dx + dy*dy <= r*r:
                surface.blit(font.render(text, True, glow), font.render(text, True, glow).get_rect(center=(x+dx, y+dy)))
    surface.blit(font.render(text, True, color), font.render(text, True, color).get_rect(center=(x, y)))

for i, line in enumerate(lyrics):
    displayed, words = "", line.split(" ")
    for word in words:
        displayed += word + " "
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()

        screen.blit(background, (0, 0)) 

        lines = wrap_text(displayed, font, WIDTH - 100)
        y = HEIGHT//2 - len(lines)*font.get_height()//2
        for l in lines:
            render_glow(screen, l, font, WIDTH//2, y, WHITE, PINK)
            y += font.get_height() + 10

        if random.random() < 0.1:
            floating_objects.append(
                FloatingObject(
                    random.randint(50, WIDTH-50),
                    HEIGHT-20,
                    random.randint(8, 20),
                    PINK,
                    random.uniform(0.3, 1.0),
                    alpha=random.randint(80, 200)
                )
            )
        new_objs = []
        for obj in floating_objects:
            obj.move(); obj.draw(screen)
            if obj.y > -30: new_objs.append(obj)
        floating_objects = new_objs

        pygame.display.flip()
        pygame.time.delay(WORD_DELAY)

    pygame.time.delay(line_delays[i])

pygame.time.delay(3000)
pygame.quit()
sys.exit()
