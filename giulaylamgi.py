import pygame, sys, random, math, time

pygame.init()
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MÓNSTAR • Giu lay lam gi 🌙")

font = pygame.font.SysFont("Georgia", 58, bold=True)

clock = pygame.time.Clock()

lyrics = [
    (" ", 80, 2),
    ("Moi thu cu the luot theo", 50, 0.6),
    (" 1 con gio", 70, 1),
    (" ", 50, 1.5),
    ("Mot nguoi moi co le voi em ", 60, 0.7),
    ("la mai mai", 60, 2),
    (" ", 60, 0.7),
    ("Bo het qua khu co nhau", 60, 1),
    ("That lau", 60, 1),
    ("That lau..", 60, 1),
    ("Vi minh khong yeu nhau", 60, 1),
    ("Giu lay lam gi?", 60, 1),
    ("!HexX!", 30, 0.8),
]

WHITE, BLACK = (255, 255, 255), (0, 0, 0)

def draw_scanlines(surface):
    for y in range(0, HEIGHT, 6):
        pygame.draw.line(surface, (20, 0, 30), (0, y), (WIDTH, y))

def generate_static_particles(n=60):
    particles = []
    for _ in range(n):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        speed_x = random.uniform(-0.5, 0.5)
        speed_y = random.uniform(-0.2, 0.2)
        brightness = random.randint(100, 180)
        size = random.uniform(1.5, 3.0)
        particles.append([x, y, speed_x, speed_y, brightness, size])
    return particles

def update_static_particles(surface, particles):
    for p in particles:
        p[0] += p[2]
        p[1] += p[3]
        if p[0] < 0: p[0] = WIDTH
        if p[0] > WIDTH: p[0] = 0
        if p[1] < 0: p[1] = HEIGHT
        if p[1] > HEIGHT: p[1] = 0
        pygame.draw.circle(surface, (p[4], p[4], p[4]), (int(p[0]), int(p[1])), int(p[5]))

def generate_stars(n=40):
    stars = []
    for _ in range(n):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        size = random.uniform(1, 2)
        twinkle = random.uniform(0, math.pi * 2)
        stars.append([x, y, size, twinkle])
    return stars

def update_stars(surface, stars, t):
    for s in stars:
        s[3] += 0.02
        brightness = 100 + int(50 * math.sin(s[3]))
        color = (brightness, brightness, 200)
        pygame.draw.circle(surface, color, (int(s[0]), int(s[1])), int(s[2]))

class Leaf:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-HEIGHT, 0)
        self.size = random.uniform(28, 40)  
        self.speed = random.uniform(0.5, 1.0)  
        self.swing = random.uniform(1.0, 2.2)  
        self.angle = random.uniform(0, math.pi * 2)
        self.color = (170 + random.randint(-20, 20), 110, 70)
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-0.15, 0.15)  # xoay chậm

    def update(self):
        self.angle += 0.02
        self.rotation += self.rotation_speed
        self.x += math.sin(self.angle) * self.swing
        self.y += self.speed
        if self.y > HEIGHT:
            self.reset()

    def draw(self, surface):
        leaf_surface = pygame.Surface((self.size, self.size * 0.6), pygame.SRCALPHA)
        pygame.draw.ellipse(leaf_surface, self.color, (0, 0, self.size, self.size * 0.6))
        rotated = pygame.transform.rotate(leaf_surface, self.rotation)
        surface.blit(rotated, (self.x, self.y))

    def draw(self, surface):
        leaf_surface = pygame.Surface((self.size, self.size * 0.6), pygame.SRCALPHA)
        pygame.draw.ellipse(leaf_surface, self.color, (0, 0, self.size, self.size * 0.6))
        rotated = pygame.transform.rotate(leaf_surface, self.rotation)
        surface.blit(rotated, (self.x, self.y))

def generate_leaves(n=25):
    return [Leaf() for _ in range(n)]

def render_glow_text(text, pos, glow_color=(BLACK), main_color=(WHITE)):
    """
    Hiệu ứng phát sáng màu vàng nâu, ấm buồn kiểu retro.
    Ánh sáng tỏa nhẹ như đèn neon trong quán cũ.
    """
    for i in range(4, 0, -1):
        glow = font.render(text, True, glow_color)
        glow.set_alpha(30 + i * 30)
        screen.blit(glow, (pos[0] - i, pos[1] - i))
        screen.blit(glow, (pos[0] + i, pos[1] + i))
    base = font.render(text, True, main_color)
    screen.blit(base, pos)


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

def draw_song_info(surface):
    overlay = pygame.Surface((330, 90), pygame.SRCALPHA)
    pygame.draw.rect(overlay, (10, 10, 20, 160), (0, 0, 330, 90), border_radius=10)
    pygame.draw.circle(overlay, (255, 255, 255), (40, 45), 25)
    pygame.draw.rect(overlay, (0, 0, 0), (30, 30, 6, 30))
    pygame.draw.rect(overlay, (0, 0, 0), (44, 30, 6, 30))
    title_font = pygame.font.SysFont("Arial", 28, bold=True)
    artist_font = pygame.font.SysFont("Arial", 24)
    title = title_font.render("Giu lay lam gi", True, (230, 200, 255))
    artist = artist_font.render("MONSTAR", True, (180, 160, 230))
    overlay.blit(title, (80, 18))
    overlay.blit(artist, (80, 50))
    surface.blit(overlay, (40, HEIGHT - 110))

scanline_layer = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
draw_scanlines(scanline_layer)
stars = generate_stars()
leaves = generate_leaves()
particles = generate_static_particles()
t = 0

overlay_tint = pygame.Surface((WIDTH, HEIGHT))
overlay_tint.fill((40, 0, 60))
overlay_tint.set_alpha(60)

running = True
current_line = 0
letter_index = 0
last_char_time = time.time()
hold_start = None
background_gradient = pygame.Surface((WIDTH, HEIGHT))
for y in range(HEIGHT):
    r = int(25 + (y / HEIGHT) * 40)  
    g = int(15 + (y / HEIGHT) * 20) 
    b = int(10 + (y / HEIGHT) * 25) 
    pygame.draw.line(background_gradient, (r, g, b), (0, y), (WIDTH, y))

overlay_tint = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
overlay_tint.fill((40, 15, 10, 80)) 

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    t += 0.03
    screen.blit(background_gradient, (0, 0))

    update_static_particles(screen, particles)
    update_stars(screen, stars, t)

    for leaf in leaves:
        leaf.update()
        leaf.draw(screen)

    screen.blit(scanline_layer, (0, 0))
    screen.blit(overlay_tint, (0, 0))

    if current_line < len(lyrics):
        text, delay, hold_time = lyrics[current_line]
        now = time.time()
        if letter_index < len(text) and now - last_char_time > delay / 1000.0:
            letter_index += 1
            last_char_time = now
        if letter_index == len(text):
            if hold_start is None:
                hold_start = now
            elif now - hold_start >= hold_time:
                current_line += 1
                letter_index = 0
                hold_start = None

        displayed = text[:letter_index]
        lines = wrap_text(displayed, font, WIDTH - 100)
        y = HEIGHT // 2 - len(lines) * font.get_height() // 2
        for l in lines:
            rect = font.render(l, True, (255, 255, 255)).get_rect(center=(WIDTH // 2, y))
            render_glow_text(l, rect.topleft)
            y += font.get_height() + 10

    draw_song_info(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
