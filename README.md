# Argentum - Competencias de Rap

Proyecto Kivy para Android basado en `main.py`.

## Generar APK en PC Linux/WSL

```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip python3-venv
python3 -m pip install --upgrade pip
python3 -m pip install buildozer cython==0.29.37
buildozer -v android debug
```

El APK aparecerá en `bin/`.

## Generación automática con GitHub Actions

Sube esta carpeta a un repositorio de GitHub. El workflow `.github/workflows/build-apk.yml` puede ejecutarse desde **Actions > Build Argentum APK > Run workflow**. Al terminar, descarga el artefacto `argentum-apk`.

Nota: la primera compilación de Kivy para Android puede tardar bastante porque descarga el SDK/NDK y compila dependencias.
