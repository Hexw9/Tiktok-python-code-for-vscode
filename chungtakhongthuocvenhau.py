import pygame, sys, time, random, math

pygame.init()
WIDTH, HEIGHT = 900, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("STMTP")

font = pygame.font.SysFont("Arial", 90, bold=True)
logo_font = pygame.font.SysFont("Courier New", 20)

lyrics = [
    ("Tai vi anh thoi",0.3,0.4,"left"),
    ("yeu say me nen doi khi qua dai kho", 0.35, 0.65, 'right'),
    ("Nham mat o tho, anh khong muon lac vao trong noi dau nay", 0.25, 0.8, 'center'),
    ("Phia truoc bay gio ai dang nam chat ban tay cua em vay?", 0.25, 0.8, 'center'),
    ("Mong lung nhu 1 tro dua", 0.3, 0.8, 'left'),
    ("Anh xin gio tay rut lui thoi", 0.25, 0.8, 'right'),
    ("Trach ai bay gio day?", 0.2, 0.8, 'center'),
    ("Hexxed", 0.5, 0.8, 'center'),
    ("Chung ta khong thuoc ve nhau", 0.3, 1, 'left'),
    ("Chung ta khong thuoc ve nhau", 0.3, 1, 'center'),
    ("Chung ta khong thuoc ve nhau", 0.1, 0.2, 'right'),
    ("Em hay cu di ben nguoi ma em can", 0.3, 3, 'left'),
    (" ", 0.01, 1, 'center')
]

gradient_colors = [
    ((10, 30, 50), (60, 0, 90)),
    ((20, 10, 40), (150, 0, 100)),
    ((30, 20, 10), (180, 60, 20)),
    ((0, 20, 60), (0, 80, 180)),
    ((10, 0, 30), (90, 10, 120)),
    ((0, 10, 10), (20, 120, 100)),
    ((30, 10, 20), (120, 20, 60)),
    ((10, 10, 10), (60, 60, 60)),
    ((40, 0, 0), (180, 20, 20)),
    ((10, 10, 10), (30, 30, 30)),
]

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GLOW_COLOR = (255, 180, 120)
LOGO_COLOR = (200, 200, 200)

# (### THAY ĐỔI ###: Hàm tạo vignette surface, chỉ gọi 1 lần)
def create_vignette_surface(width, height, vignette_strength=180, vignette_radius_ratio=0.5):
    vignette_surf = pygame.Surface((width, height), pygame.SRCALPHA)
    center_x, center_y = width / 2, height / 2
    max_radius = min(width, height) / 2
    inner_radius = max_radius * vignette_radius_ratio
    for y in range(height):
        for x in range(width):
            dist = math.hypot(x - center_x, y - center_y)
            if dist > inner_radius:
                alpha = int(vignette_strength * ((dist - inner_radius) / (max_radius - inner_radius)))
                alpha = min(alpha, 255)
            else:
                alpha = 0
            vignette_surf.set_at((x, y), (0, 0, 0, alpha))
    return vignette_surf

def draw_background_gradient(surface, color1, color2):
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))

def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = []
    current_width = 0
    for word in words:
        word_display = word + (' ' if current_line else '')
        word_width = font.size(word_display)[0]

        if not current_line or current_width + word_width <= max_width - 100:
            current_line.append(word)
            current_width += font.size(word + (' ' if len(current_line) > 1 else ''))[0]
        else:
            lines.append(" ".join(current_line))
            current_line = [word]
            current_width = font.size(word)[0]

    if current_line:
        lines.append(" ".join(current_line))
    return lines

def draw_text_simple_glow(surface, text, pos):
    x, y = pos
    glow = font.render(text, True, GLOW_COLOR)
    glow.set_alpha(80)
    text_main = font.render(text, True, WHITE)
    offsets = [(-2, -2), (2, -2), (-2, 2), (2, 2)]
    for off_x, off_y in offsets:
        surface.blit(glow, (x + off_x, y + off_y))
    surface.blit(text_main, (x, y))

