# KeyPilot 0.1.0 Release Checklist

## Build

```bash
packaging/deb/build-deb.sh 0.1.0
```

Output:

```text
dist/keypilot_0.1.0_all.deb
```

## Test

```bash
sudo apt install ./dist/keypilot_0.1.0_all.deb
sudo usermod -aG input "$USER"
```

Log out and log back in.

```bash
mkdir -p ~/.config/keypilot
cp /etc/keypilot/config.json ~/.config/keypilot/config.json
systemctl --user daemon-reload
systemctl --user enable --now keypilot
systemctl --user status keypilot
```

Press the Copilot/F23 key and verify that the launcher opens.

## Git

```bash
git add .
git commit -m "Prepare KeyPilot 0.1.0 release"
git tag v0.1.0
git push
git push origin v0.1.0
```

## GitHub Release Notes

Title:

```text
KeyPilot 0.1.0
```

Description:

```text
Initial public release of KeyPilot.

KeyPilot turns the Copilot/F23 key into a customizable launcher on Linux.

Install on Ubuntu/Debian:

sudo apt install ./keypilot_0.1.0_all.deb
sudo usermod -aG input "$USER"

Then log out and log back in, enable the user service, and press the Copilot key.
```

Upload:

```text
dist/keypilot_0.1.0_all.deb
```
