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

    def draw_logo(self, screen):
        pygame.draw.rect(screen, (32, 176, 255), (45, 35, 24, 24))
        l = self.os_system.font.render('F', True, (255, 255, 255))
        screen.blit(l, (48, 36))

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
                self.open_selected()
            elif e.key in (K_o, K_O):
                self.open_selected()
            elif e.key in (K_DELETE,):
                self.delete_selected()
            elif e.key == K_r and pygame.key.get_mods() & KMOD_CTRL:
                self.rename_selected()

    def get_selected_path(self):
        if not self.entries:
            return None
        entry = self.entries[self.selected]
        if entry == '..':
            return os.path.abspath(os.path.join(self.current_path, '..'))
        return os.path.abspath(os.path.join(self.current_path, entry))

    def open_selected(self):
        target = self.get_selected_path()
        if not target:
            return
        if os.path.isdir(target):
            self.current_path = target
            self.selected = 0
            self.update_entries()
        elif os.path.isfile(target):
            ext = os.path.splitext(target)[1].lower()
            if ext in ['.png', '.jpg', '.jpeg', '.bmp', '.gif']:
                self.os_system.apps['bitmap'].load_image(target)
                self.os_system.set_app('bitmap')
            else:
                try:
                    with open(target, 'r', encoding='utf-8', errors='replace') as f:
                        text = f.read().splitlines()
                    notepad = self.os_system.apps['notepad']
                    notepad.lines = text
                    notepad.file_path = target
                    notepad.loaded_file = target
                    self.os_system.set_app('notepad')
                except Exception as e:
                    self.os_system.notification = f'Falha ao abrir: {e}'

    def delete_selected(self):
        target = self.get_selected_path()
        if not target or not os.path.exists(target):
            return
        try:
            if os.path.isdir(target):
                os.rmdir(target)
                self.os_system.notification = f'Diretório removido: {target}'
            else:
                os.remove(target)
                self.os_system.notification = f'Arquivo removido: {target}'
            self.update_entries()
        except Exception as e:
            self.os_system.notification = f'Erro removendo: {e}'

    def rename_selected(self):
        target = self.get_selected_path()
        if not target:
            return
        newname = os.path.join(self.current_path, f'renamed-{self.entries[self.selected]}')
        try:
            os.rename(target, newname)
            self.os_system.notification = f'Renamed to {newname}'
            self.update_entries()
        except Exception as e:
            self.os_system.notification = f'Erro rename: {e}'

    def draw(self, screen):
        screen.fill((10, 25, 35))
        self.draw_logo(screen)
        header = self.title_font.render(f'Gerenciador de Arquivos: {self.current_path}', True, (255, 255, 255))
        screen.blit(header, (16, 32))
        y = 70
        for i, entry in enumerate(self.entries[:25]):
            color = (130, 220, 180) if i == self.selected else (190, 220, 250)
            label = self.os_system.font.render(entry, True, color)
            screen.blit(label, (24, y))
            y += 22
