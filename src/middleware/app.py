from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Função para análise de currículo (simulação)
def analisar_curriculo(file):
    # Aqui você pode adicionar a lógica de análise do currículo.
    # Neste exemplo, retornamos uma análise fictícia.
    return {
        "status": "sucesso",
        "score": 85,
        "feedback": "Currículo bem estruturado e com boas habilidades."
    }

@app.route('/process', methods=['POST'])
def processar_curriculo():
    if 'file_name' not in request.json:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    file_name = request.json['file_name']
    
    try:
        # Simulação de leitura e análise do currículo
        resultado = analisar_curriculo(file_name)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": f"Erro ao processar o arquivo: {str(e)}"}), 500

if __name__ == '__main__':
    # Rodando o servidor Flask
    app.run(debug=True, host='0.0.0.0', port=8000)
