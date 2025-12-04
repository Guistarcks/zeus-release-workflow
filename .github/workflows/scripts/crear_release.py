import subprocess
import sys

def crear_tag_y_release(repo, version, nombre_release, descripcion, commits=None):
    """
    Función para crear un tag y un release en GitHub utilizando gh-cli.
    :param repo: El nombre del repositorio en formato 'owner/repo'.
    :param version: La versión para el nuevo tag (por ejemplo, 'v1.0.0').
    :param nombre_release: El nombre del release.
    :param descripcion: Descripción del release.
    :param commits: String de commits delimitados por '|||', cada uno en formato 'hash mensaje'
    """
    changelog = ""
    if commits:
        if isinstance(commits, list):
            commits_str = commits[0] if commits else ""
        else:
            commits_str = commits
        commit_lines = [c for c in commits_str.split('|||') if c.strip()]
        features = []
        fixes = []
        improvements = []
        chores = []
        breaking = []
        others = []
        for line in commit_lines:
            parts = line.strip().split(' ', 1)
            if len(parts) != 2:
                continue
            hash_, msg = parts
            if msg.startswith('feat'):
                features.append(f"{hash_} {msg}")
            elif msg.startswith('fix'):
                fixes.append(f"{hash_} {msg}")
            elif msg.startswith('chore'):
                chores.append(f"{hash_} {msg}")
            elif msg.startswith('refactor') or msg.startswith('test') or msg.startswith('perf'):
                improvements.append(f"{hash_} {msg}")
            elif msg.startswith('BREAKING'):
                breaking.append(f"{hash_} {msg}")
            else:
                others.append(f"{hash_} {msg}")
        if breaking:
            changelog += "BREAKING CHANGES\n" + "\n".join(breaking) + "\n"
        if features:
            changelog += "Features\n" + "\n".join(features) + "\n"
        if fixes:
            changelog += "Fixes\n" + "\n".join(fixes) + "\n"
        if improvements:
            changelog += "Improvements\n" + "\n".join(improvements) + "\n"
        if chores:
            changelog += "Chores\n" + "\n".join(chores) + "\n"
        if others:
            changelog += "Others\n" + "\n".join(others) + "\n"
        descripcion = f"{descripcion}\n\nChangelog:\n{changelog}"
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
    parser.add_argument('--commits', help='String de commits delimitados por "|||"')
    args = parser.parse_args()

    # Crear tag y release
    crear_tag_y_release(args.repo, args.version, args.nombre_release, args.descripcion, args.commits)

if __name__ == "__main__":
    main()