class Sparkle:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.alpha = random.randint(80, 180)
        self.alpha_dir = random.choice([-1, 1]) * random.randint(2, 5)
        self.angle = random.randint(0, 360)
        self.rot_speed = random.uniform(-0.5, 0.5)
        self.speed_x = random.uniform(-0.3, 0.3)
        self.speed_y = random.uniform(-0.3, 0.3)

    def update_and_draw(self, surface):
        self.alpha += self.alpha_dir
        if not 50 < self.alpha < 200:
            self.alpha_dir *= -1
            self.alpha = max(50, min(200, self.alpha))

        self.angle = (self.angle + self.rot_speed) % 360
        self.x += self.speed_x
        self.y += self.speed_y
        if self.x < -self.size: self.x = WIDTH + self.size
        elif self.x > WIDTH + self.size: self.x = -self.size
        if self.y < -self.size: self.y = HEIGHT + self.size
        elif self.y > HEIGHT + self.size: self.y = -self.size

        color = (255, 192, 203, self.alpha)
        sparkle_surf_base = pygame.Surface((self.size*2.5, self.size*2.5), pygame.SRCALPHA)
        center_x, center_y = sparkle_surf_base.get_width() // 2, sparkle_surf_base.get_height() // 2
        points = [
            (center_x, center_y - self.size), (center_x + self.size // 3, center_y - self.size // 3),
            (center_x + self.size, center_y), (center_x + self.size // 3, center_y + self.size // 3),
            (center_x, center_y + self.size), (center_x - self.size // 3, center_y + self.size // 3),
            (center_x - self.size, center_y), (center_x - self.size // 3, center_y - self.size // 3),
        ]
        pygame.draw.polygon(sparkle_surf_base, color, points)
        rotated_surf = pygame.transform.rotate(sparkle_surf_base, self.angle)
        rot_rect = rotated_surf.get_rect(center=(self.x, self.y))
        surface.blit(rotated_surf, rot_rect)


line_index = 0
word_index = 0
last_word_update = 0
is_typing = True
is_waiting = False
wait_start_time = 0

sparkles = []
for _ in range(40):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    size = random.randint(10, 25)
    sparkles.append(Sparkle(x, y, size))

clock = pygame.time.Clock()
running = True

pre_rendered_vignette = create_vignette_surface(WIDTH, HEIGHT, vignette_strength=180, vignette_radius_ratio=0.5)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    t = time.time()
    color1, color2 = gradient_colors[line_index % len(gradient_colors)]
    draw_background_gradient(screen, color1, color2)

    screen.blit(pre_rendered_vignette, (0, 0))

    for sp in sparkles:
        sp.update_and_draw(screen)

    if line_index < len(lyrics):
        line, word_delay, line_delay, alignment = lyrics[line_index]
        words_in_line = line.split(' ')

        if is_typing:
            if t - last_word_update > word_delay:
                if word_index < len(words_in_line):
                    word_index += 1
                    last_word_update = t
                else:
                    is_typing = False
                    is_waiting = True
                    wait_start_time = t

        if is_waiting:
            if t - wait_start_time > line_delay:
                is_waiting = False
                is_typing = True
                line_index = (line_index + 1) % len(lyrics)
                word_index = 0
                last_word_update = time.time()

        visible_words = words_in_line[:word_index]
        visible_text = " ".join(visible_words)

        if visible_text:
            wrapped = wrap_text(visible_text, font, WIDTH * 0.8)
            y_start = HEIGHT // 2 - (len(wrapped) * font.get_height()) // 2

            for row, line_text in enumerate(wrapped):
                text_surface = font.render(line_text, True, WHITE)
                text_width = text_surface.get_width()

                if alignment == 'center':
                    x_pos = WIDTH // 2 - text_width // 2
                elif alignment == 'left':
                    x_pos = 50
                elif alignment == 'right':
                    x_pos = WIDTH - text_width - 50
                else:
                    x_pos = WIDTH // 2 - text_width // 2

                y_pos = y_start + row * font.get_height()

                draw_text_simple_glow(screen, line_text, (x_pos, y_pos))

    logo_surface = logo_font.render("@hexw_ - @hex2101", True, LOGO_COLOR)
    logo_rect = logo_surface.get_rect(center=(WIDTH // 2, HEIGHT - 20))
    screen.blit(logo_surface, logo_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
