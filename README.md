# TodayOS

Projeto de demonstração de ambiente gráfico pseudo-OS em Python sobre Linux.

## Como usar

1. Instale dependências do sistema (Ubuntu/Debian):

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip libgl1-mesa-dev libgles2-mesa-dev
```

2. Rodar bootstrap (cria venv e instala pacotes):

```bash
chmod +x scripts/bootstrap.sh
./scripts/bootstrap.sh
```

3. Ative o virtualenv:

```bash
source .venv/bin/activate
```

4. Execute:

```bash
python main.py
```

## Atalhos

- F1: Shell
- F2: Bloco de notas
- F3: Gerenciador de arquivos
- F4: Visualizador de imagens
- ESC: Sair
- TAB: alterna entre apps abertos

## O que este projeto implementa

- Loop principal para captura de eventos teclado/mouse via `pygame`.
- Shell de comandos rodando `subprocess` e exibindo saída.
- Bloco de notas simples com `Ctrl+S` para salvar em `todayos_note.txt`.
- Gerenciador de arquivos navegável (`UP/DOWN`, `ENTER` abre diretório ou imagem).
- Visualizador de bitmap via `Pillow` + `pygame`.

## Kernel Linux custom (experimental)

1. Baixe e compile o kernel:

```bash
chmod +x scripts/build_and_install_kernel.sh
./scripts/build_and_install_kernel.sh
```

2. Reinicie e, se necessário, selecione o novo kernel no GRUB.
3. No boot, execute o TodayOS:

```bash
cd /workspaces/TodayOS
source .venv/bin/activate
python main.py
```

## Autostart TodayOS no usuário

```bash
chmod +x scripts/setup_todayos_autostart.sh
./scripts/setup_todayos_autostart.sh
```

Esse script cria e habilita o serviço `todayos.service` no systemd de usuário (requere sessão gráfica existente).
