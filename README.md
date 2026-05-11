# 🌌 VaroASCII: El Motor Definitivo de Arte ASCII y Efectos Visuales para Terminal

¡Bienvenido a **VaroASCII**! Esta es una versión mejorada y personalizada de `terminaltexteffects`, diseñada para ser una herramienta "todo en uno" que combina la potencia de los efectos visuales animados con la generación de arte ASCII profesional.

> [!IMPORTANT]
> **PROYECTO PRIVADO**: Este repositorio es de uso personal y para desarrollo específico de VaroTv7.

---

## ✨ Características Principales

*   **Generador ASCII Integrado**: Convierte cualquier texto en arte ASCII usando fuentes FIGlet (incluyendo la exclusiva *Delta Corps Priest 1*).
*   **Biblioteca de Efectos**: Más de 30 efectos visuales (lluvia, matriz, fuegos artificiales, desintegración, etc.).
*   **Colores RGB/Xterm**: Soporte completo para colores de 24 bits y paletas de 256 colores.
*   **Altamente Personalizable**: Control total sobre la velocidad, gradientes, direcciones y comportamientos de los efectos.
*   **Todo en Uno**: Genera el arte ASCII y anímalo en un solo comando.

---

## 🚀 Instalación

VaroASCII es multiplataforma y funciona en Windows y Linux.

### 1. Sin Docker (Local)

#### Requisitos
*   Python 3.8 o superior.
*   `pip` o `uv` (recomendado).

#### Instalación rápida
Clona el repositorio e instala en modo editable:

```bash
git clone https://github.com/VaroTv7/varoascii.git
cd varoascii
pip install .
```

O usando `uv`:
```bash
uv pip install .
```

### 2. Con Docker

Si prefieres no instalar Python localmente, puedes usar Docker.

#### Construir la imagen
```bash
docker build -t varoascii .
```

#### Ejecutar
```bash
echo "Varo" | docker run -i varoascii ascii --font slant | docker run -i varoascii rain
```

---

## 🛠️ Uso y Ejemplos

VaroASCII se puede usar como aplicación de consola o como librería de Python.

### Comandos Básicos

Generar arte ASCII con un efecto de lluvia:
```bash
echo "VaroASCII" | varoascii ascii --font slant | varoascii rain
```

Efecto de descompresión (decrypt):
```bash
echo "ACCESO DENEGADO" | varoascii decrypt --typing-speed 2
```

Lanzar un efecto aleatorio:
```bash
echo "Sorpresa" | varoascii -R
```

### El nuevo comando `ascii`
Hemos añadido un comando específico para generar arte ASCII antes de animarlo:
*   `--font`: Especifica la fuente FIGlet (ej: `slant`, `standard`, `block`, `Delta Corps Priest 1`).
*   `--list-fonts`: Muestra todas las fuentes disponibles.

---

## 🪟 Guía Específica para Windows

En Windows, se recomienda usar **Windows Terminal** o **PowerShell 7** para una mejor representación de los colores ANSI.

1.  Asegúrate de tener Python instalado (`python --version`).
2.  Si usas PowerShell, puedes usar tuberías igual que en Linux:
    ```powershell
    "Hola Varo" | varoascii ascii --font block | varoascii matrix
    ```

---

## 🐧 Guía Específica para Linux

VaroASCII funciona perfectamente en cualquier emulador de terminal moderno (GNOME Terminal, Alacritty, Kitty, etc.).

1.  Instala las dependencias: `pip install .`
2.  Añade el binario a tu PATH si es necesario.
3.  ¡Disfruta de los efectos en tus scripts de automatización!

---

## 📂 Estructura del Proyecto

*   `varoascii/`: Código fuente principal.
*   `varoascii/effects/`: Directorio con todos los módulos de efectos.
*   `varoascii/fonts/`: Fuentes ASCII personalizadas.
*   `Dockerfile`: Configuración para contenedores.

---

## 📜 Licencia

Distribuido bajo la Licencia MIT. Consulta el archivo `LICENSE` para más información.

---

**Desarrollado con ❤️ por VaroTv7**
