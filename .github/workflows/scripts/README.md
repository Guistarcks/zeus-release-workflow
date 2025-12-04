# Script `crear_release.py`

Este script permite crear un tag y un release en GitHub de forma automática utilizando la GitHub CLI (`gh`). Es ideal para integrarse en workflows de CI/CD, como GitHub Actions, para automatizar la publicación de releases.

## Requisitos

- Tener instalada la GitHub CLI (`gh`).
- El token de autenticación (`GH_TOKEN`) debe tener permisos de escritura sobre el repositorio.
- Python 3.6 o superior.

## Uso

```bash
python crear_release.py \
  --repo <owner/repo> \
  --version <tag> \
  --nombre_release "Nombre del release" \
  --descripcion "Descripción del release" \
  [--commits "commit1|||commit2|||commit3"]
```

### Argumentos

- `--repo`: Repositorio en formato `owner/repo` (ejemplo: `Guistarcks/zeus-release-workflow`).
- `--version`: Tag para el release (ejemplo: `v1.0.0`).
- `--nombre_release`: Nombre visible del release.
- `--descripcion`: Descripción del release. Si se usa `--commits`, el changelog se agregará automáticamente al final.
- `--commits` (opcional): String de commits separados por `|||`, cada uno en formato `mensaje` o `hash mensaje`. Si se provee, el script agrupa los mensajes por tipo (features, fixes, chores, etc.) y los añade como changelog.

## Ejemplo de integración en GitHub Actions

```yaml
- name: Crear tag y release
  env:
    GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  run: |
    COMMITS=$(git log --pretty=format:"%s" origin/main..origin/${{ github.event.pull_request.head.ref }} | paste -sd '|||' -)
    python .github/workflows/scripts/crear_release.py \
      --repo "${{ github.repository }}" \
      --version "$VERSION" \
      --nombre_release "Release $VERSION" \
      --descripcion "Release generado automáticamente desde ${{ github.event.pull_request.head.ref }}" \
      --commits "$COMMITS"
```

## Notas

- Si no se pasa el argumento `--commits`, solo se usará la descripción proporcionada.
- El script imprime mensajes de éxito o error en consola.
- El changelog se agrupa automáticamente si se pasan los commits en el formato adecuado.

---

Cualquier duda o mejora, puedes abrir un issue o PR en el repositorio.
