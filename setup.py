"""
Setup configuration for DOC2PDF API
"""

from setuptools import setup, find_packages
from pathlib import Path

# Lê o README para a descrição longa
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Importa informações de versão
exec(open('version.py').read())

setup(
    name="doc2pdf-api",
    version=__version__,
    author=__author__,
    author_email=__email__,
    description="API Flask para conversão de documentos Word para PDF com substituição de tags",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Maxwbh/doc2pdf",
    project_urls={
        "Bug Tracker": "https://github.com/Maxwbh/doc2pdf/issues",
        "Documentation": "https://github.com/Maxwbh/doc2pdf#readme",
        "Source Code": "https://github.com/Maxwbh/doc2pdf",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Framework :: Flask",
        "Topic :: Office/Business",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.9",
    install_requires=[
        "Flask>=3.0.0",
        "flask-cors>=4.0.0",
        "python-docx>=1.1.0",
        "gunicorn>=21.2.0",
        "Werkzeug>=3.0.1",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "doc2pdf-api=app:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="pdf word docx conversion flask api document-processing",
    license=__license__,
)
