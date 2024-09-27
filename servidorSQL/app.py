# app.py
from flask import Flask, request, make_response

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    # Pegando os dados do POST
    username = request.form.get('username')
    password = request.form.get('password')

    # Printando os dados recebidos para visualização (apenas para teste)
    print(f"Tentativa de login com Username: {username} e Password: {password}")

    # Simulando resposta de sucesso (sempre autorizando)
    response_html = "<h1>Autorizado</h1>"
    
    # Retornando resposta HTTP 200 com HTML "autorizado"
    return make_response(response_html, 200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
