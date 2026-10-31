"""Verifica el punto de partida sin generar salidas ni mostrar secretos."""
import hashlib
import os
import sys
from pathlib import Path


def main():
    try:
        import lab1
    except ImportError as exc:
        raise RuntimeError("Falta lab1.py o su dependencia; revisa README.md") from exc
    if Path(lab1.__file__).resolve().parent != Path(__file__).resolve().parent:
        raise RuntimeError("lab1.py debe estar junto a este comprobador")
    entrada=lab1.DATOS/"pedidos.csv"
    referencia=lab1.BASE/"referencia.sha256"
    esperado=referencia.read_text(encoding="ascii").strip()
    real=hashlib.sha256(entrada.read_bytes()).hexdigest()
    assert real==esperado,"El original no coincide; no recalcules la referencia"
    assert lab1.calcular_hash(entrada)==esperado,"Revisa TODO 1"
    rows=lab1.leer_pedidos(entrada)
    assert len(rows)==12,"Se esperan 12 pedidos del caso"
    assert os.environ.get("DATAOPS_KEY"),"Carga DATAOPS_KEY en esta terminal"
    clave=(lab1.BASE/".secrets/fernet.key").read_text(encoding="ascii").strip()
    assert os.environ["DATAOPS_KEY"]==clave,"Carga la clave original de .secrets/fernet.key"
    f=lab1.cargar_cifrador()
    texto="prueba_sin_datos_personales"
    token=lab1.cifrar(texto,f)
    assert isinstance(token,str) and token!=texto,"Revisa TODO 3"
    assert lab1.descifrar(token,f)==texto,"Revisa TODO 4"
    permisos={"operador":{"ejecutar","recuperar"},"analista":{"resumen"},"auditor":{"evidencias"}}
    for rol in ["operador","analista","auditor","desconocido"]:
        for op in ["ejecutar","recuperar","resumen","evidencias","inexistente"]:
            try:lab1.autorizar(rol,op)
            except PermissionError:
                assert op not in permisos.get(rol,set()),"Permiso valido denegado"
            else:
                assert op in permisos.get(rol,set()),"Operacion no autorizada permitida"
    copia=lab1.DATOS/"pedidos_prueba_parte1.csv"
    if not copia.exists():
        print("AVISO: falta la copia alterada; creala con comprobar_1a.py antes del escenario A")
    else:
        assert hashlib.sha256(copia.read_bytes()).hexdigest()!=esperado,"La copia no esta alterada"
    print("Preparacion verificada: datos, referencia, clave y TODO 1 a 4")
    print("No se han creado salidas ni mostrado claves o datos personales")


if __name__=="__main__":
    try:main()
    except Exception as exc:
        # Mensajes sin imprimir excepciones que pudieran contener datos.
        if isinstance(exc,(AssertionError,RuntimeError,NotImplementedError)):
            sys.exit(f"REVISAR: {exc}")
        sys.exit(f"REVISAR: {type(exc).__name__}; consulta GUIA_PARTICIPANTE.md")
