# Comercial Nova · Laboratorio 2 · Versión 2.1

**Paquete para comenzar desde cero.** Abre [GUIA_PARTICIPANTE.md](GUIA_PARTICIPANTE.md) y sigue sus secciones en orden.

No necesitas una versión anterior ni archivos de otra práctica. `ACTUALIZAR_A_2_1.md` era una guía para migrar avances previos y no forma parte de este paquete.

## Qué está resuelto y qué harás

- `lab1.py`: TODO 1–4 resueltos (hashing, autorización, cifrado y recuperación).
- `lab2.py`: completa TODO 5–7 (eventos, minimización y trazabilidad).
- [REPASO_LAB1.md](REPASO_LAB1.md): contexto y recorrido de la primera sesión, sin implementar código.

## 1. Preparar una sola vez

Descomprime la carpeta `comercial_nova` y abre una terminal dentro de ella.

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python preparar.py
$env:DATAOPS_KEY = (Get-Content .secrets/fernet.key -Raw).Trim()
```

Si la activación está bloqueada, utiliza `.\.venv\Scripts\python.exe` en lugar de `python` después de crear el entorno. No cambies la política del equipo.

WSL o Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python preparar.py
export DATAOPS_KEY="$(cat .secrets/fernet.key)"
```

Elige solo una alternativa. `preparar.py` genera los 12 pedidos ficticios, la referencia y tu clave local. No se incluyen claves precreadas.

## 2. Verificar y repasar

```text
python comprobar_1a.py --todo 1
python comprobar_preparacion_lab2.py
```

Debes ver la preparación verificada. Después sigue [REPASO_LAB1.md](REPASO_LAB1.md) y regresa a la sección 5 de la guía principal.

## 3. Completar y probar TODO 5–7

Implementa y guarda cada función en `lab2.py` antes de ejecutar su comprobación:

```text
python comprobar_lab2.py --todo 5
python comprobar_lab2.py --todo 6
python comprobar_lab2.py --todo 7
python comprobar_lab2.py
```

`PENDIENTE` significa que aún falta implementar la función. Las pruebas por TODO son independientes; la comprobación completa se detiene en el primer pendiente o fallo.

## 4. Ejecutar la auditoría

Con los tres TODO completos:

```text
python lab2.py ejecutar --rol operador
python lab2.py consultar --rol auditor --reporte ejecuciones/RUN_ID/reporte.json
```

Sustituye `RUN_ID` por el identificador que imprimió la ejecución. Comprueba los cinco controles del reporte, realiza los escenarios de fallo de la guía y completa `evidencias_lab2.md`.

## Al volver a abrir la terminal

Activa tu entorno y vuelve a cargar `DATAOPS_KEY`. Conserva tus datos y tu clave. **No vuelvas a ejecutar `preparar.py` ni reinstales todo para avanzar de un TODO al siguiente.**

## Archivos del paquete

| Archivo | Uso |
| --- | --- |
| GUIA_PARTICIPANTE.md | Instrucciones completas y resultados esperados |
| REPASO_LAB1.md | Recorrido de la base resuelta |
| lab1.py | Pipeline funcional de la primera sesión |
| lab2.py | Código a completar en esta sesión |
| preparar.py | Preparación inicial de datos, referencia y clave |
| comprobar_1a.py | Comprobar la base y crear una copia alterada |
| comprobar_preparacion_lab2.py | Verificar datos, clave, funciones y permisos previos |
| comprobar_lab2.py | Probar los TODO 5–7 |
| evidencias_lab2.md | Registrar observaciones de la práctica |
| requirements.txt | Instalar dependencias |

No entregues la clave ni el entorno virtual. El detalle cifra nombre y correo; el original permanece legible. El laboratorio produce evidencias técnicas y no certifica cumplimiento normativo integral.
