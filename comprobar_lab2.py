"""Comprobador del laboratorio 2 version 2.1, independiente por TODO."""
import argparse
from datetime import datetime, timezone, timedelta
import json
from pathlib import Path
import sys
import tempfile


def exigir(condicion, mensaje):
    if not condicion:
        raise AssertionError(mensaje)


def probar_5(lab2, raiz):
    ruta = raiz / "eventos_todo5.jsonl"
    run_id = "prueba_aislada"
    esperados = [("operador", "ejecutar", "PERMITIDO"),
                 ("operador", "pipeline", "COMPLETADO"),
                 ("analista", "ejecutar", "DENEGADO")]
    for rol, operacion, resultado in esperados:
        lab2.registrar_evento(ruta, run_id, rol, operacion, resultado)
    contenido = ruta.read_text(encoding="utf-8")
    lineas = contenido.splitlines()
    exigir(len(lineas) == 3, "TODO 5: debes anexar tres eventos sin sobrescribir")
    exigir(contenido.endswith("\n"), "TODO 5: termina cada objeto JSON con un salto de linea")
    campos = {"run_id", "fecha_utc", "rol", "operacion", "resultado"}
    for linea, triple in zip(lineas, esperados):
        evento = json.loads(linea)
        exigir(isinstance(evento, dict) and set(evento) == campos,
               "TODO 5: cada linea debe tener los cinco campos exactos")
        exigir(all(isinstance(v, str) and v.strip() for v in evento.values()),
               "TODO 5: los valores deben ser textos no vacios")
        exigir(evento["run_id"] == run_id, "TODO 5: conserva el run_id recibido")
        exigir((evento["rol"], evento["operacion"], evento["resultado"]) == triple,
               "TODO 5: conserva los valores de la operacion recibida")
        fecha = datetime.fromisoformat(evento["fecha_utc"])
        exigir(fecha.tzinfo is not None and fecha.utcoffset() == timedelta(0),
               "TODO 5: fecha ISO con zona UTC")
        exigir(abs((datetime.now(timezone.utc) - fecha).total_seconds()) < 120,
               "TODO 5: genera la fecha actual, no una fecha fija")
    print("TODO 5 OK: tres eventos anexados con campos exactos y fecha UTC.")


def probar_6(lab2, raiz):
    # Datos de prueba propios: no utiliza registrar_evento ni TODO 7.
    ruta = raiz / "resumen_todo6.csv"
    ruta.write_text("ciudad,total_ventas\nMerida,4000.00\n", encoding="utf-8")
    exigir(lab2.comprobar_minimizacion(ruta) is True,
           "TODO 6: el resumen valido debe devolver True")
    invalidos = [
        "ciudad,total_ventas,correo\nMerida,4000.00,cliente@example.com\n",
        "ciudad,total_ventas\n",
        "total_ventas,ciudad\n4000.00,Merida\n",
        "",
        "ciudad,total_ventas\nMerida\n",
        "ciudad,total_ventas\nMerida,4000.00,extra\n",
    ]
    for contenido in invalidos:
        ruta.write_text(contenido, encoding="utf-8")
        exigir(lab2.comprobar_minimizacion(ruta) is False,
               "TODO 6: rechaza encabezados distintos, CSV vacio o filas incompletas")
    ruta.write_bytes(b"\xff\xfe\xfa")
    exigir(lab2.comprobar_minimizacion(ruta) is False,
           "TODO 6: un archivo que no puede leerse como UTF-8 devuelve False")
    exigir(lab2.comprobar_minimizacion(raiz / "ausente.csv") is False,
           "TODO 6: un archivo ausente debe devolver False")
    print("TODO 6 OK: resumen valido aceptado y ocho casos invalidos rechazados.")


def probar_7(lab2, raiz):
    # Fixtures propios: TODO 7 se prueba aunque TODO 5 y 6 sigan pendientes.
    ruta = raiz / "eventos_todo7.jsonl"
    run_id = "prueba_aislada"
    fecha = datetime.now(timezone.utc).isoformat()
    filas = [
        {"run_id": run_id, "fecha_utc": fecha, "rol": rol,
         "operacion": operacion, "resultado": resultado}
        for rol, operacion, resultado in [
            ("operador", "ejecutar", "PERMITIDO"),
            ("operador", "pipeline", "COMPLETADO"),
            ("analista", "ejecutar", "DENEGADO"),
        ]
    ]
    def escribir(registros):
        ruta.write_text("".join(json.dumps(r) + "\n" for r in registros), encoding="utf-8")
    escribir(filas)
    exigir(lab2.comprobar_trazabilidad(ruta, run_id) is True,
           "TODO 7: una traza completa y valida debe devolver True")
    variantes = [filas[:-1]]
    for campo, valor in [
        ("run_id", "otra_ejecucion"),
        ("correo", "cliente@example.com"),
        ("fecha_utc", "2026-10-26T10:00:00"),
        ("fecha_utc", "2026-10-26T10:00:00+01:00"),
        ("rol", "   "),
        ("resultado", None),
    ]:
        copia = [dict(r) for r in filas]
        copia[0][campo] = valor
        variantes.append(copia)
    copia = [dict(r) for r in filas]
    del copia[0]["resultado"]
    variantes.append(copia)
    for registros in variantes:
        escribir(registros)
        exigir(lab2.comprobar_trazabilidad(ruta, run_id) is False,
               "TODO 7: rechaza campos, valores, run_id o fecha invalidos y eventos ausentes")
    for contenido in ["no_es_json\n", "", "[]\n", "null\n"]:
        ruta.write_text(contenido, encoding="utf-8")
        exigir(lab2.comprobar_trazabilidad(ruta, run_id) is False,
               "TODO 7: rechaza JSON invalido, contenido vacio u objetos de otro tipo")
    ruta.write_bytes(b"\xff\xfe\xfa")
    exigir(lab2.comprobar_trazabilidad(ruta, run_id) is False,
           "TODO 7: un archivo que no puede leerse como UTF-8 devuelve False")
    exigir(lab2.comprobar_trazabilidad(raiz / "ausente.jsonl", run_id) is False,
           "TODO 7: un archivo ausente debe devolver False")
    print("TODO 7 OK: traza valida aceptada y catorce casos invalidos rechazados.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--todo", type=int, choices=[5, 6, 7],
                        help="Prueba solo la etapa seleccionada; sin opcion prueba 5, 6 y 7")
    args = parser.parse_args()
    numero = args.todo or 5
    try:
        import lab2
        exigir(Path(lab2.__file__).resolve().parent == Path(__file__).resolve().parent,
               "Coloca el comprobador junto a lab2.py y lab1.py")
        pruebas = {5: probar_5, 6: probar_6, 7: probar_7}
        with tempfile.TemporaryDirectory(prefix="nova_lab2_") as temp:
            for numero in ([args.todo] if args.todo else [5, 6, 7]):
                pruebas[numero](lab2, Path(temp))
        if args.todo:
            print(f"Etapa TODO {args.todo} verificada; no valida las otras funciones.")
        else:
            print("TODO 5, 6 y 7 verificados. Continua con la auditoria completa.")
        return 0
    except NotImplementedError:
        print(f"PENDIENTE: TODO {numero}; implementa y guarda esa funcion en lab2.py", file=sys.stderr)
        return 2
    except AssertionError as exc:
        print(f"REVISAR: {exc}", file=sys.stderr)
        return 1
    except ModuleNotFoundError:
        print("REVISAR: faltan lab1.py, lab2.py o las dependencias; consulta README.md", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"REVISAR TODO {numero}: {type(exc).__name__}; comprueba el contrato de errores", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
