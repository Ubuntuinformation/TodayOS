import pygame
from pygame.locals import *
from PIL import Image

class BitmapViewerApp:
    def __init__(self, os_system):
        self.os_system = os_system
        self.title_font = pygame.font.SysFont('Consolas', 24, bold=True)
        self.image_surface = None
        self.image_path = None

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

    def handle_event(self, e):
        pass

    def draw(self, screen):
        screen.fill((15, 15, 15))
        header = self.title_font.render('Visualizador de Bitmap', True, (255, 255, 255))
        screen.blit(header, (16, 32))
        if self.image_surface:
            rect = self.image_surface.get_rect(center=(self.os_system.width // 2, self.os_system.height // 2 + 30))
            screen.blit(self.image_surface, rect)
            info = self.os_system.font.render(f'{self.image_path}', True, (220,220,220))
            screen.blit(info, (16, self.os_system.height - 32))
        else:
            texto = self.os_system.font.render('Selecione um arquivo de imagem no Gerenciador de Arquivos.', True, (220, 220, 220))
            screen.blit(texto, (16, 120))
