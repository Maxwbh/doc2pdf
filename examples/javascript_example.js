/**
 * Exemplos de uso da API DOC2PDF em JavaScript/Node.js
 * Autor: Maxwell da Silva Oliveira - M&S do Brasil LTDA
 */

const axios = require('axios');
const fs = require('fs');

const API_URL = 'http://localhost:5000';  // Ajuste conforme necessário

// Codifica arquivo para Base64
function encodeFileToBase64(filePath) {
    const file = fs.readFileSync(filePath);
    return file.toString('base64');
}

// Salva Base64 em arquivo
function saveBase64ToFile(base64String, outputPath) {
    const buffer = Buffer.from(base64String, 'base64');
    fs.writeFileSync(outputPath, buffer);
}

// Exemplo 1: /convert
async function exemploConvert() {
    console.log('='.repeat(60));
    console.log('EXEMPLO 1: Endpoint /convert');
    console.log('='.repeat(60));

    const docBase64 = encodeFileToBase64('template.docx');

    const payload = {
        document: docBase64,
        replacements: {
            NOME: 'João Silva',
            CPF: '123.456.789-00',
            DATA: '05/12/2025'
        },
        quality: 'high'
    };

    try {
        const response = await axios.post(`${API_URL}/convert`, payload);
        console.log('✓ Sucesso!');
        console.log(`  Tempo: ${response.data.processing_time}s`);
        console.log(`  Qualidade: ${response.data.stats.quality}`);

        saveBase64ToFile(response.data.pdf, 'output.pdf');
        console.log('✓ PDF salvo em: output.pdf');
    } catch (error) {
        console.error('✗ Erro:', error.response?.data || error.message);
    }
}

// Exemplo 2: /convert-file
async function exemploConvertFile() {
    console.log('\n' + '='.repeat(60));
    console.log('EXEMPLO 2: Endpoint /convert-file');
    console.log('='.repeat(60));

    const docBase64 = encodeFileToBase64('template.docx');

    const payload = {
        document: docBase64,
        replacements: {
            TITULO: 'Contrato de Serviços',
            VALOR: 'R$ 10.000,00'
        },
        filename: 'contrato.pdf',
        quality: 'medium'
    };

    try {
        const response = await axios.post(`${API_URL}/convert-file`, payload, {
            responseType: 'arraybuffer'
        });

        fs.writeFileSync('contrato.pdf', response.data);
        console.log('✓ PDF salvo em: contrato.pdf');
    } catch (error) {
        console.error('✗ Erro:', error.response?.data || error.message);
    }
}

// Executa exemplos
async function main() {
    console.log('\n╔══════════════════════════════════════╗');
    console.log('║  API DOC2PDF - Exemplos JS v1.5.0   ║');
    console.log('╚══════════════════════════════════════╝\n');

    try {
        // Health check
        const health = await axios.get(`${API_URL}/health`);
        console.log(`✓ API Online: ${health.data.service} v${health.data.version}\n`);

        // Executa exemplos
        await exemploConvert();
        await exemploConvertFile();

        console.log('\n' + '='.repeat(60));
        console.log('✓ Exemplos concluídos!');
        console.log('='.repeat(60));
    } catch (error) {
        console.error('✗ Erro ao conectar:', error.message);
        console.error(`  Verifique se a API está rodando em ${API_URL}`);
    }
}

main();
