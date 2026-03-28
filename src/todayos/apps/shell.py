import pygame
from pygame.locals import *

class ShellApp:
    def __init__(self, os_system):
        self.os_system = os_system
        self.title_font = pygame.font.SysFont('Consolas', 24, bold=True)
        self.lines = ['Shell iniciado. Digite comando e pressione ENTER.']
        self.input_text = ''

    def activate(self):
        self.lines = ['Shell ativo. Digite comando e pressione ENTER.']
        self.input_text = ''

    def handle_event(self, e):
        if e.type == KEYDOWN:
            if e.key == K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif e.key == K_RETURN:
                if self.input_text.strip():
                    output = self.os_system.execute_command(self.input_text.strip())
                    self.lines.append('$ ' + self.input_text)
                    self.lines.extend(output.splitlines())
                    self.input_text = ''
                    self.lines = self.lines[-25:]
            else:
                if e.unicode and e.key != K_TAB:
                    self.input_text += e.unicode

    def draw(self, screen):
        screen.fill((0, 0, 20))
        header = self.title_font.render('Shell', True, (255, 255, 255))
        screen.blit(header, (16, 32))
        y = 70
        for line in self.lines[-20:]:
            label = self.os_system.font.render(line, True, (180, 230, 180))
            screen.blit(label, (16, y))
            y += 22
        input_label = self.os_system.font.render('> ' + self.input_text, True, (255, 255, 255))
        screen.blit(input_label, (16, 680))
