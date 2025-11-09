import pygame, sys, time, random
from PIL import Image, ImageSequence

pygame.init()
WIDTH, HEIGHT = 1400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nang am")

font = pygame.font.SysFont("Arial", 70, bold=True)
logo_font = pygame.font.SysFont("Courier New", 20)

lyrics = [
    ("Lac vao khu rung hoa nay khu rung ngap mui huong nguoi ta",0.2,0.5),
    ("Danh tang em bai ca ki niem thang nam ta da qua", 0.25, 0.2),
    ("O ben anh duoc khong long nay anh cu trong rong", 0.25, 0.2),
    ("Dau van mai luu luyen nu cuoi tuoi", 0.25, 1.2),
    ("", 0.01, 0.1),
    ("Anh om doi vai nay dem ngay khong thoat ra duoc dau", 0.2, 0.5),
    ("Om theo bao giac mo o trong tung thang nam kia nhiem mau", 0.2, 0.5),
    ("em oi xin dung xa chang dong van luon lanh gia", 0.25, 0.6),
    ("Dung de long tan nat den bao ngay thang ta khong chung loi!!", 0.25, 0.5),
]

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (200, 0, 0)
LOGO_COLOR = (150, 150, 150)

blood_drops = []

dots = []
for _ in range(80):
    dots.append([
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT),
        random.uniform(0.5, 1.5), 
        random.randint(1, 3),  
        random.randint(100, 200)   # brightness
    ])


class MemeObject:
    def __init__(self, frames, x, y, speed):
        self.frames = frames
        self.x = x
        self.y = y
        self.speed = speed
        self.frame_index = 0
        self.frame_delay = random.randint(2, 4)
        self.frame_tick = 0

    def update(self):
        self.y += self.speed
        self.frame_tick += 1
        if self.frame_tick >= self.frame_delay:
            self.frame_tick = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
        if self.y > HEIGHT:
            self.y = -random.randint(50, 200)
            self.x = random.randint(0, WIDTH - 80)

    def draw(self, surface):
        frame = self.frames[self.frame_index]
        surface.blit(frame, (self.x, self.y))

def load_gif_frames(path, scale=0.4):
    img = Image.open(path)
    frames = []
    for frame in ImageSequence.Iterator(img):
        frame = frame.convert("RGBA")
        frame = frame.resize((int(frame.width*scale), int(frame.height*scale)))
        mode = frame.mode
        data = frame.tobytes()
        py_image = pygame.image.fromstring(data, frame.size, mode)
        frames.append(py_image)
    return frames


import os
memes = []
meme_folder = "memes"
if os.path.exists(meme_folder):
    for file in os.listdir(meme_folder):
        if file.lower().endswith((".gif", ".png", ".jpg", ".jpeg")):
            try:
                frames = load_gif_frames(os.path.join(meme_folder, file))
                memes.append(frames)
            except Exception as e:
                print("❌ Không load được:", file, e)

meme_objects = []
if memes:
    for _ in range(8):
        frames = random.choice(memes)
        meme_objects.append(MemeObject(frames, random.randint(0, WIDTH-100),
                                       random.randint(-200, HEIGHT),
                                       random.uniform(0.5, 1.2)))

def wrap_text(words, font, max_width):
    lines, current = [], []
    for w in words:
        test_line = " ".join(current + [w])
        if font.size(test_line)[0] <= max_width+200:
            current.append(w)
        else:
            lines.append(current)
            current = [w]
    if current:
        lines.append(current)
    return lines


def draw_glow_text(surface, text, pos, main_color=WHITE, glow_color=(255,255,255)):
    """Tạo hiệu ứng glow mờ quanh chữ"""
    glow_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    text_surface = font.render(text, True, glow_color)
    for offset in range(1, 6):  # độ dày viền sáng
        glow_surface.blit(text_surface, (pos[0]-offset, pos[1]))
        glow_surface.blit(text_surface, (pos[0]+offset, pos[1]))
        glow_surface.blit(text_surface, (pos[0], pos[1]-offset))
        glow_surface.blit(text_surface, (pos[0], pos[1]+offset))
    glow_surface.set_alpha(60)
    surface.blit(glow_surface, (0, 0))
    main_surface = font.render(text, True, main_color)
    surface.blit(main_surface, pos)


line_index, word_index = 0, 0
clock = pygame.time.Clock()
running = True
last_word_time = time.time()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    # Floating dots
    for d in dots:
        pygame.draw.circle(screen, (d[4], d[4], d[4]), (int(d[0]), int(d[1])), d[3])
        d[1] += d[2] * 0.5
        d[0] += random.uniform(-0.3, 0.3)
        if d[1] > HEIGHT:
            d[1] = -5
            d[0] = random.randint(0, WIDTH)
            d[4] = random.randint(100, 200)

    for m in meme_objects:
        m.update()
        m.draw(screen)

    if line_index < len(lyrics):
        line, word_delay, line_delay = lyrics[line_index]
        words = line.split()

        if time.time() - last_word_time > word_delay and word_index < len(words):
            word_index += 1
            for _ in range(random.randint(0, 2)):
                blood_drops.append([random.randint(WIDTH//2-200, WIDTH//2+200), HEIGHT//2, 0])
            last_word_time = time.time()

        wrapped = wrap_text(words[:word_index], font, WIDTH * 0.5)
        line_spacing = 80
        total_height = len(wrapped) * line_spacing 
        y_start = (HEIGHT - total_height) // 2
        for row, line_words in enumerate(wrapped):
            line_text = " ".join(line_words)
            text_surface = font.render(line_text, True, WHITE)
            rect = text_surface.get_rect(center=(WIDTH//2, y_start + row*line_spacing))
            draw_glow_text(screen, line_text, (rect.left, rect.top))
        if word_index == len(words):
            if time.time() - last_word_time > line_delay:
                line_index += 1
                word_index = 0
                last_word_time = time.time()
    logo_text = "@hexw_ - @hex2101"
    logo_surface = logo_font.render(logo_text, True, LOGO_COLOR)
    logo_rect = logo_surface.get_rect(center=(WIDTH-700, HEIGHT-15))
    screen.blit(logo_surface, logo_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
