#!/usr/bin/env bash
set -euo pipefail

# ATENÇÃO: precisa de reboot manual e acesso root. Não execute em produção sem testar.
# Recomendado: rodar em máquina virtual (VM) ou container com suporte a KVM.

DEFAULT_KERNEL_VERSION="6.7.21"
KERNEL_VERSION="${KERNEL_VERSION:-$DEFAULT_KERNEL_VERSION}"
KERNEL_TARBALL="linux-$KERNEL_VERSION.tar.xz"
KERNEL_URL="https://cdn.kernel.org/pub/linux/kernel/v6.x/$KERNEL_TARBALL"
SRC_DIR="/tmp/linux-$KERNEL_VERSION"

find_latest_kernel() {
  >&2 echo "Tentando detectar última versão estável disponível em cdn.kernel.org..."
  latest=$(wget -qO- https://cdn.kernel.org/pub/linux/kernel/v6.x/ | grep -Po 'linux-6\.[0-9]+\.[0-9]+\.tar\.xz' | sort -V | tail -n1)
  if [ -n "$latest" ]; then
    latest_version=${latest#linux-}
    latest_version=${latest_version%.tar.xz}
    >&2 echo "Versão detectada: $latest_version"
    printf '%s' "$latest_version"
  else
    >&2 echo "Nenhuma versão detectada"
    return 1
  fi
}

download_kernel() {
  KERNEL_TARBALL="linux-$KERNEL_VERSION.tar.xz"
  KERNEL_URL="https://cdn.kernel.org/pub/linux/kernel/v6.x/$KERNEL_TARBALL"
  echo "Baixando e extraindo fontes do kernel $KERNEL_VERSION"
  cd /tmp
  if [ ! -f "$KERNEL_TARBALL" ]; then
    wget --no-check-certificate --tries=3 --timeout=20 "$KERNEL_URL"
  fi
}

echo "1) Iniciando processo de instalação do kernel ($KERNEL_VERSION)"
cd /tmp
if ! download_kernel; then
  echo "Falha no download do kernel $KERNEL_VERSION. Tentando detectar versão mais recente..."
  latest_ver=$(find_latest_kernel)
  if [ -n "$latest_ver" ]; then
    KERNEL_VERSION="$latest_ver"
    SRC_DIR="/tmp/linux-$KERNEL_VERSION"
    download_kernel
  else
    echo "Não foi possível detectar e baixar versão de kernel válida. Abortando."
    exit 1
  fi
fi

rm -rf "$SRC_DIR"
tar xf "/tmp/linux-$KERNEL_VERSION.tar.xz"

echo "2) Configurando kernel (copiando config do sistema atual ou fallback defconfig)"
cd "$SRC_DIR"
if [ -f "/boot/config-$(uname -r)" ]; then
  cp "/boot/config-$(uname -r)" .config
  make olddefconfig
else
  echo "A config de /boot não foi encontrada. Usando make defconfig."
  make defconfig
fi

echo "3) Compilando kernel e módulos (pode demorar)"
make -j"$(nproc)"

if [ -d "/boot" ] && [ -w "/boot" ]; then
  echo "4) Instalando kernel no /boot (requere sudo)"
  make modules_install
  sudo make install
  echo "5) Atualizando GRUB"
  sudo update-grub
  INSTALLED_ON_SYSTEM=1
else
  echo "4) /boot não disponível ou sem permissão - instalando em modo local /tmp"
  DESTDIR="/tmp/linux-$KERNEL_VERSION-install"
  mkdir -p "$DESTDIR/boot"
  make INSTALL_PATH="$DESTDIR" modules_install || true
  cp -v arch/$(uname -m)/boot/bzImage "$DESTDIR/boot/vmlinuz-$KERNEL_VERSION" || true
  INSTALLED_ON_SYSTEM=0
fi

cat <<EOF

Kernel $KERNEL_VERSION compilado.
EOF

if [ "$INSTALLED_ON_SYSTEM" -eq 1 ]; then
  cat <<EOF
Kernel instalado no sistema. Reinicie o sistema e selecione o kernel no GRUB.
EOF
else
  cat <<EOF
Kernel instalado em modo local em $DESTDIR (sem reboot automático):
 - kernel: $DESTDIR/boot/vmlinuz-$KERNEL_VERSION
 - módulos: $DESTDIR/lib/modules/$KERNEL_VERSION
Use este kernel em QEMU ou outro ambiente manualmente.
EOF
fi

cat <<EOF

Kernel $KERNEL_VERSION instalado.
Reinicie o sistema e selecione o kernel novo no GRUB (se não for padrão).
Depois, rode ./scripts/bootstrap.sh e execute python main.py no ambiente gráfico.
EOF
