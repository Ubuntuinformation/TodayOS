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
    TASKBAR_HEIGHT = 40

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
        self.start_menu_open = False

        self.icon_defs = [
            {'key': 'shell', 'label': 'Shell', 'rect': pygame.Rect(60, 120, 140, 80), 'color': (37, 129, 255)},
            {'key': 'notepad', 'label': 'Notepad', 'rect': pygame.Rect(60, 220, 140, 80), 'color': (255, 205, 44)},
            {'key': 'filemanager', 'label': 'Files', 'rect': pygame.Rect(60, 320, 140, 80), 'color': (62, 191, 80)},
            {'key': 'bitmap', 'label': 'Bitmap', 'rect': pygame.Rect(60, 420, 140, 80), 'color': (208, 67, 208)},
        ]

        self.desktop_windows = {}
        x0, y0 = 160, 130
        w, h = 900, 550
        for i, app_name in enumerate(self.apps.keys()):
            self.desktop_windows[app_name] = {
                'app': self.apps[app_name],
                'rect': pygame.Rect(x0 + i * 40, y0 + i * 30, w, h),
                'dragging': False,
                'drag_offset': (0, 0),
                'minimized': True,
                'z': i,
            }

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
            window = self.desktop_windows[name]
            window['minimized'] = False
            self.active_app = window
            self.active_app['app'].activate()
            self.active_app['z'] = max(w['z'] for w in self.desktop_windows.values()) + 1
            self.notification = f'[{name.title()}] Janela aberta. Clique em X ou ESC para fechar.'
            self.start_menu_open = False

    def handle_desktop_click(self, pos):
        for icon in self.icon_defs:
            if icon['rect'].collidepoint(pos):
                self.set_app(icon['key'])
                return

    def handle_taskbar_click(self, pos):
        if pos[1] >= self.height - self.TASKBAR_HEIGHT:
            start_rect = pygame.Rect(0, self.height - self.TASKBAR_HEIGHT, 100, self.TASKBAR_HEIGHT)
            if start_rect.collidepoint(pos):
                self.start_menu_open = not self.start_menu_open
                return

            x = 110
            for name, window in self.desktop_windows.items():
                btn_rect = pygame.Rect(x, self.height - self.TASKBAR_HEIGHT + 6, 90, 28)
                if btn_rect.collidepoint(pos):
                    window['minimized'] = False
                    self.set_app(name)
                    return
                x += 100

    def get_window_at_point(self, pos):
        windows = sorted(self.desktop_windows.items(), key=lambda x: x[1]['z'], reverse=True)
        for name, win in windows:
            if win['rect'].collidepoint(pos) and not win['minimized']:
                return name, win
        return None, None

    def check_close_button(self, pos):
        close_rect = pygame.Rect(self.width - 135, 90, 24, 24)
        return close_rect.collidepoint(pos)

    def draw_app_window(self, name, window):
        app = window['app']
        win_rect = window['rect']

        pygame.draw.rect(self.screen, (240, 240, 245), win_rect)
        pygame.draw.rect(self.screen, (50, 50, 50), win_rect, 2)

        title_rect = pygame.Rect(win_rect.x, win_rect.y, win_rect.width, 32)
        pygame.draw.rect(self.screen, (70, 130, 180), title_rect)
        title_text = self.font.render(f'{name.title()} - TodayOS', True, (255, 255, 255))
        self.screen.blit(title_text, (title_rect.x + 8, title_rect.y + 6))

        close_rect = pygame.Rect(win_rect.right - 35, win_rect.y + 4, 24, 24)
        pygame.draw.rect(self.screen, (220, 80, 80), close_rect)
        x_text = self.font.render('X', True, (255, 255, 255))
        self.screen.blit(x_text, (close_rect.x + 5, close_rect.y + 1))

        mini_rect = pygame.Rect(win_rect.right - 70, win_rect.y + 4, 24, 24)
        pygame.draw.rect(self.screen, (200, 180, 0), mini_rect)
        m_text = self.font.render('-', True, (255, 255, 255))
        self.screen.blit(m_text, (mini_rect.x + 7, mini_rect.y + 1))

        content_rect = pygame.Rect(win_rect.x + 8, win_rect.y + 40, win_rect.width - 16, win_rect.height - 48)
        content_surf = self.screen.subsurface(content_rect)
        content_surf.fill((230, 230, 235))
        app.draw(content_surf)

        window['close_rect'] = close_rect
        window['mini_rect'] = mini_rect
        window['title_bar'] = title_rect
        window['content_rect'] = content_rect

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

    def draw_taskbar(self):
        pygame.draw.rect(self.screen, (20, 20, 20), (0, self.height - self.TASKBAR_HEIGHT, self.width, self.TASKBAR_HEIGHT))
        pygame.draw.rect(self.screen, (150, 150, 150), (0, self.height - self.TASKBAR_HEIGHT, self.width, 1))
        start_text = self.font.render('Iniciar', True, (255, 255, 255))
        self.screen.blit(start_text, (10, self.height - self.TASKBAR_HEIGHT + 10))

        x = 110
        for name, window in self.desktop_windows.items():
            btn_rect = pygame.Rect(x, self.height - self.TASKBAR_HEIGHT + 6, 90, 28)
            pygame.draw.rect(self.screen, (80, 80, 80), btn_rect)
            pygame.draw.rect(self.screen, (150, 150, 150), btn_rect, 1)
            label = self.font.render(name.title(), True, (255, 255, 255))
            label_rect = label.get_rect(center=btn_rect.center)
            self.screen.blit(label, label_rect)
            x += 100

    def draw_start_menu(self):
        menu_rect = pygame.Rect(0, self.height - self.TASKBAR_HEIGHT - 200, 220, 200)
        pygame.draw.rect(self.screen, (30, 30, 30), menu_rect)
        pygame.draw.rect(self.screen, (200, 200, 200), menu_rect, 1)
        y = menu_rect.y + 16

        self.screen.blit(self.font.render('Menu Iniciar', True, (255, 255, 255)), (menu_rect.x + 16, y))
        y += 30

        for icon in self.icon_defs:
            item = pygame.Rect(menu_rect.x + 10, y, menu_rect.width - 20, 28)
            pygame.draw.rect(self.screen, (40, 40, 40), item)
            pygame.draw.rect(self.screen, (120, 120, 120), item, 1)
            label = self.font.render(icon['label'], True, (255, 255, 255))
            self.screen.blit(label, (item.x + 8, item.y + 4))
            y += 34

    def draw_windows(self):
        windows = sorted(self.desktop_windows.items(), key=lambda x: x[1]['z'])
        for name, window in windows:
            if window['minimized']:
                continue
            self.draw_app_window(name, window)

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
                    elif ev.key == K_SPACE:
                        self.start_menu_open = not self.start_menu_open
                elif ev.type == MOUSEBUTTONDOWN and ev.button == 1:
                    if ev.pos[1] >= self.height - self.TASKBAR_HEIGHT:
                        self.handle_taskbar_click(ev.pos)
                        continue

                    if self.start_menu_open and ev.pos[1] >= self.height - self.TASKBAR_HEIGHT - 200:
                        self.handle_start_menu_click(ev.pos)
                        continue

                    name, window = self.get_window_at_point(ev.pos)
                    if name:
                        if window['close_rect'].collidepoint(ev.pos):
                            window['minimized'] = True
                            self.notification = f'{name.title()} minimizado no taskbar.'
                            if self.active_app == window:
                                self.active_app = None
                            continue
                        if window['mini_rect'].collidepoint(ev.pos):
                            window['minimized'] = True
                            self.notification = f'{name.title()} minimizado no taskbar.'
                            if self.active_app == window:
                                self.active_app = None
                            continue
                        if window['title_bar'].collidepoint(ev.pos):
                            window['dragging'] = True
                            window['drag_offset'] = (ev.pos[0] - window['rect'].x, ev.pos[1] - window['rect'].y)
                            self.active_app = window
                            window['z'] = max(w['z'] for w in self.desktop_windows.values()) + 1
                            continue

                    if self.active_app and self.active_app['content_rect'].collidepoint(ev.pos):
                        rel = (ev.pos[0] - self.active_app['content_rect'].x, ev.pos[1] - self.active_app['content_rect'].y)
                        ev_copy = pygame.event.Event(ev.type, {'pos': rel, 'button': ev.button})
                        self.active_app['app'].handle_event(ev_copy)
                        continue

                    self.handle_desktop_click(ev.pos)
                elif ev.type == MOUSEBUTTONUP and ev.button == 1:
                    for window in self.desktop_windows.values():
                        window['dragging'] = False
                elif ev.type == MOUSEMOTION:
                    for window in self.desktop_windows.values():
                        if window.get('dragging'):
                            dx, dy = window['drag_offset']
                            window['rect'].x = ev.pos[0] - dx
                            window['rect'].y = ev.pos[1] - dy

                if self.active_app and ev.type not in (MOUSEBUTTONDOWN, MOUSEBUTTONUP):
                    self.active_app['app'].handle_event(ev)

            if self.active_app:
                self.draw_windows()
            else:
                self.draw_desktop()

            self.draw_taskbar()
            if self.start_menu_open:
                self.draw_start_menu()

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
            'Use o menu Iniciar / taskbar para abrir apps.',
            'Pressione ESC para sair.',
        ]
        y = 160
        for line in msg:
            label = self.font.render(line, True, (210, 210, 210))
            rect = label.get_rect(center=(self.width // 2, y))
            self.screen.blit(label, rect)
            y += 35

    def handle_start_menu_click(self, pos):
        menu_rect = pygame.Rect(0, self.height - self.TASKBAR_HEIGHT - 200, 220, 200)
        if not menu_rect.collidepoint(pos):
            self.start_menu_open = False
            return

        y = menu_rect.y + 46
        for icon in self.icon_defs:
            item = pygame.Rect(menu_rect.x + 10, y, menu_rect.width - 20, 28)
            if item.collidepoint(pos):
                self.set_app(icon['key'])
                self.start_menu_open = False
                return
            y += 34

    def execute_command(self, cmd):
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=20)
            return result.stdout + result.stderr
        except Exception as e:
            return str(e)

    def execute_command(self, cmd):
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=20)
            return result.stdout + result.stderr
        except Exception as e:
            return str(e)
