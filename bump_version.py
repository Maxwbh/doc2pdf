#!/usr/bin/env python3
"""
Script para incrementar automaticamente a versão do projeto

Uso:
    python bump_version.py patch  # 1.0.0 -> 1.0.1
    python bump_version.py minor  # 1.0.0 -> 1.1.0
    python bump_version.py major  # 1.0.0 -> 2.0.0

Autor: Maxwell da Silva Oliveira - M&S do Brasil LTDA
"""

import re
import sys
from pathlib import Path
from datetime import date


def get_current_version():
    """Lê a versão atual do arquivo version.py"""
    version_file = Path("version.py")
    content = version_file.read_text()
    match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    if match:
        return match.group(1)
    raise ValueError("Versão não encontrada em version.py")


def bump_version(current_version, bump_type):
    """Incrementa a versão baseado no tipo (major, minor, patch)"""
    major, minor, patch = map(int, current_version.split('.'))

    if bump_type == 'major':
        return f"{major + 1}.0.0"
    elif bump_type == 'minor':
        return f"{major}.{minor + 1}.0"
    elif bump_type == 'patch':
        return f"{major}.{minor}.{patch + 1}"
    else:
        raise ValueError("Tipo de bump inválido. Use: major, minor ou patch")


def update_version_file(new_version):
    """Atualiza o arquivo version.py com a nova versão"""
    version_file = Path("version.py")
    content = version_file.read_text()
    content = re.sub(
        r'__version__\s*=\s*["\'][^"\']+["\']',
        f'__version__ = "{new_version}"',
        content
    )
    version_file.write_text(content)
    print(f"✅ Atualizado version.py para v{new_version}")


def update_changelog(new_version):
    """Adiciona entrada no CHANGELOG.md para a nova versão"""
    changelog_file = Path("CHANGELOG.md")
    content = changelog_file.read_text()

    today = date.today().strftime("%Y-%m-%d")

    # Adiciona nova entrada após o cabeçalho
    new_entry = f"""
## [{new_version}] - {today}

### Adicionado
-

### Alterado
-

### Corrigido
-

"""

    # Insere após a primeira ocorrência de "## ["
    parts = content.split("## [", 1)
    if len(parts) == 2:
        content = parts[0] + new_entry + "## [" + parts[1]
        changelog_file.write_text(content)
        print(f"✅ Adicionada entrada no CHANGELOG.md para v{new_version}")
    else:
        print("⚠️  Não foi possível atualizar o CHANGELOG.md automaticamente")


def main():
    """Função principal"""
    if len(sys.argv) != 2:
        print("Uso: python bump_version.py [major|minor|patch]")
        print("\nExemplos:")
        print("  python bump_version.py patch  # 1.0.0 -> 1.0.1")
        print("  python bump_version.py minor  # 1.0.0 -> 1.1.0")
        print("  python bump_version.py major  # 1.0.0 -> 2.0.0")
        sys.exit(1)

    bump_type = sys.argv[1].lower()

    if bump_type not in ['major', 'minor', 'patch']:
        print("❌ Tipo de bump inválido. Use: major, minor ou patch")
        sys.exit(1)

    try:
        # Lê versão atual
        current_version = get_current_version()
        print(f"📦 Versão atual: {current_version}")

        # Calcula nova versão
        new_version = bump_version(current_version, bump_type)
        print(f"🚀 Nova versão: {new_version}")

        # Atualiza arquivos
        update_version_file(new_version)
        update_changelog(new_version)

        print("\n✨ Versão incrementada com sucesso!")
        print(f"\nPróximos passos:")
        print(f"1. Atualize o CHANGELOG.md com as mudanças da v{new_version}")
        print(f"2. git add version.py CHANGELOG.md")
        print(f"3. git commit -m 'chore: bump version to {new_version}'")
        print(f"4. git tag v{new_version}")
        print(f"5. git push && git push --tags")

    except Exception as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
