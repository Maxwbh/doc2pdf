"""
DOC2PDF Converter API - Entry Point

API REST profissional para conversão de documentos Word para PDF
com substituição inteligente de tags.

Autor: Maxwell da Silva Oliveira
Email: maxwbh@gmail.com
Empresa: M&S do Brasil LTDA
LinkedIn: /maxwbh

Versão: 1.5.0
"""
from app import create_app

# Cria a aplicação usando factory pattern
app = create_app()

if __name__ == '__main__':
    # Roda apenas em desenvolvimento
    # Em produção, use Gunicorn
    app.run(debug=False, host='0.0.0.0', port=5000)
