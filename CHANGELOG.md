# Changelog

Todos los cambios relevantes de **VaroASCII** se documentan aquí.

## [1.0.0] — 2026-05-13

### ✨ Añadido
- **6 efectos originales VaroASCII:**
  - `glitch` — Distorsión digital con reparación progresiva
  - `typewriter` — Máquina de escribir con cursor, pausas y erratas
  - `neon` — Letrero de neón que se enciende con parpadeos
  - `hack` — Animación Hollywood de hacking con código binario/hex
  - `cinema` — Revelado cinematográfico con foco de luz dramático
  - `radar` — Barrido radar de 360° que ilumina caracteres
- **15 temas de color:** cyberpunk, retrowave, matrix, fire, ocean, sunset, arctic, lava, neon, gold, vapor, terminal, blood, pastel, monochrome
- **Generador ASCII integrado** con fuentes FIGlet y revelado animado (4 modos: row, column, random, instant)
- **Carga de fuentes locales** desde `varoascii/fonts/` con detección automática
- **API simplificada:** `varoascii.render()`, `render_to_string()`, `list_effects()`, `list_themes()`
- **Docker:** Multi-stage build optimizado con `.dockerignore`
- **CLI mejorada:** flags `--theme`, `--list-themes`, atajo `va`
- **Fuente incluida:** Delta Corps Priest 1

### 🔧 Corregido
- `prog="tte"` → `prog="varoascii"` en el parser CLI
- Versión PEP 440 (`1.0.0` en vez de `1.0.0-varo`)
- Empaquetado de fuentes con `force-include` en vez de `shared-data`
- Compatibilidad de carga de fuentes con `Figlet(font=, dir=)`
- Protección contra textos de solo espacios en el efecto typewriter
- `requires-python` actualizado a `>=3.10` (3.8/3.9 son EOL)

### 🔄 Cambios
- Rebranding completo de TerminalTextEffects a VaroASCII
- README profesional en español con documentación completa
- Eliminada dependencia de email placeholder

### 📊 Estadísticas
- **44+ efectos** disponibles (38 heredados + 6 originales)
- **15 temas** de color predefinidos
- **4 funciones** de API pública
