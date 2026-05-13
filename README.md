# 🌌 VaroASCII: El Motor Definitivo de Arte ASCII y Efectos Visuales para Terminal

¡Bienvenido a **VaroASCII**! Una herramienta "todo en uno" que combina la potencia de más de **40 efectos visuales animados** con la generación de arte ASCII profesional, temas de color predefinidos y una API simplificada.

> [!IMPORTANT]
> **PROYECTO PRIVADO**: Este repositorio es de uso personal y para desarrollo específico de VaroTv7.

---

## ✨ Características Principales

*   🎨 **10 Temas de Color**: Cyberpunk, Retrowave, Matrix, Fire, Ocean, Sunset, Arctic, Lava, Neon y Gold.
*   🆕 **Efectos Originales**: `glitch` (distorsión digital) y `typewriter` (máquina de escribir) — exclusivos de VaroASCII.
*   🔤 **Generador ASCII Integrado**: Convierte texto en arte ASCII con fuentes FIGlet (incluyendo *Delta Corps Priest 1*).
*   🎬 **Revelado Animado**: El arte ASCII se revela de forma progresiva (fila, columna, aleatorio).
*   📚 **40+ Efectos Visuales**: Lluvia, matriz, fuegos artificiales, desintegración, humo, etc.
*   🎯 **API Simplificada**: `varoascii.render("texto", effect="rain", theme="cyberpunk")`.
*   🐳 **Docker Listo**: Multi-stage build con imagen optimizada.
*   🔧 **CI/CD**: GitHub Actions con lint, tests y build Docker automático.

---

## 🚀 Instalación

### 1. Sin Docker (Local)

#### Requisitos
*   Python 3.10 o superior.
*   `pip` o `uv` (recomendado).

#### Instalación rápida
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

#### Construir la imagen
```bash
docker build -t varoascii .
```

#### Ejecutar
```bash
echo "Varo" | docker run -it varoascii glitch --theme cyberpunk
```

---

## 🛠️ Uso y Ejemplos

### Comandos Básicos

Generar arte ASCII con revelado animado:
```bash
echo "VaroASCII" | varoascii ascii --font slant --reveal-mode row --reveal-speed 5
```

Efecto glitch con tema cyberpunk (🆕 **exclusivo VaroASCII**):
```bash
echo "HACKING..." | varoascii --theme cyberpunk glitch --glitch-intensity 70
```

Efecto máquina de escribir (🆕 **exclusivo VaroASCII**):
```bash
echo "Bienvenido a VaroASCII" | varoascii typewriter --typing-speed 1 --mistake-probability 5
```

Efecto de descompresión con tema fire:
```bash
echo "ACCESO DENEGADO" | varoascii --theme fire decrypt --typing-speed 2
```

Lanzar un efecto aleatorio:
```bash
echo "Sorpresa" | varoascii -R
```

### El comando `ascii` con revelado animado
*   `--font`: Fuente FIGlet (ej: `slant`, `standard`, `block`, `Delta Corps Priest 1`).
*   `--reveal-mode`: Cómo se revela (`row`, `column`, `random`, `instant`).
*   `--reveal-speed`: Caracteres por frame (por defecto: 3).
*   `--list-fonts`: Muestra todas las fuentes disponibles (locales marcadas con ⭐).

### 🎨 Temas de Color
Aplica un tema a cualquier efecto con `--theme`:
```bash
echo "Texto" | varoascii --theme retrowave matrix
echo "Texto" | varoascii --theme neon rain
varoascii --list-themes  # Ver todos los temas disponibles
```

| Tema | Colores |
|------|---------|
| `cyberpunk` | Magenta → Cyan → Hot Pink |
| `retrowave` | Neon Pink → Slate Blue → Turquoise |
| `matrix` | Green → Dark Green → Deep Green |
| `fire` | Orange-Red → Dark Orange → Gold |
| `ocean` | Sea Blue → Sky Blue → Turquoise |
| `sunset` | Coral → Salmon → Saffron |
| `arctic` | Ice White → Light Cyan → Medium Cyan |
| `lava` | Red → Orange-Red → Dark Red |
| `neon` | Neon Green → Neon Red → Neon Cyan |
| `gold` | Gold → Goldenrod → Dark Goldenrod |

### 🐍 Uso como Librería Python
```python
import varoascii

# Forma más sencilla
varoascii.render("¡Hola Mundo!", effect="rain")

# Con tema de color
varoascii.render("VaroASCII", effect="glitch", theme="cyberpunk")

# Con fuente ASCII art
varoascii.render("VARO", effect="print", font="slant", theme="fire")
```

