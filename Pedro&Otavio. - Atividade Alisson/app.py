from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)

# Função para ler o arquivo JSON com os dados dos clientes
def load_clients():
    try:
        # Obtém o diretório onde o app.py está localizado
        app_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Cria o caminho correto para o arquivo 'clientes.json'
        data_path = os.path.join(app_dir, 'data', 'clientes.json')
        
        # Abre o arquivo JSON para leitura
        with open(data_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    except FileNotFoundError:
        print(f"Erro: O arquivo 'clientes.json' não foi encontrado no caminho: {data_path}")
        return []  # Retorna uma lista vazia se o arquivo não for encontrado
    except json.JSONDecodeError:
        print(f"Erro: O arquivo 'clientes.json' está mal formatado!")
        return []  # Retorna uma lista vazia se o arquivo JSON estiver mal formatado
    except Exception as e:
        print(f"Erro ao carregar o arquivo de clientes: {e}")
        return []  # Retorna uma lista vazia em caso de outros erros

def save_clients(clients):
    try:
        # Obtém o diretório onde o app.py está localizado
        app_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Cria o caminho correto para o arquivo 'clientes.json'
        data_path = os.path.join(app_dir, 'data', 'clientes.json')
        
        # Abre o arquivo em modo de escrita (substitui o conteúdo)
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(clients, f, indent=4, ensure_ascii=False)
    
    except Exception as e:
        print(f"Erro ao salvar os dados: {e}")

# Rota para a página inicial (consultar e cadastrar clientes)
@app.route('/')
def index():
    return render_template('index.html')

# Rota para consulta de cliente por CPF
@app.route('/api/consulta', methods=['GET'])
def consulta_cliente():
    cpf = request.args.get('cpf')
    if not cpf:
        return jsonify({'error': 'CPF é obrigatório'}), 400
    
    clients = load_clients()
    client = next((c for c in clients if c['cpf'] == cpf), None)
    
    if client:
        return jsonify(client)
    else:
        return jsonify({'error': 'Cliente não encontrado'}), 404

# Rota para cadastrar um novo cliente
@app.route('/api/cadastrar', methods=['POST'])
def cadastrar_cliente():
    data = request.json
    cpf = data.get('cpf')
    nome = data.get('nome')
    nascimento = data.get('nascimento')
    email = data.get('email')
    
    # Verifica se todos os campos necessários estão presentes
    if not cpf or not nome or not nascimento or not email:
        return jsonify({'error': 'Todos os campos são obrigatórios'}), 400
    
    # Carrega os clientes existentes
    clients = load_clients()

    # Verifica se o CPF já existe
    if any(c['cpf'] == cpf for c in clients):
        return jsonify({'error': 'CPF já cadastrado'}), 400
    
    # Adiciona o novo cliente
    new_client = {
        'cpf': cpf,
        'nome': nome,
        'nascimento': nascimento,
        'email': email
    }
    clients.append(new_client)
    
    # Ordena os clientes por nome
    clients.sort(key=lambda x: x['nome'])

    # Salva os clientes no arquivo JSON
    save_clients(clients)
    
    return jsonify({'message': 'Cliente cadastrado com sucesso'}), 201


if __name__ == '__main__':
    app.run(debug=True)
