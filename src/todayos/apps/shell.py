import os
import shlex
import pygame
from pygame.locals import *

class ShellApp:
    def __init__(self, os_system):
        self.os_system = os_system
        self.title_font = pygame.font.SysFont('Consolas', 24, bold=True)
        self.header_font = pygame.font.SysFont('Consolas', 20, bold=True)
        self.lines = ['Shell iniciado. Digite comando e pressione ENTER.']
        self.input_text = ''
        self.history = []
        self.history_index = -1
        self.cwd = os.getcwd()

    def activate(self):
        self.lines = [f'Shell ativo em {self.cwd}. Comandos: help, ls, cd, pwd, cat, echo, clear, exit']
        self.input_text = ''
        self.history_index = len(self.history)

    def handle_event(self, e):
        if e.type == KEYDOWN:
            if e.key == K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif e.key == K_RETURN:
                cmd = self.input_text.strip()
                if cmd:
                    self.history.append(cmd)
                    self.history_index = len(self.history)
                    self.process_command(cmd)
                self.input_text = ''
            elif e.key == K_UP and self.history:
                self.history_index = max(0, self.history_index - 1)
                self.input_text = self.history[self.history_index]
            elif e.key == K_DOWN and self.history:
                self.history_index = min(len(self.history) - 1, self.history_index + 1)
                self.input_text = self.history[self.history_index] if self.history_index < len(self.history) else ''
            elif e.key == K_TAB:
                # simples autocomplete de comandos locais
                cmds = ['help', 'ls', 'cd', 'pwd', 'cat', 'echo', 'clear', 'exit', 'mkdir', 'rm', 'rmdir']
                prefix = self.input_text.strip()
                matches = [c for c in cmds if c.startswith(prefix)]
                if len(matches) == 1:
                    self.input_text = matches[0] + ' '
            elif e.key == K_LCTRL or e.key == K_RCTRL:
                pass
            elif e.unicode and e.key != K_TAB:
                self.input_text += e.unicode

    def run_external(self, cmd):
        try:
            output = self.os_system.execute_command(cmd, cwd=self.cwd)
            if output:
                self.lines.extend(output.splitlines())
            else:
                self.lines.append('(sem saída)')
        except Exception as ex:
            self.lines.append('erro ao executar: ' + str(ex))

    def process_command(self, cmd):
        self.lines.append('$ ' + cmd)
        parts = shlex.split(cmd)
        if not parts:
            return

        cmd0 = parts[0]
        args = parts[1:]

        try:
            if cmd0 == 'help':
                self.lines.extend([
                    'Comandos internos: help, ls, cd, pwd, cat, echo, clear, exit, mkdir, rm, rmdir',
                    'Comando externo é permitido via shell.'
                ])
            elif cmd0 == 'clear':
                self.lines = []
            elif cmd0 == 'pwd':
                self.lines.append(self.cwd)
            elif cmd0 == 'cd':
                target = args[0] if args else os.path.expanduser('~')
                new = os.path.abspath(os.path.join(self.cwd, target))
                if os.path.isdir(new):
                    self.cwd = new
                    os.chdir(new)
                    self.lines.append('Diretório: ' + self.cwd)
                else:
                    self.lines.append('cd: diretorio não encontrado: ' + target)
            elif cmd0 == 'ls':
                path = self.cwd if not args else os.path.abspath(os.path.join(self.cwd, args[0]))
                if os.path.isdir(path):
                    entries = sorted(os.listdir(path))
                    self.lines.extend(entries)
                else:
                    self.lines.append('ls: não é diretório: ' + path)
            elif cmd0 == 'cat':
                if not args:
                    self.lines.append('cat: forneça arquivo')
                for filename in args:
                    path = os.path.abspath(os.path.join(self.cwd, filename))
                    if os.path.isfile(path):
                        with open(path, 'r', encoding='utf-8', errors='replace') as f:
                            self.lines.extend(f.read().splitlines())
                    else:
                        self.lines.append('cat: arquivo não encontrado: ' + filename)
            elif cmd0 == 'echo':
                self.lines.append(' '.join(args))
            elif cmd0 == 'exit':
                self.os_system.active_app = None
                self.lines.append('Fechando shell...')
            elif cmd0 == 'mkdir':
                if not args:
                    self.lines.append('mkdir: nome do diretório necessário')
                else:
                    for d in args:
                        path = os.path.abspath(os.path.join(self.cwd, d))
                        os.makedirs(path, exist_ok=True)
                        self.lines.append('diretório criado: ' + path)
            elif cmd0 == 'rmdir':
                if not args:
                    self.lines.append('rmdir: nome do diretório necessário')
                else:
                    for d in args:
                        path = os.path.abspath(os.path.join(self.cwd, d))
                        if os.path.isdir(path):
                            os.rmdir(path)
                            self.lines.append('diretório removido: ' + path)
                        else:
                            self.lines.append('rmdir: não é diretório: ' + d)
            elif cmd0 == 'rm':
                if not args:
                    self.lines.append('rm: nome do arquivo necessário')
                else:
                    for f in args:
                        path = os.path.abspath(os.path.join(self.cwd, f))
                        if os.path.isfile(path):
                            os.remove(path)
                            self.lines.append('arquivo removido: ' + path)
                        else:
                            self.lines.append('rm: arquivo não encontrado: ' + f)
            else:
                self.run_external(cmd)
        except Exception as ex:
            self.lines.append('Erro: ' + str(ex))

        self.lines = self.lines[-40:]

    def process_command(self, cmd):
        self.lines.append('$ ' + cmd)
        parts = shlex.split(cmd)
        if not parts:
            return

        cmd0 = parts[0]
        args = parts[1:]

        try:
            if cmd0 == 'help':
                self.lines.extend([
                    'Comandos internos: help, ls, cd, pwd, cat, echo, clear, exit',
                    'Também aceita comandos do shell sistema (exec com setas).'
                ])
            elif cmd0 == 'clear':
                self.lines = []
            elif cmd0 == 'pwd':
                self.lines.append(self.cwd)
            elif cmd0 == 'cd':
                target = args[0] if args else os.path.expanduser('~')
                new = os.path.abspath(os.path.join(self.cwd, target))
                if os.path.isdir(new):
                    self.cwd = new
                    os.chdir(new)
                    self.lines.append('Diretório: ' + self.cwd)
                else:
                    self.lines.append('cd: diretorio não encontrado: ' + target)
            elif cmd0 == 'ls':
                path = self.cwd if not args else os.path.abspath(os.path.join(self.cwd, args[0]))
                if os.path.isdir(path):
                    entries = os.listdir(path)
                    self.lines.extend(entries)
                else:
                    self.lines.append('ls: não é diretório: ' + path)
            elif cmd0 == 'cat':
                for filename in args:
                    path = os.path.abspath(os.path.join(self.cwd, filename))
                    if os.path.isfile(path):
                        with open(path, 'r', encoding='utf-8', errors='replace') as f:
                            self.lines.extend(f.read().splitlines())
                    else:
                        self.lines.append('cat: arquivo não encontrado: ' + filename)
            elif cmd0 == 'echo':
                self.lines.append(' '.join(args))
            elif cmd0 == 'exit':
                self.os_system.active_app = None
                self.lines.append('Fechando shell...')
            else:
                output = self.os_system.execute_command(cmd)
                self.lines.extend(output.splitlines())
        except Exception as ex:
            self.lines.append('Erro: ' + str(ex))

        self.lines = self.lines[-30:]

    def draw(self, screen):
        screen.fill((20, 20, 30))
        header = self.title_font.render('TodayOS Shell', True, (255, 255, 255))
        screen.blit(header, (16, 16))

        logo = self.header_font.render('🖥️', True, (255, 200, 0))
        screen.blit(logo, (screen.get_width() - 60, 16))

        y = 56
        for line in self.lines[-20:]:
            label = self.os_system.font.render(line, True, (200, 230, 180))
            screen.blit(label, (16, y))
            y += 22

        input_label = self.os_system.font.render('> ' + self.input_text + ('_' if (pygame.time.get_ticks() // 500) % 2 == 0 else ''), True, (255, 255, 255))
        screen.blit(input_label, (16, screen.get_height() - 40))
