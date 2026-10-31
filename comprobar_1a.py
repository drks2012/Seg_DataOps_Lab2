"""Comprobaciones de 1A por etapas. Version 2.1; sin soluciones de los TODO."""
import argparse
import hashlib
from pathlib import Path
import sys


class Pendiente(Exception):
    pass


class Revisar(Exception):
    pass


def exigir(condicion, mensaje):
    if not condicion:
        raise Revisar(mensaje)


def probar_hash(lab1):
    """TODO 1 no usa la clave ni llama a cifrar o descifrar."""
    entrada = lab1.DATOS / "pedidos.csv"
    referencia = (lab1.BASE / "referencia.sha256").read_text(encoding="ascii").strip()
    contenido = entrada.read_bytes()
    exigir(hashlib.sha256(contenido).hexdigest() == referencia,
           "El original no coincide con la referencia; revisa su origen sin recalcularla")
    try:
        huella = lab1.calcular_hash(entrada)
    except NotImplementedError:
        raise Pendiente("TODO 1: implementa calcular_hash en lab1.py") from None
    exigir(isinstance(huella, str) and len(huella) == 64,
           "TODO 1 debe devolver un str hexadecimal de 64 caracteres, no imprimirlo")
    exigir(huella == referencia, "TODO 1: la huella del original no coincide")

    # Preparar la misma copia de prueba usada en 1B sin reemplazar una existente.
    alterado = contenido.replace(b"1850.00", b"1851.00", 1)
    exigir(alterado != contenido, "No se encontro el importe de prueba en el original")
    copia = lab1.DATOS / "pedidos_prueba_parte1.csv"
    if copia.exists():
        exigir(copia.read_bytes() == alterado,
               "La copia de prueba existente tiene otro contenido; revisala sin sobrescribirla")
    else:
        with copia.open("xb") as archivo:
            archivo.write(alterado)
    try:
        huella_copia = lab1.calcular_hash(copia)
    except NotImplementedError:
        raise Pendiente("TODO 1: completa calcular_hash para cualquier ruta de archivo") from None
    exigir(huella_copia == hashlib.sha256(alterado).hexdigest(),
           "TODO 1: calcula la huella de la ruta recibida; no devuelvas un valor fijo")
    exigir(huella_copia != referencia, "TODO 1: la modificacion no fue detectada")
    print("TODO 1 OK: original coincide True; copia alterada coincide False.")


def probar_cifrado(lab1):
    """TODO 3 se contrasta con Fernet directamente, sin llamar a TODO 4."""
    fernet = lab1.cargar_cifrador()
    for valor in ("cliente001@example.com", "Cliente Prueba \u00d1"):
        try:
            token = lab1.cifrar(valor, fernet)
        except NotImplementedError:
            raise Pendiente("TODO 3: implementa cifrar en lab1.py") from None
        exigir(isinstance(token, str), "TODO 3 debe devolver un token str, no bytes")
        exigir(token != valor, "TODO 3: el dato sigue legible")
        try:
            recuperado = fernet.decrypt(token.encode("ascii")).decode("utf-8")
        except Exception:
            raise Revisar("TODO 3: el resultado no es un token Fernet ASCII valido para esta clave") from None
        exigir(recuperado == valor, "TODO 3: el token no conserva el texto original")
    print("TODO 3 OK: token ASCII valido y cifrado verificado sin TODO 4.")


def probar_descifrado(lab1):
    """TODO 4 usa el TODO 3 ya verificado para producir el token."""
    fernet = lab1.cargar_cifrador()
    for valor in ("cliente001@example.com", "Cliente Prueba \u00d1"):
        try:
            token = lab1.cifrar(valor, fernet)
        except NotImplementedError:
            raise Pendiente("TODO 4 requiere TODO 3: completa cifrar y verifica --todo 3 primero") from None
        exigir(isinstance(token, str), "Antes de TODO 4, verifica cifrar con --todo 3")
        try:
            exigir(fernet.decrypt(token.encode("ascii")).decode("utf-8") == valor,
                   "Antes de TODO 4, corrige cifrar con --todo 3")
        except Revisar:
            raise
        except Exception:
            raise Revisar("Antes de TODO 4, corrige cifrar con --todo 3") from None
        try:
            recuperado = lab1.descifrar(token, fernet)
        except NotImplementedError:
            raise Pendiente("TODO 4: implementa descifrar en lab1.py") from None
        exigir(isinstance(recuperado, str) and recuperado == valor,
               "TODO 4 debe devolver el texto UTF-8 original, no bytes ni None")
    print("TODO 4 OK: recuperacion coincidente True.")


def main():
    parser = argparse.ArgumentParser(
        description="Valida TODO 1, 3 o 4 por separado; sin --todo prueba 1, 3 y 4 en orden.")
    parser.add_argument("--todo", type=int, choices=[1, 3, 4],
                        help="Etapa que quieres comprobar; TODO 4 requiere TODO 3")
    args = parser.parse_args()
    try:
        import lab1
        exigir(Path(lab1.__file__).resolve().parent == Path(__file__).resolve().parent,
               "Coloca este comprobador junto a lab1.py en comercial_nova")
        pruebas = {1: probar_hash, 3: probar_cifrado, 4: probar_descifrado}
        for numero in ([args.todo] if args.todo is not None else [1, 3, 4]):
            pruebas[numero](lab1)
        if args.todo is None:
            print("Repaso de proteccion verificado: TODO 1, 3 y 4 resueltos. La preparacion revisa tambien TODO 2.")
        else:
            print(f"Etapa TODO {args.todo} verificada; este resultado no valida las otras etapas.")
        return 0
    except Pendiente as exc:
        print(f"PENDIENTE: {exc}", file=sys.stderr)
        return 2
    except Revisar as exc:
        print(f"REVISAR: {exc}", file=sys.stderr)
        return 1
    except ModuleNotFoundError:
        print("REVISAR: faltan lab1.py o las dependencias; revisa GUIA_PARTICIPANTE.md", file=sys.stderr)
        return 1
    except FileNotFoundError:
        print("REVISAR: falta un archivo de preparacion; revisa GUIA_PARTICIPANTE.md", file=sys.stderr)
        return 1
    except ValueError:
        print("REVISAR: comprueba DATAOPS_KEY y los tipos o valores devueltos; consulta REPASO_LAB1.md", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"REVISAR: {type(exc).__name__}; consulta REPASO_LAB1.md y revisa la etapa seleccionada", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
