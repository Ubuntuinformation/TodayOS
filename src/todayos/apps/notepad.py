import os
import pygame
from pygame.locals import *

class NotepadApp:
    def __init__(self, os_system):
        self.os_system = os_system
        self.title_font = pygame.font.SysFont('Consolas', 24, bold=True)
        self.lines = ['Bloco de notas iniciado. Digite e pressione Ctrl+S para salvar.']
        self.current_line = ''
        self.file_path = os.path.join(os.getcwd(), 'todayos_note.txt')
        self.loaded_file = None

    def activate(self):
        self.lines = [f'Bloco de notas ativo: {self.file_path} (Ctrl+O abrir, Ctrl+S salvar, Ctrl+N novo)']
        self.current_line = ''
        self.loaded_file = self.file_path

    def draw_logo(self, screen):
        pygame.draw.circle(screen, (255, 181, 0), (50, 50), 22)
        l = self.os_system.font.render('N', True, (20, 20, 20))
        screen.blit(l, (44, 42))

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
            elif e.key == K_o and pygame.key.get_mods() & KMOD_CTRL:
                self.open_dialog()
            elif e.key == K_n and pygame.key.get_mods() & KMOD_CTRL:
                self.new_file()
            else:
                if e.unicode and e.key != K_TAB:
                    self.current_line += e.unicode

    def open_dialog(self):
        path = self.current_line.strip() if self.current_line.strip() else self.file_path
        try:
            if os.path.isfile(path):
                with open(path, 'r', encoding='utf-8', errors='replace') as f:
                    self.lines = f.read().splitlines()
                self.file_path = path
                self.loaded_file = path
                self.lines.append(f'Arquivo aberto: {path}')
            else:
                self.lines.append(f'Arquivo não encontrado: {path}')
        except Exception as e:
            self.lines.append('Erro ao abrir arquivo: ' + str(e))

    def new_file(self):
        self.lines = ['Novo arquivo de bloco de notas. Ctrl+S salvar.']
        self.current_line = ''
        self.file_path = os.path.join(os.getcwd(), 'todayos_note.txt')
        self.loaded_file = None

    def save(self):
        path = self.file_path if self.loaded_file else self.file_path
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(self.lines + [self.current_line]))
            self.lines.append(f'Arquivo salvo: {path}')
            self.loaded_file = path
            self.file_path = path
        except Exception as e:
            self.lines.append('Erro ao salvar: ' + str(e))

    def save(self):
        path = os.path.join(os.getcwd(), 'todayos_note.txt')
        with open(path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.lines + [self.current_line]))
        self.lines.append(f'Arquivo salvo: {path}')

    def draw(self, screen):
        screen.fill((20, 10, 30))
        self.draw_logo(screen)
        header = self.title_font.render('Bloco de Notas', True, (255, 255, 255))
        screen.blit(header, (16, 32))
        y = 70
        for line in self.lines[-22:]:
            label = self.os_system.font.render(line, True, (204, 204, 255))
            screen.blit(label, (16, y))
            y += 22

        input_label = self.os_system.font.render(self.current_line + ('_' if (pygame.time.get_ticks() // 500) % 2 == 0 else ''), True, (255, 255, 255))
        screen.blit(input_label, (16, 690))
