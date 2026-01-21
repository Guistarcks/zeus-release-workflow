#!/usr/bin/env python3
"""
Script para crear o actualizar el archivo CHANGELOG.md.
Utiliza la información del PR mergeado para generar entradas limpias.
"""

import argparse
import logging
import os
import re
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

CHANGELOG_HEADER = """# Changelog

Todas las novedades de este proyecto seguirán el formato [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/).

"""


def validar_version(version: str) -> bool:
    """Valida que la versión tenga formato semver."""
    pattern = r'^v?\d+\.\d+\.\d+(-[\w.]+)?$'
    return bool(re.match(pattern, version))


def obtener_repo_root() -> Path:
    """
    Encuentra la raíz del repositorio.
    Prioriza GITHUB_WORKSPACE (CI), luego busca .git.
    """
    # En GitHub Actions
    if 'GITHUB_WORKSPACE' in os.environ:
        return Path(os.environ['GITHUB_WORKSPACE'])

    # Buscar .git en directorios padre
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / '.git').exists():
            return parent

    # Fallback: 4 niveles arriba (estructura .github/workflows/scripts/)
    return current.parent.parent.parent.parent


def obtener_fecha_actual() -> str:
    """Obtiene la fecha actual en formato ISO."""
    return datetime.now().strftime("%Y-%m-%d")


def generar_entrada_changelog(
    version: str,
    pr_title: str | None,
    pr_number: str | None,
    pr_body: str | None,
    branch: str | None,
    repo: str | None
) -> str:
    """
    Genera una entrada de changelog basada en el PR.
    """
    fecha = obtener_fecha_actual()
    lines = [f"## [{version}] - {fecha}\n"]

    # Título del PR como header
    if pr_title:
        lines.append(f"### {pr_title}")
        if pr_number and repo:
            lines.append(f"PR: [#{pr_number}](https://github.com/{repo}/pull/{pr_number})\n")
        elif pr_number:
            lines.append(f"PR: #{pr_number}\n")

    # Tipo de cambio basado en la rama
    if branch:
        if branch.startswith('hotfix'):
            lines.append("> Hotfix release\n")
        elif branch.startswith('release'):
            lines.append("> Release\n")

    # Contenido del PR
    if pr_body and pr_body.strip():
        lines.append(pr_body.strip())

    lines.append("")  # Línea en blanco al final
    return "\n".join(lines)


def version_existe(contenido: str, version: str) -> bool:
    """Verifica si la versión ya existe en el changelog."""
    # Buscar [version] o [vX.Y.Z]
    version_clean = version.lstrip('v')
    pattern = rf'\[v?{re.escape(version_clean)}\]'
    return bool(re.search(pattern, contenido))


def actualizar_changelog(
    changelog_path: Path,
    nueva_entrada: str,
    version: str
) -> bool:
    """
    Actualiza el CHANGELOG.md insertando la nueva versión al inicio.
    Retorna True si se actualizó, False si la versión ya existía.
    """
    if changelog_path.exists():
        contenido = changelog_path.read_text(encoding='utf-8')

        # Verificar si la versión ya existe
        if version_existe(contenido, version):
            logger.warning(f"La versión {version} ya existe en el changelog")
            return False

        # Encontrar donde termina el header para insertar después
        # Buscamos la primera línea que empieza con "## ["
        lineas = contenido.split('\n')
        insert_index = 0

        for i, linea in enumerate(lineas):
            if linea.startswith('## ['):
                insert_index = i
                break
            insert_index = i + 1

        # Insertar la nueva entrada
        lineas_nuevas = lineas[:insert_index] + [nueva_entrada] + lineas[insert_index:]
        nuevo_contenido = '\n'.join(lineas_nuevas)

    else:
        # Crear nuevo changelog
        nuevo_contenido = CHANGELOG_HEADER + nueva_entrada

    # Escribir el archivo
    changelog_path.write_text(nuevo_contenido, encoding='utf-8')
    logger.info(f"Changelog actualizado con la versión {version}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Crear o actualizar el CHANGELOG.md basado en información del PR'
    )
    parser.add_argument(
        '--version',
        required=True,
        help='Tag/versión para el changelog (ej: v1.0.0)'
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
    parser.add_argument(
        '--repo',
        help="Repositorio en formato 'owner/repo' para generar links"
    )

    args = parser.parse_args()

    # Validar versión
    if not validar_version(args.version):
        logger.error(f"Formato de versión inválido: {args.version}")
        return 1

    # Obtener path del changelog
    repo_root = obtener_repo_root()
    changelog_path = repo_root / 'CHANGELOG.md'

    # Generar entrada
    entrada = generar_entrada_changelog(
        version=args.version,
        pr_title=args.pr_title,
        pr_number=args.pr_number,
        pr_body=args.pr_body,
        branch=args.branch,
        repo=args.repo
    )

    # Actualizar changelog
    actualizar_changelog(changelog_path, entrada, args.version)
    return 0


if __name__ == "__main__":
    exit(main())
