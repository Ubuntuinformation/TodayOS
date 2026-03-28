import os
import subprocess
import pygame
from pygame.locals import *
from PIL import Image, ImageDraw
from todayos.apps.shell import ShellApp
from todayos.apps.notepad import NotepadApp
from todayos.apps.filemanager import FileManagerApp
from todayos.apps.bitmap_viewer import BitmapViewerApp


class TodayOS:
    def __init__(self, width=1280, height=800):
        pygame.init()
        pygame.display.set_caption('TodayOS - Python Desktop Shell')
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Consolas', 18)
        self.apps = {
            'shell': ShellApp(self),
            'notepad': NotepadApp(self),
            'filemanager': FileManagerApp(self),
            'bitmap': BitmapViewerApp(self),
        }
        self.active_app = None
        self.notification = 'Clique nos ícones ou pressione F1..F4 para iniciar apps.'

        self.icon_defs = [
            {'key': 'shell', 'label': 'Shell', 'rect': pygame.Rect(60, 120, 140, 80), 'color': (37, 129, 255)},
            {'key': 'notepad', 'label': 'Notepad', 'rect': pygame.Rect(60, 220, 140, 80), 'color': (255, 205, 44)},
            {'key': 'filemanager', 'label': 'Files', 'rect': pygame.Rect(60, 320, 140, 80), 'color': (62, 191, 80)},
            {'key': 'bitmap', 'label': 'Bitmap', 'rect': pygame.Rect(60, 420, 140, 80), 'color': (208, 67, 208)},
        ]

        self.desktop_background = None
        asset_bg = os.path.join(os.getcwd(), 'assets', 'desktop_bg.png')
        try:
            if not os.path.exists(os.path.dirname(asset_bg)):
                os.makedirs(os.path.dirname(asset_bg), exist_ok=True)
            if not os.path.isfile(asset_bg):
                img = Image.new('RGB', (1280, 800), (24, 88, 170))
                draw = ImageDraw.Draw(img)
                for y in range(0, 800, 4):
                    blend = int(24 + (y/800)*45)
                    draw.line([(0, y), (1280, y)], fill=(blend, 88, 170))
                img.save(asset_bg)

            self.desktop_background = pygame.image.load(asset_bg)
            self.desktop_background = pygame.transform.smoothscale(self.desktop_background, (self.width, self.height))
        except Exception:
            self.desktop_background = None

    def draw_status(self):
        pygame.draw.rect(self.screen, (44, 44, 44), (0, 0, self.width, 26))
        text = self.font.render(self.notification, True, (255, 255, 255))
        self.screen.blit(text, (8, 4))

    def draw_desktop_background(self):
        if self.desktop_background:
            self.screen.blit(self.desktop_background, (0,0))
        else:
            for i in range(0, self.height, 8):
                color = (30 + i // 12, 80 + i // 18, 160 + i // 20)
                pygame.draw.rect(self.screen, color, (0, i, self.width, 8))

    def set_app(self, name):
        if name in self.apps:
            self.active_app = self.apps[name]
            self.active_app.activate()
            self.notification = f'[{name.title()}] Janela aberta. Clique em X ou ESC para fechar.'

    def handle_desktop_click(self, pos):
        for icon in self.icon_defs:
            if icon['rect'].collidepoint(pos):
                self.set_app(icon['key'])
                return

    def check_close_button(self, pos):
        close_rect = pygame.Rect(self.width - 135, 90, 24, 24)
        return close_rect.collidepoint(pos)

    def draw_app_window(self, app):
        # Fundo da janela
        win_rect = pygame.Rect(100, 80, self.width - 200, self.height - 180)
        pygame.draw.rect(self.screen, (240, 240, 245), win_rect)
        pygame.draw.rect(self.screen, (50, 50, 50), win_rect, 2)

        # Barra de título
        title_rect = pygame.Rect(win_rect.x, win_rect.y, win_rect.width, 32)
        pygame.draw.rect(self.screen, (70, 130, 180), title_rect)
        title_text = self.font.render(f'TodayOS - {app.__class__.__name__}', True, (255, 255, 255))
        self.screen.blit(title_text, (title_rect.x + 8, title_rect.y + 6))

        # Botão Fechar
        close_rect = pygame.Rect(win_rect.right - 35, win_rect.y + 4, 24, 24)
        pygame.draw.rect(self.screen, (220, 80, 80), close_rect)
        x_text = self.font.render('X', True, (255, 255, 255))
        self.screen.blit(x_text, (close_rect.x + 5, close_rect.y + 1))

        # Área de conteúdo para o app
        content_surf = self.screen.subsurface(pygame.Rect(win_rect.x + 8, win_rect.y + 40, win_rect.width - 16, win_rect.height - 48))
        content_surf.fill((230, 230, 235))
        app.draw(content_surf)

    def draw_desktop(self):
        # Desenhar ícones de aplicativo na área de trabalho
        for icon in self.icon_defs:
            pygame.draw.rect(self.screen, (255, 255, 255, 150), icon['rect'])
            pygame.draw.rect(self.screen, icon['color'], icon['rect'], 3)
            circle_center = (icon['rect'].x + 24, icon['rect'].y + 24)
            pygame.draw.circle(self.screen, icon['color'], circle_center, 16)
            initial = icon['label'][0].upper()
            initial_render = self.font.render(initial, True, (255, 255, 255))
            self.screen.blit(initial_render, (circle_center[0]-8, circle_center[1]-12))

            label = self.font.render(icon['label'], True, (255, 255, 255))
            text_rect = label.get_rect(center=(icon['rect'].centerx + 10, icon['rect'].centery + 20))
            self.screen.blit(label, text_rect)

        desktop_text = self.font.render('Clique nos ícones para abrir aplicativos', True, (250, 250, 250))
        self.screen.blit(desktop_text, (60, 80))

    def run(self):
        self.active_app = None
        running = True

        while running:
            self.draw_desktop_background()
            self.draw_status()

            for ev in pygame.event.get():
                if ev.type == QUIT:
                    running = False
                elif ev.type == KEYDOWN:
                    if ev.key == K_ESCAPE:
                        if self.active_app:
                            self.active_app = None
                        else:
                            running = False
                    elif ev.key == K_F1:
                        self.set_app('shell')
                    elif ev.key == K_F2:
                        self.set_app('notepad')
                    elif ev.key == K_F3:
                        self.set_app('filemanager')
                    elif ev.key == K_F4:
                        self.set_app('bitmap')
                elif ev.type == MOUSEBUTTONDOWN and ev.button == 1:
                    if self.active_app:
                        if self.check_close_button(ev.pos):
                            self.active_app = None
                            self.notification = 'Retornou para Desktop. Clique em ícones para iniciar apps.'
                        else:
                            self.active_app.handle_event(ev)
                    else:
                        self.handle_desktop_click(ev.pos)

                # Passe outros eventos para app em primeiro plano
                if self.active_app and ev.type not in (MOUSEBUTTONDOWN, MOUSEBUTTONUP):
                    self.active_app.handle_event(ev)

            if self.active_app:
                self.draw_app_window(self.active_app)
            else:
                self.draw_desktop()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def cycle_app(self):
        keys = list(self.apps.keys())
        if self.active_app is None:
            self.set_app(keys[0])
            return
        current = next((k for k, app in self.apps.items() if app == self.active_app), keys[0])
        next_index = (keys.index(current) + 1) % len(keys)
        self.set_app(keys[next_index])

    def draw_welcome(self):
        msg = [
            'TodayOS Python Shell',
            'Este é um ambiente gráfico em cima do Linux.',
            'Use F1..F4 para iniciar apps.',
            'Pressione ESC para sair.',
        ]
        y = 120
        for line in msg:
            label = self.font.render(line, True, (210, 210, 210))
            rect = label.get_rect(center=(self.width // 2, y))
            self.screen.blit(label, rect)
            y += 35

    def execute_command(self, cmd):
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=20)
            return result.stdout + result.stderr
        except Exception as e:
            return str(e)
