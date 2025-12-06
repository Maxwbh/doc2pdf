#!/bin/bash
#
# Exemplos de uso da API DOC2PDF com cURL
# Autor: Maxwell da Silva Oliveira - M&S do Brasil LTDA
#

API_URL="http://localhost:5000"  # Ajuste conforme necessário

# Codifica arquivo para Base64
encode_file() {
    base64 -w 0 "$1"
}

echo "========================================"
echo "  API DOC2PDF - Exemplos cURL v1.5.0"
echo "========================================"

# Health check
echo -e "\n1. Health Check"
curl -s "$API_URL/health" | jq .

# Exemplo /convert
echo -e "\n2. Endpoint /convert (retorna Base64)"
DOC_BASE64=$(encode_file "template.docx")
curl -X POST "$API_URL/convert" \
  -H "Content-Type: application/json" \
  -d "{
    \"document\": \"$DOC_BASE64\",
    \"replacements\": {
      \"NOME\": \"João Silva\",
      \"CPF\": \"123.456.789-00\"
    },
    \"quality\": \"high\"
  }" | jq .

# Exemplo /convert-file
echo -e "\n3. Endpoint /convert-file (retorna arquivo)"
curl -X POST "$API_URL/convert-file" \
  -H "Content-Type: application/json" \
  -d "{
    \"document\": \"$DOC_BASE64\",
    \"replacements\": {
      \"TITULO\": \"Contrato de Serviços\"
    },
    \"filename\": \"contrato.pdf\",
    \"quality\": \"medium\"
  }" -o "output.pdf"

echo "✓ PDF salvo em output.pdf"

# Exemplo /process
echo -e "\n4. Endpoint /process (flexível)"
curl -X POST "$API_URL/process" \
  -H "Content-Type: application/json" \
  -d "{
    \"document\": \"$DOC_BASE64\",
    \"replacements\": {
      \"TAG\": \"valor\"
    },
    \"input_type\": \"base64\",
    \"output_type\": \"base64_pdf\",
    \"quality\": \"low\"
  }" | jq .

echo -e "\n✓ Exemplos concluídos!"