---

## 📋 Lista Completa de Efectos (40+)

| Efecto | Descripción |
|--------|-------------|
| `ascii` | Genera arte ASCII con fuentes FIGlet y revelado animado |
| `beams` | Rayos de luz que revelan el texto |
| `binarypath` | Caminos binarios que forman el texto |
| `blackhole` | El texto es absorbido por un agujero negro |
| `bouncyballs` | Bolas que rebotan formando el texto |
| `bubbles` | Burbujas que flotan y revelan el texto |
| `burn` | El texto se quema y desaparece |
| `colorshift` | Cambio de colores progresivo |
| `crumble` | El texto se desmorona |
| `decrypt` | Desencriptación estilo película |
| `errorcorrect` | Corrección de errores visual |
| `expand` | El texto se expande desde el centro |
| `fireworks` | Fuegos artificiales que revelan el texto |
| `glitch` | 🆕 Distorsión digital con reparación progresiva |
| `highlight` | Resaltado progresivo del texto |
| `laseretch` | Grabado láser del texto |
| `matrix` | Efecto lluvia estilo Matrix |
| `middleout` | Revelado desde el centro hacia fuera |
| `orbittingvolley` | Órbitas que forman el texto |
| `overflow` | Desbordamiento de caracteres |
| `pour` | El texto cae como un líquido |
| `print` | Impresión simple con gradiente |
| `rain` | Lluvia de caracteres |
| `randomsequence` | Secuencia aleatoria de revelado |
| `rings` | Anillos concéntricos |
| `scattered` | Dispersión y recomposición |
| `slice` | Cortes que revelan el texto |
| `slide` | Deslizamiento del texto |
| `smoke` | Efecto de humo |
| `spotlights` | Focos que iluminan el texto |
| `spray` | Spray de pintura |
| `swarm` | Enjambre de caracteres |
| `sweep` | Barrido horizontal/vertical |
| `synthgrid` | Cuadrícula sintética retro |
| `thunderstorm` | Tormenta eléctrica |
| `typewriter` | 🆕 Máquina de escribir con cursor y erratas |
| `unstable` | Texto inestable que vibra |
| `vhstape` | Distorsión de cinta VHS |
| `waves` | Ondas que recorren el texto |
| `wipe` | Limpieza progresiva del texto |

---

## 🪟 Guía Específica para Windows

Se recomienda usar **Windows Terminal** o **PowerShell 7** para colores ANSI:

```powershell
"Hola Varo" | varoascii --theme cyberpunk glitch
"VaroASCII" | varoascii ascii --font block --reveal-mode random
```

---

## 🐧 Guía Específica para Linux

Funciona en cualquier emulador moderno (GNOME Terminal, Alacritty, Kitty, etc.):

```bash
pip install .
echo "VaroASCII" | varoascii --theme retrowave typewriter
```

---

## 🐳 Docker Avanzado

```bash
# Construir
docker build -t varoascii .

# Ejecutar un efecto con tema
echo "Docker" | docker run -it varoascii --theme matrix rain

# Usando docker-compose
docker compose build
echo "Test" | docker compose run varoascii glitch
```

---

## 📂 Estructura del Proyecto

```
varoascii/
├── __init__.py          # API pública + render()
├── __main__.py          # Punto de entrada CLI
├── themes.py            # 10 temas de color predefinidos
├── effects/             # 40+ módulos de efectos
│   ├── effect_ascii.py      # Generador ASCII con revelado animado
│   ├── effect_glitch.py     # 🆕 Efecto glitch (original VaroASCII)
│   ├── effect_typewriter.py # 🆕 Efecto typewriter (original VaroASCII)
│   └── ...                  # Efectos heredados mejorados
├── fonts/               # Fuentes FIGlet personalizadas
│   └── Delta Corps Priest 1.flf
├── engine/              # Motor de animación y renderizado
└── utils/               # Utilidades (colores, geometría, etc.)
.github/workflows/ci.yml # CI/CD con GitHub Actions
Dockerfile               # Multi-stage build optimizado
docker-compose.yml        # Orquestación Docker
```

---

## 📜 Licencia

Distribuido bajo la Licencia MIT. Consulta el archivo `LICENSE` para más información.

---

**Desarrollado con ❤️ por VaroTv7**
