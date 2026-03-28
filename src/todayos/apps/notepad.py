import os
import pygame
from pygame.locals import *

class NotepadApp:
    def __init__(self, os_system):
        self.os_system = os_system
        self.title_font = pygame.font.SysFont('Consolas', 24, bold=True)
        self.lines = ['Bloco de notas iniciado. Digite e pressione Ctrl+S para salvar.']
        self.current_line = ''
        self.file_path = None

    def activate(self):
        self.lines = ['Edite este texto. Ctrl+S para salvar em ./todayos_note.txt']
        self.current_line = ''

    def handle_event(self, e):
        if e.type == KEYDOWN:
            if e.key == K_BACKSPACE:
                self.current_line = self.current_line[:-1]
            elif e.key == K_RETURN:
                self.lines.append(self.current_line)
                self.current_line = ''
            elif e.key == K_s and pygame.key.get_mods() & KMOD_CTRL:
                self.save()
            else:
                if e.unicode and e.key != K_TAB:
                    self.current_line += e.unicode

    def save(self):
        path = os.path.join(os.getcwd(), 'todayos_note.txt')
        with open(path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.lines + [self.current_line]))
        self.lines.append(f'Arquivo salvo: {path}')

    def draw(self, screen):
        screen.fill((20, 10, 30))
        header = self.title_font.render('Bloco de Notas', True, (255, 255, 255))
        screen.blit(header, (16, 32))
        y = 70
        for line in self.lines[-22:]:
            label = self.os_system.font.render(line, True, (204, 204, 255))
            screen.blit(label, (16, y))
            y += 22

        input_label = self.os_system.font.render(self.current_line + '|', True, (255, 255, 255))
        screen.blit(input_label, (16, 690))
