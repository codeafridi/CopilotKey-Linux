#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
VERSION="${1:-0.1.0}"
ARCH="${ARCH:-all}"
PACKAGE="keypilot"
BUILD_DIR="$ROOT_DIR/build/${PACKAGE}_${VERSION}_${ARCH}"
DEB_PATH="$ROOT_DIR/dist/${PACKAGE}_${VERSION}_${ARCH}.deb"

rm -rf "$BUILD_DIR"
mkdir -p \
    "$BUILD_DIR/DEBIAN" \
    "$BUILD_DIR/usr/bin" \
    "$BUILD_DIR/usr/lib/systemd/user" \
    "$BUILD_DIR/etc/keypilot" \
    "$BUILD_DIR/usr/share/doc/keypilot"

install -m 0755 "$ROOT_DIR/keypilot.py" "$BUILD_DIR/usr/bin/keypilot"
install -m 0644 "$ROOT_DIR/packaging/deb/keypilot.service" "$BUILD_DIR/usr/lib/systemd/user/keypilot.service"
install -m 0644 "$ROOT_DIR/config.example.json" "$BUILD_DIR/etc/keypilot/config.json"
install -m 0644 "$ROOT_DIR/README.md" "$BUILD_DIR/usr/share/doc/keypilot/README.md"
install -m 0644 "$ROOT_DIR/LICENSE" "$BUILD_DIR/usr/share/doc/keypilot/copyright"
install -m 0755 "$ROOT_DIR/packaging/deb/postinst" "$BUILD_DIR/DEBIAN/postinst"
install -m 0755 "$ROOT_DIR/packaging/deb/prerm" "$BUILD_DIR/DEBIAN/prerm"

cat > "$BUILD_DIR/DEBIAN/control" <<CONTROL
Package: keypilot
Version: $VERSION
Section: utils
Priority: optional
Architecture: $ARCH
Maintainer: Afridi <codeafridi@users.noreply.github.com>
Depends: python3, python3-evdev, xdg-utils, rofi-wayland | wofi | fuzzel | rofi
Homepage: https://github.com/codeafridi/CopilotKey-Linux
Description: Turn the Copilot key into a customizable Linux launcher
 KeyPilot listens for the Copilot/F23 key and opens a configurable launcher
 menu for apps, websites, files, and system actions.
CONTROL

mkdir -p "$ROOT_DIR/dist"
dpkg-deb --root-owner-group --build "$BUILD_DIR" "$DEB_PATH"
echo "Built $DEB_PATH"
