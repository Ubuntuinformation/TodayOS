import pygame
from pygame.locals import *
from PIL import Image

class BitmapViewerApp:
    def __init__(self, os_system):
        self.os_system = os_system
        self.title_font = pygame.font.SysFont('Consolas', 24, bold=True)
        self.image_surface = None
        self.image_path = None

    def draw_logo(self, screen):
        pygame.draw.circle(screen, (180, 120, 255), (50, 50), 20)
        l = self.os_system.font.render('B', True, (255, 255, 255))
        screen.blit(l, (46, 42))

    def activate(self):
        pass

    def load_image(self, path):
        try:
            img = Image.open(path).convert('RGBA')
            w, h = img.size
            max_w = self.os_system.width - 40
            max_h = self.os_system.height - 100
            scale = min(1.0, min(max_w / w, max_h / h))
            if scale < 1.0:
                img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
            mode = img.mode
            data = img.tobytes()
            self.image_surface = pygame.image.fromstring(data, img.size, mode)
            self.image_path = path
        except Exception as e:
            self.image_surface = None
            self.image_path = None
            self.os_system.notification = f'Falha ao abrir imagem: {e}'

    def __init__(self, os_system):
        self.os_system = os_system
        self.title_font = pygame.font.SysFont('Consolas', 24, bold=True)
        self.image_surface = None
        self.image_path = None
        self.zoom = 1.0

    def activate(self):
        self.zoom = 1.0

    def handle_event(self, e):
        if e.type == KEYDOWN:
            if e.key in (K_PLUS, K_EQUALS):
                self.zoom = min(5.0, self.zoom + 0.1)
            elif e.key in (K_MINUS, K_UNDERSCORE):
                self.zoom = max(0.2, self.zoom - 0.1)
            elif e.key == K_0:
                self.zoom = 1.0
            elif e.key == K_r:
                if self.image_path:
                    self.load_image(self.image_path)

    def draw(self, screen):
        screen.fill((15, 15, 15))
        self.draw_logo(screen)
        header = self.title_font.render('Visualizador de Bitmap', True, (255, 255, 255))
        screen.blit(header, (16, 32))
        if self.image_surface:
            iw, ih = self.image_surface.get_size()
            target_w = int(iw * self.zoom)
            target_h = int(ih * self.zoom)
            img = pygame.transform.smoothscale(self.image_surface, (target_w, target_h))
            rect = img.get_rect(center=(self.os_system.width // 2, self.os_system.height // 2 + 30))
            screen.blit(img, rect)
            info = self.os_system.font.render(f'{self.image_path} | zoom:{self.zoom:.1f}', True, (220,220,220))
            screen.blit(info, (16, self.os_system.height - 54))
            hint = self.os_system.font.render('+/- para zoom, 0 reset, r reload', True, (220,220,220))
            screen.blit(hint, (16, self.os_system.height - 30))
        else:
            texto = self.os_system.font.render('Selecione um arquivo de imagem no Gerenciador de Arquivos.', True, (220, 220, 220))
            screen.blit(texto, (16, 120))
