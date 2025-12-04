import subprocess
import sys

def crear_tag_y_release(repo, version, nombre_release, descripcion):
    """
    Función para crear un tag y un release en GitHub utilizando gh-cli.
    
    :param repo: El nombre del repositorio en formato 'owner/repo'.
    :param version: La versión para el nuevo tag (por ejemplo, 'v1.0.0').
    :param nombre_release: El nombre del release.
    :param descripcion: Descripción del release.
    """
    # 1. Crear un tag
    try:
        subprocess.check_call(['gh', 'release', 'create', version, '--repo', repo, '--title', nombre_release, '--notes', descripcion])
        print(f"Release '{nombre_release}' con tag '{version}' creado correctamente en el repositorio '{repo}'.")
    except subprocess.CalledProcessError as e:
        print(f"Error al crear el release: {e}")
        sys.exit(1)

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Crear un release en GitHub')
    parser.add_argument('--repo', required=True, help="Repositorio en formato 'owner/repo'")
    parser.add_argument('--version', required=True, help='Tag/version para el release')
    parser.add_argument('--nombre_release', required=True, help='Nombre del release')
    parser.add_argument('--descripcion', required=True, help='Descripción del release')
    args = parser.parse_args()

    # Crear tag y release
    crear_tag_y_release(args.repo, args.version, args.nombre_release, args.descripcion)

if __name__ == "__main__":
    main()
