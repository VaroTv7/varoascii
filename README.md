<p align="center">
  <img src="https://img.shields.io/badge/VaroASCII-v1.0.0-00ff41?style=for-the-badge&logo=gnometerminal&logoColor=white" alt="Version"/>
  <img src="https://img.shields.io/badge/Python-3.10+-3776ab?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Docker-Ready-2496ed?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"/>
  <img src="https://img.shields.io/badge/Efectos-40+-ff6ec7?style=for-the-badge" alt="Effects"/>
  <img src="https://img.shields.io/badge/Licencia-MIT-ffd700?style=for-the-badge" alt="License"/>
</p>

<h1 align="center">🌌 VaroASCII</h1>
<h3 align="center">El Motor Definitivo de Arte ASCII y Efectos Visuales para Terminal</h3>

<p align="center">
  <em>Transforma cualquier texto en animaciones espectaculares directamente en tu terminal.</em><br/>
  <em>Genera arte ASCII, aplica efectos visuales cinematográficos y personaliza cada detalle.</em>
</p>

---

> [!IMPORTANT]
> **PROYECTO PRIVADO** — Este repositorio es propiedad exclusiva de **VaroTv7**. Uso personal y desarrollo específico.

---

## 📋 Índice

- [Descripción General](#-descripción-general)
- [Características Principales](#-características-principales)
- [Requisitos del Sistema](#-requisitos-del-sistema)
- [Instalación](#-instalación)
- [Guía de Uso Completa](#-guía-de-uso-completa)
- [Sistema de Temas de Color](#-sistema-de-temas-de-color)
- [Catálogo Completo de Efectos](#-catálogo-completo-de-efectos)
- [Efectos Exclusivos VaroASCII](#-efectos-exclusivos-varoascii)
- [Generador ASCII Integrado](#-generador-ascii-integrado)
- [API para Desarrolladores](#-api-para-desarrolladores)
- [Despliegue con Docker](#-despliegue-con-docker)
- [Guía por Sistema Operativo](#-guía-por-sistema-operativo)
- [Arquitectura del Proyecto](#-arquitectura-del-proyecto)
- [Diferencias con el Proyecto Original](#-diferencias-con-el-proyecto-original)
- [Resolución de Problemas](#-resolución-de-problemas)
- [Licencia](#-licencia)

---

## 🔍 Descripción General

**VaroASCII** es un motor de efectos visuales para terminal que combina tres herramientas en una sola:

1. **Motor de Animaciones** — Más de 40 efectos visuales que transforman texto plano en animaciones cinematográficas (lluvia, fuego, glitch, matrix, desencriptación y muchos más).
2. **Generador de Arte ASCII** — Convierte cualquier texto en tipografías artísticas usando fuentes FIGlet, con soporte para fuentes locales personalizadas.
3. **Sistema de Temas** — 10 paletas de color predefinidas que se pueden aplicar a cualquier efecto con un solo flag.

Es un fork mejorado de [TerminalTextEffects](https://github.com/ChrisBuilds/terminaltexteffects), extendido con funcionalidades exclusivas, efectos originales, y una API simplificada.

### ¿Para qué sirve?

- **Scripts de bienvenida** en servidores y terminales.
- **Presentaciones** y demostraciones de terminal en vivo.
- **Banners animados** para herramientas CLI propias.
- **Contenido para streams** y vídeos de programación.
- **Automatización visual** de tareas con estilo.

---

## ✨ Características Principales

| Funcionalidad | Descripción |
|---------------|-------------|
| 🎬 **40+ Efectos** | Animaciones de terminal: rain, matrix, burn, decrypt, fireworks, glitch, typewriter... |
| 🆕 **Efectos Originales** | `glitch` y `typewriter` — exclusivos de VaroASCII, no existen en el proyecto original |
| 🔤 **Arte ASCII** | Generación integrada de texto artístico con fuentes FIGlet y revelado animado |
| 🎨 **10 Temas** | Paletas predefinidas: cyberpunk, retrowave, matrix, fire, ocean, sunset, arctic, lava, neon, gold |
| 📦 **Fuentes Locales** | Carga automática de archivos `.flf` desde `varoascii/fonts/` — incluye *Delta Corps Priest 1* |
| 🐍 **API Python** | Función `varoascii.render()` para integración programática en 1 línea |
| 🎯 **CLI Completa** | Interfaz de línea de comandos con ayuda detallada para cada efecto y parámetro |
| 🌈 **Color RGB/Xterm** | Soporte completo para colores de 24 bits (RGB) y paletas de 256 colores (Xterm) |
| 🐳 **Docker** | Multi-stage build optimizado con `.dockerignore` |
| ⚡ **Pipes Unix** | Composición de efectos mediante tuberías estándar |
| 🔧 **Extensible** | Sistema de plugins: añade efectos personalizados en `~/.config/varoascii/effects/` |

---

## 💻 Requisitos del Sistema

| Componente | Requisito |
|------------|-----------|
| **Python** | 3.10 o superior |
| **SO** | Windows 10+, Linux, macOS |
| **Terminal** | Compatible con secuencias ANSI y colores de 24 bits |
| **Dependencias** | `pyfiglet >= 0.8` (se instala automáticamente) |

### Terminales Recomendadas

| Plataforma | Terminal Recomendada |
|------------|---------------------|
| **Windows** | Windows Terminal, PowerShell 7 |
| **Linux** | Alacritty, Kitty, GNOME Terminal |
| **macOS** | iTerm2, Alacritty |

> [!WARNING]
> La consola clásica de Windows (`cmd.exe`) tiene soporte limitado de colores ANSI. Usa **Windows Terminal** para la mejor experiencia.

---

## 🚀 Instalación

### Método 1 — Instalación Local (recomendado)

```bash
# 1. Clonar el repositorio
git clone https://github.com/VaroTv7/varoascii.git
cd varoascii

# 2. Instalar con pip
pip install .

# 3. Verificar la instalación
varoascii --version
```

#### Con `uv` (alternativa rápida)
```bash
uv pip install .
```

#### Modo desarrollo (para contribuir)
```bash
pip install -e .
```

### Método 2 — Docker

```bash
# Construir la imagen
docker build -t varoascii .

# Verificar
echo "Hola" | docker run -i varoascii --help
```

> [!TIP]
> Se instalan dos alias: `varoascii` (nombre completo) y `va` (atajo rápido).

---

## 🛠️ Guía de Uso Completa

### Sintaxis General

```
echo "texto" | varoascii [opciones globales] <efecto> [opciones del efecto]
```

O con archivo de entrada:
```
varoascii -i archivo.txt <efecto> [opciones]
```

### Opciones Globales

| Flag | Descripción |
|------|-------------|
| `--theme <nombre>` / `-t` | Aplica un tema de color al efecto |
| `--list-themes` | Muestra todos los temas disponibles |
| `--random-effect` / `-R` | Selecciona un efecto al azar |
| `--input-file <ruta>` / `-i` | Lee el texto desde un archivo |
| `--seed <int>` | Semilla para reproducir resultados aleatorios |
| `--xterm-colors` | Usa paleta Xterm de 256 colores |
| `--no-color` | Desactiva colores |
| `--frame-rate <fps>` | Fotogramas por segundo de la animación |
| `--canvas-width <int>` | Ancho del lienzo de renderizado |
| `--canvas-height <int>` | Alto del lienzo de renderizado |
| `--wrap-text` | Ajusta el texto al ancho del terminal |
| `--version` / `-v` | Muestra la versión instalada |

### Ejemplos Rápidos

```bash
# Efecto lluvia básico
echo "VaroASCII" | varoascii rain

# Efecto matrix con tema cyberpunk
echo "SYSTEM ONLINE" | varoascii --theme cyberpunk matrix

# Glitch con alta intensidad (exclusivo VaroASCII)
echo "HACKING..." | varoascii --theme neon glitch --glitch-intensity 80

# Máquina de escribir con erratas (exclusivo VaroASCII)
echo "Bienvenido al sistema" | varoascii typewriter --mistake-probability 10

# Arte ASCII con revelado animado
echo "VARO" | varoascii ascii --font slant --reveal-mode row --reveal-speed 5

# Desencriptación estilo película
echo "ACCESO DENEGADO" | varoascii --theme fire decrypt --typing-speed 2

# Efecto aleatorio
echo "Sorpresa" | varoascii -R

# Encadenar: generar ASCII art → aplicar efecto
echo "VARO" | varoascii ascii --font block | varoascii --theme retrowave rain

# Ayuda específica de un efecto
varoascii glitch -h
```

---

## 🎨 Sistema de Temas de Color

Aplica un tema a **cualquier efecto** con el flag `--theme` o `-t`. El tema sobreescribe los colores del gradiente final del efecto.

```bash
echo "Texto" | varoascii --theme cyberpunk <efecto>
varoascii --list-themes   # Ver todos los temas
```

### Catálogo de Temas

| Tema | Colores | Estética |
|------|---------|----------|
| 🟣 `cyberpunk` | `#ff00ff` → `#00ffff` → `#ff0080` | Neón urbano futurista |
| 🌊 `retrowave` | `#ff6ec7` → `#7b68ee` → `#00ced1` | Synthwave años 80 |
| 🟢 `matrix` | `#00ff41` → `#008f11` → `#003b00` | Terminal estilo Matrix |
| 🔥 `fire` | `#ff4500` → `#ff8c00` → `#ffd700` | Llamas y brasas |
| 🌊 `ocean` | `#006994` → `#00bfff` → `#40e0d0` | Profundidad marina |
| 🌅 `sunset` | `#ff6b6b` → `#ffa07a` → `#ffd93d` | Atardecer cálido |
| ❄️ `arctic` | `#e0f7fa` → `#80deea` → `#4dd0e1` | Hielo y escarcha |
| 🌋 `lava` | `#ff0000` → `#ff4500` → `#8b0000` | Magma volcánico |
| ⚡ `neon` | `#39ff14` → `#ff073a` → `#0ff0fc` | Neón eléctrico |
| ✨ `gold` | `#ffd700` → `#daa520` → `#b8860b` | Oro y lujo |

---

## 📚 Catálogo Completo de Efectos (40+)

### Efectos de Revelado
| Efecto | Descripción | Parámetros Clave |
|--------|-------------|------------------|
| `print` | Impresión simple con gradiente de color | `--final-gradient-stops`, `--final-gradient-direction` |
| `expand` | El texto se expande desde el centro | `--final-gradient-stops` |
| `middleout` | Revelado desde el medio hacia los extremos | `--expand-direction` |
| `pour` | El texto cae como un líquido desde arriba | `--pour-direction` |
| `scattered` | Caracteres dispersos que se recomponen | `--final-gradient-stops` |
| `sweep` | Barrido horizontal o vertical | `--final-gradient-stops` |
| `wipe` | Limpieza progresiva | `--wipe-direction` |
| `slide` | Deslizamiento del texto | `--movement-speed` |
| `randomsequence` | Revelado en orden aleatorio | `--speed` |
| `highlight` | Resaltado progresivo del texto | `--final-gradient-stops` |

### Efectos Cinematográficos
| Efecto | Descripción | Parámetros Clave |
|--------|-------------|------------------|
| `decrypt` | Desencriptación estilo película de hackers | `--typing-speed`, `--ciphertext-colors` |
| `matrix` | Lluvia de código verde estilo Matrix | `--rain-colors`, `--final-gradient-stops` |
| `rain` | Lluvia de caracteres que forman el texto | `--rain-symbols`, `--rain-colors` |
| `fireworks` | Fuegos artificiales que revelan el texto | `--firework-colors`, `--launch-delay` |
| `beams` | Rayos de luz que iluminan el texto | `--beam-delay` |
| `laseretch` | Grabado láser carácter a carácter | `--final-gradient-stops` |
| `spotlights` | Focos de luz que revelan el texto | `--spotlight-count` |

### Efectos de Destrucción
| Efecto | Descripción | Parámetros Clave |
|--------|-------------|------------------|
| `burn` | El texto se quema con efecto de fuego | `--burned-color`, `--final-gradient-stops` |
| `crumble` | El texto se desmorona y cae | `--final-gradient-stops` |
| `blackhole` | El texto es absorbido por un agujero negro | `--blackhole-color` |
| `slice` | El texto se corta en fragmentos | `--slice-direction` |

### Efectos de Movimiento
| Efecto | Descripción | Parámetros Clave |
|--------|-------------|------------------|
| `bouncyballs` | Bolas que rebotan y forman el texto | `--ball-colors` |
| `bubbles` | Burbujas que flotan hasta posición | `--bubble-colors`, `--bubble-speed` |
| `orbittingvolley` | Órbitas de caracteres | `--top-launcher-symbol` |
| `spray` | Spray de pintura | `--spray-colors` |
| `swarm` | Enjambre de caracteres que convergen | `--swarm-colors` |
| `waves` | Ondas que recorren el texto | `--wave-count` |

### Efectos de Distorsión
| Efecto | Descripción | Parámetros Clave |
|--------|-------------|------------------|
| `errorcorrect` | Errores que se corrigen en tiempo real | `--error-pairs` |
| `overflow` | Desbordamiento de caracteres | `--final-gradient-stops` |
| `unstable` | Texto inestable que vibra | `--final-gradient-stops` |
| `vhstape` | Distorsión de cinta VHS retro | `--glitch-line-colors` |
| `colorshift` | Cambio de colores progresivo | `--travel-direction` |

### Efectos Especiales
| Efecto | Descripción | Parámetros Clave |
|--------|-------------|------------------|
| `smoke` | El texto aparece entre humo | `--final-gradient-stops` |
| `rings` | Anillos concéntricos que revelan | `--ring-colors` |
| `synthgrid` | Cuadrícula retro sintética | `--grid-gradient-stops` |
| `thunderstorm` | Tormenta eléctrica con relámpagos | `--lightning-colors` |
| `binarypath` | Caminos binarios que forman el texto | `--binary-colors` |

---

## 🆕 Efectos Exclusivos VaroASCII

Estos efectos son **creación original** de VaroASCII y no existen en el proyecto base.

### 🔮 Glitch — Distorsión Digital

El texto aparece como símbolos corruptos con colores de aberración cromática. Tras una fase de caos controlado, los caracteres se reparan progresivamente hasta revelar el mensaje final.

```bash
echo "SYSTEM BREACH" | varoascii --theme cyberpunk glitch
```

**Fases de la animación:**
1. **Aparición** — Todo el texto aparece como bloques corruptos (░▒▓█⣿⡿).
2. **Caos** — Los caracteres parpadean aleatoriamente durante `--glitch-duration` frames.
3. **Reparación** — Los caracteres se estabilizan progresivamente con `--settle-speed`.

| Parámetro | Default | Descripción |
|-----------|---------|-------------|
| `--glitch-intensity` | 50 | Probabilidad (1-100) de glitch por frame |
| `--glitch-duration` | 30 | Frames de fase caótica |
| `--settle-speed` | 2 | Caracteres reparados por frame |

### ⌨️ Typewriter — Máquina de Escribir

Los caracteres aparecen uno a uno con un cursor visible que avanza por el texto. Incluye pausas naturales en espacios y erratas que se corrigen automáticamente.

```bash
echo "Bienvenido al sistema VaroASCII" | varoascii typewriter --mistake-probability 8
```

**Características:**
- Cursor visible (█) que avanza con cada carácter.
- Pausas naturales al encontrar espacios.
- Erratas aleatorias que se muestran en rojo y se corrigen automáticamente.

| Parámetro | Default | Descripción |
|-----------|---------|-------------|
| `--typing-speed` | 1 | Caracteres escritos por frame |
| `--cursor-symbol` | █ | Símbolo del cursor |
| `--cursor-color` | `00ff00` | Color del cursor |
| `--pause-on-space` | 2 | Frames de pausa en espacios |
| `--mistake-probability` | 3 | Probabilidad (0-100) de errata |

---

## 🔤 Generador ASCII Integrado

El efecto `ascii` convierte texto plano en arte ASCII usando fuentes FIGlet y lo revela con animación progresiva.

```bash
# Revelado fila por fila
echo "VARO" | varoascii ascii --font slant --reveal-mode row

# Revelado aleatorio con tema
echo "HACK" | varoascii --theme neon ascii --font block --reveal-mode random

# Ver todas las fuentes disponibles (locales marcadas con ⭐)
varoascii ascii --list-fonts
```

### Parámetros del Efecto ASCII

| Parámetro | Default | Opciones | Descripción |
|-----------|---------|----------|-------------|
| `--font` | `standard` | Cualquier FIGlet | Fuente tipográfica |
| `--reveal-mode` | `row` | `row`, `column`, `random`, `instant` | Modo de revelado |
| `--reveal-speed` | 3 | Entero positivo | Caracteres por frame |
| `--list-fonts` | — | — | Lista todas las fuentes |

### Fuentes Locales Personalizadas

VaroASCII busca fuentes `.flf` en el directorio `varoascii/fonts/`. Actualmente incluye:

- **Delta Corps Priest 1** — Tipografía militar/cyberpunk.

Para añadir más fuentes, simplemente copia archivos `.flf` a esa carpeta. Se detectarán automáticamente.

---

## 🐍 API para Desarrolladores

VaroASCII se puede usar como librería Python con una API de alto nivel:

```python
import varoascii

# Uso básico — una sola línea
varoascii.render("¡Hola Mundo!", effect="rain")

# Con tema de color
varoascii.render("VaroASCII", effect="glitch", theme="cyberpunk")

# Con fuente ASCII art + tema
varoascii.render("VARO", effect="print", font="slant", theme="fire")
```

### Firma de la Función

```python
varoascii.render(
    text: str,              # Texto a animar
    effect: str = "print",  # Nombre del efecto
    theme: str | None,      # Tema de color (opcional)
    font: str | None,       # Fuente FIGlet (opcional)
) -> None
```

### Uso Avanzado (control granular)

```python
from varoascii.effects import Glitch
from varoascii.engine.terminal import TerminalConfig

config = Glitch.GlitchConfig._build_config()
config.glitch_intensity = 80
config.glitch_duration = 50

effect = Glitch("Mi texto", effect_config=config)
with effect.terminal_output() as terminal:
    for frame in effect:
        terminal.print(frame)
```

---

## 🐳 Despliegue con Docker

### Construcción

```bash
docker build -t varoascii .
```

El Dockerfile usa **multi-stage build** para optimizar el tamaño de la imagen final.

### Ejecución

```bash
# Efecto básico
echo "Docker funciona" | docker run -i varoascii rain

# Con tema
echo "Cyberpunk" | docker run -i varoascii --theme cyberpunk glitch

# Modo interactivo
docker run -it varoascii --help
```

### Docker Compose

```bash
docker compose build
echo "Test" | docker compose run varoascii glitch
```

> [!TIP]
> Usa siempre el flag `-i` (stdin) o `-it` (stdin + TTY) para que Docker reciba el texto por la tubería.

---

## 🖥️ Guía por Sistema Operativo

### 🪟 Windows

**Requisitos:** Windows 10 build 1903+, Windows Terminal o PowerShell 7.

```powershell
# Instalación
git clone https://github.com/VaroTv7/varoascii.git
cd varoascii
pip install .

# Uso con PowerShell
"Hola Varo" | varoascii --theme cyberpunk glitch
"VaroASCII" | varoascii ascii --font block --reveal-mode random

# Atajo rápido
"Test" | va rain
```

### 🐧 Linux

Funciona en cualquier emulador moderno con soporte ANSI.

```bash
# Instalación
git clone https://github.com/VaroTv7/varoascii.git
cd varoascii
pip install .

# Uso
echo "VaroASCII" | varoascii --theme retrowave typewriter
cat archivo.txt | varoascii matrix

# En scripts de bienvenida (.bashrc)
echo "Bienvenido $(whoami)" | varoascii --theme gold print
```

---

## 📂 Arquitectura del Proyecto

```
varoascii/
├── __init__.py              # API pública + varoascii.render()
├── __main__.py              # Punto de entrada CLI
├── themes.py                # 10 temas de color predefinidos
├── effects/                 # 40+ módulos de efectos
│   ├── effect_ascii.py          # Generador ASCII con revelado animado
│   ├── effect_glitch.py         # 🆕 Efecto glitch (original)
│   ├── effect_typewriter.py     # 🆕 Efecto typewriter (original)
│   ├── effect_rain.py           # Lluvia de caracteres
│   ├── effect_matrix.py         # Efecto Matrix
│   ├── effect_decrypt.py        # Desencriptación
│   └── ... (35+ efectos más)
├── fonts/                   # Fuentes FIGlet personalizadas
│   └── Delta Corps Priest 1.flf
├── engine/                  # Motor de animación
│   ├── terminal.py              # Gestión del terminal
│   ├── animation.py             # Sistema de escenas y frames
│   ├── base_effect.py           # Clases base para efectos
│   ├── base_character.py        # Gestión de caracteres
│   └── motion.py                # Sistema de movimiento
├── utils/                   # Utilidades
│   ├── graphics.py              # Colores, gradientes
│   ├── geometry.py              # Coordenadas, matemáticas
│   ├── easing.py                # Funciones de interpolación
│   └── argutils.py              # Parseo de argumentos CLI
├── template/                # Plantilla para crear nuevos efectos
Dockerfile                   # Multi-stage build
docker-compose.yml           # Orquestación Docker
.dockerignore                # Exclusiones de build
pyproject.toml               # Configuración del paquete
```

### Sistema de Plugins

VaroASCII soporta efectos personalizados. Coloca archivos `.py` en:
- **Linux/macOS:** `~/.config/varoascii/effects/`
- **Windows:** `%APPDATA%/varoascii/effects/`

Cada archivo debe implementar `get_effect_resources()` devolviendo el nombre del comando, la clase del efecto y la clase de configuración.

---

## 🔄 Diferencias con el Proyecto Original

| Característica | TerminalTextEffects | VaroASCII |
|----------------|--------------------:|----------:|
| Efectos totales | 38 | **40+** |
| Efectos originales | 0 | **2** (glitch, typewriter) |
| Arte ASCII integrado | ❌ | ✅ con revelado animado |
| Temas de color | ❌ | ✅ 10 paletas predefinidas |
| Fuentes locales `.flf` | ❌ | ✅ carga automática |
| API `render()` | ❌ | ✅ 1 línea de código |
| Docker multi-stage | ❌ | ✅ imagen optimizada |
| Documentación español | ❌ | ✅ completa |
| Atajo CLI `va` | ❌ | ✅ |

---

## 🔧 Resolución de Problemas

| Problema | Solución |
|----------|----------|
| Los colores no se muestran | Usa **Windows Terminal** o un emulador con soporte ANSI de 24 bits |
| `varoascii: command not found` | Asegúrate de que `pip install .` finalizó correctamente y que el directorio `Scripts/` está en tu `PATH` |
| La fuente personalizada no se carga | Verifica que el archivo `.flf` está en `varoascii/fonts/` y que el nombre coincide exactamente (sin extensión) |
| Error de encoding en Windows | Ejecuta `chcp 65001` antes de usar VaroASCII para activar UTF-8 |
| La animación va muy rápida/lenta | Ajusta con `--frame-rate <fps>` (por defecto ~60 fps) |
| Docker no recibe texto | Usa `echo "texto" \| docker run -i varoascii <efecto>` (flag `-i` obligatorio) |

---

## 📜 Licencia

Distribuido bajo la **Licencia MIT**. Consulta el archivo [LICENSE](LICENSE) para más información.

---

<p align="center">
  <strong>Desarrollado con ❤️ por <a href="https://github.com/VaroTv7">VaroTv7</a></strong><br/>
  <em>VaroASCII v1.0.0 — Motor de Efectos Visuales y Arte ASCII para Terminal</em>
</p>
