import os
import pygame
from pygame.locals import *

class FileManagerApp:
    def __init__(self, os_system):
        self.os_system = os_system
        self.current_path = os.getcwd()
        self.selected = 0
        self.entries = []
        self.title_font = pygame.font.SysFont('Consolas', 24, bold=True)
        self.update_entries()

    def activate(self):
        self.current_path = os.getcwd()
        self.selected = 0
        self.update_entries()

    def update_entries(self):
        try:
            all_names = sorted(os.listdir(self.current_path), key=lambda x: (not os.path.isdir(os.path.join(self.current_path, x)), x.lower()))
            self.entries = ['..'] + all_names
        except Exception as e:
            self.entries = ['..']
            print('Error reading folder:', e)

    def handle_event(self, e):
        if e.type == KEYDOWN:
            if e.key == K_DOWN:
                self.selected = min(self.selected + 1, max(0, len(self.entries) - 1))
            elif e.key == K_UP:
                self.selected = max(0, self.selected - 1)
            elif e.key in (K_RETURN, K_RIGHT):
                entry = self.entries[self.selected]
                target = os.path.abspath(os.path.join(self.current_path, entry))
                if entry == '..':
                    target = os.path.abspath(os.path.join(self.current_path, '..'))
                if os.path.isdir(target):
                    self.current_path = target
                    self.selected = 0
                    self.update_entries()
                else:
                    self.os_system.apps['bitmap'].load_image(target)
                    self.os_system.set_app('bitmap')

    def draw(self, screen):
        screen.fill((10, 25, 35))
        header = self.title_font.render(f'Gerenciador de Arquivos: {self.current_path}', True, (255, 255, 255))
        screen.blit(header, (16, 32))
        y = 70
        for i, entry in enumerate(self.entries[:25]):
            color = (130, 220, 180) if i == self.selected else (190, 220, 250)
            label = self.os_system.font.render(entry, True, color)
            screen.blit(label, (24, y))
            y += 22
