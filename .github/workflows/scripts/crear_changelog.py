import os
import datetime

def obtener_fecha_actual():
    """Obtiene la fecha actual en el formato adecuado para el changelog."""
    return datetime.datetime.now().strftime("%Y-%m-%d")

def obtener_changelog_path():
    """Devuelve la ruta al archivo CHANGELOG.md."""
    return "CHANGELOG.md"

def crear_o_actualizar_changelog(version, descripcion, changelog_path):
    """Crea o actualiza el archivo CHANGELOG.md con la nueva entrada de release."""
    fecha_actual = obtener_fecha_actual()

    # Verificar si el changelog ya existe
    if os.path.exists(changelog_path):
        # Si el changelog existe, leerlo
        with open(changelog_path, 'r') as f:
            changelog_contenido = f.read()

        # Verificar si la versión ya está registrada (para evitar duplicados)
        if f"## [{version}]" in changelog_contenido:
            print(f"El changelog ya contiene una entrada para la versión {version}.")
            return
        else:
            # Agregar una nueva entrada al final
            with open(changelog_path, 'a') as f:
                f.write(f"\n## [{version}] - {fecha_actual}\n")
                f.write(f"{descripcion}\n")
            print(f"Changelog actualizado con la versión {version}.")
    else:
        # Si el changelog no existe, crearlo desde cero
        with open(changelog_path, 'w') as f:
            f.write("# Changelog\n\n")
            f.write("Todas las novedades de este proyecto seguirán el formato del changelog.\n\n")
            f.write(f"## [{version}] - {fecha_actual}\n")
            f.write(f"{descripcion}\n")
        print(f"Changelog creado para la versión {version}.")

def generar_descripcion_release(version):
    """Genera una descripción del release de acuerdo con las mejores prácticas de GitHub."""
    # Se pueden agregar las secciones automáticamente, por ejemplo, al realizar un release desde un workflow de CI.
    descripcion = (
        f"### Notas para la versión {version}\n"
        "\n"
        "#### Añadido\n"
        "- Nuevas funcionalidades o características.\n"
        "\n"
        "#### Cambiado\n"
        "- Cambios o mejoras de funcionalidades existentes.\n"
        "\n"
        "#### Arreglado\n"
        "- Correcciones de errores.\n"
        "\n"
        "#### Deprecado\n"
        "- Funcionalidades descontinuadas.\n"
        "\n"
        "#### Eliminado\n"
        "- Funcionalidades eliminadas.\n"
        "\n"
        "#### Seguridad\n"
        "- Mejoras relacionadas con la seguridad.\n"
    )
    return descripcion

def main():
    # Variables necesarias
    version = "v1.0.0"  # Cambia esto según el release que estás manejando
    changelog_path = obtener_changelog_path()

    # Generar la descripción para el changelog
    descripcion = generar_descripcion_release(version)

    # Crear o actualizar el changelog
    crear_o_actualizar_changelog(version, descripcion, changelog_path)

if __name__ == "__main__":
    main()
