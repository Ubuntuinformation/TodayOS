import os
import subprocess
import pygame
from pygame.locals import *
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
        self.notification = 'F1 Shell | F2 Notepad | F3 File Manager | F4 Bitmap Viewer | ESC Sair'

    def draw_status(self):
        pygame.draw.rect(self.screen, (44, 44, 44), (0, 0, self.width, 26))
        text = self.font.render(self.notification, True, (255, 255, 255))
        self.screen.blit(text, (8, 4))

    def set_app(self, name):
        if name in self.apps:
            self.active_app = self.apps[name]
            self.active_app.activate()
            self.notification = f'[{name.title()}] Alt+Tab para trocar. F1-F4 aplicação rápida. ESC para sair.'

    def run(self):
        self.active_app = None
        running = True
        while running:
            self.screen.fill((20, 20, 20))
            self.draw_status()
            for ev in pygame.event.get():
                if ev.type == QUIT:
                    running = False
                elif ev.type == KEYDOWN:
                    if ev.key == K_ESCAPE:
                        running = False
                    elif ev.key == K_F1:
                        self.set_app('shell')
                    elif ev.key == K_F2:
                        self.set_app('notepad')
                    elif ev.key == K_F3:
                        self.set_app('filemanager')
                    elif ev.key == K_F4:
                        self.set_app('bitmap')
                    elif ev.key == K_TAB and self.active_app:
                        self.cycle_app()
                if self.active_app:
                    self.active_app.handle_event(ev)

            if self.active_app:
                self.active_app.draw(self.screen)
            else:
                self.draw_welcome()

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
