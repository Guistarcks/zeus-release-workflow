#!/usr/bin/env python3
"""
Script para crear releases en GitHub usando gh-cli.
Utiliza la información del PR mergeado en lugar de commits individuales.
"""

import argparse
import subprocess
import sys
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def validar_version(version: str) -> bool:
    """Valida que la versión tenga formato semver."""
    pattern = r'^v?\d+\.\d+\.\d+(-[\w.]+)?$'
    return bool(re.match(pattern, version))


def validar_repo(repo: str) -> bool:
    """Valida que el repo tenga formato owner/repo."""
    pattern = r'^[\w.-]+/[\w.-]+$'
    return bool(re.match(pattern, repo))


def generar_descripcion(
    pr_title: str | None,
    pr_number: str | None,
    pr_body: str | None,
    branch: str | None,
    repo: str
) -> str:
    """
    Genera la descripción del release basada en el PR.
    """
    lines = []

    # Header con información del PR
    if pr_title and pr_number:
        lines.append(f"## {pr_title}")
        lines.append(f"PR: [#{pr_number}](https://github.com/{repo}/pull/{pr_number})")

    # Tipo de release basado en la rama
    if branch:
        if branch.startswith('hotfix'):
            lines.append("\n> 🔧 **Hotfix Release**")
        elif branch.startswith('release'):
            lines.append("\n> 🚀 **Release**")

    # Contenido del PR (descripción del autor)
    if pr_body and pr_body.strip():
        lines.append("\n### Descripción")
        lines.append(pr_body.strip())

    # Footer
    lines.append("\n---")
    lines.append("*Release generado automáticamente*")

    return "\n".join(lines)


def crear_release(
    repo: str,
    version: str,
    nombre_release: str,
    descripcion: str
) -> None:
    """
    Crea un release en GitHub utilizando gh-cli.
    """
    # Validaciones
    if not validar_repo(repo):
        logger.error(f"Formato de repositorio inválido: {repo}")
        sys.exit(1)

    if not validar_version(version):
        logger.error(f"Formato de versión inválido: {version}")
        sys.exit(1)

    try:
        cmd = [
            'gh', 'release', 'create', version,
            '--repo', repo,
            '--title', nombre_release,
            '--notes', descripcion
        ]

        subprocess.check_call(cmd)
        logger.info(f"Release '{nombre_release}' creado correctamente en '{repo}'")

    except FileNotFoundError:
        logger.error("gh-cli no está instalado. Instálalo con: https://cli.github.com/")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error al crear el release: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Crear un release en GitHub basado en información del PR'
    )
    parser.add_argument(
        '--repo',
        required=True,
        help="Repositorio en formato 'owner/repo'"
    )
    parser.add_argument(
        '--version',
        required=True,
        help='Tag/versión para el release (ej: v1.0.0)'
    )
    parser.add_argument(
        '--nombre_release',
        required=True,
        help='Nombre del release'
    )
    parser.add_argument(
        '--pr-title',
        help='Título del PR mergeado'
    )
    parser.add_argument(
        '--pr-number',
        help='Número del PR mergeado'
    )
    parser.add_argument(
        '--pr-body',
        help='Descripción/body del PR mergeado'
    )
    parser.add_argument(
        '--branch',
        help='Rama origen del PR (hotfix/*, release/*)'
    )

    args = parser.parse_args()

    # Generar descripción basada en el PR
    descripcion = generar_descripcion(
        pr_title=args.pr_title,
        pr_number=args.pr_number,
        pr_body=args.pr_body,
        branch=args.branch,
        repo=args.repo
    )

    # Crear el release
    crear_release(
        repo=args.repo,
        version=args.version,
        nombre_release=args.nombre_release,
        descripcion=descripcion
    )


if __name__ == "__main__":
    main()
