// Função para consultar o cliente
function consultarCliente() {
    const cpf = document.getElementById('cpfConsulta').value;
    fetch(`/api/consulta?cpf=${cpf}`)
        .then(response => response.json())
        .then(data => {
            const dadosDiv = document.getElementById('dadosCliente');
            if (data.error) {
                dadosDiv.innerHTML = `<p class="error">${data.error}</p>`;
            } else {
                dadosDiv.innerHTML = `
                    <p><strong>Nome:</strong> ${data.nome}</p>
                    <p><strong>Data de Nascimento:</strong> ${data.nascimento}</p>
                    <p><strong>E-mail:</strong> ${data.email}</p>
                `;
            }
        })
        .catch(error => console.error('Erro:', error));
}

// Função para cadastrar um novo cliente
function cadastrarCliente() {
    const cpf = document.getElementById('cpfCadastro').value;
    const nome = document.getElementById('nomeCadastro').value;
    const nascimento = document.getElementById('nascimentoCadastro').value;
    const email = document.getElementById('emailCadastro').value;

    const cliente = { cpf, nome, nascimento, email };

    fetch('/api/cadastrar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(cliente)
    })
    .then(response => response.json())
    .then(data => {
        const mensagemDiv = document.getElementById('mensagemCadastro');
        if (data.error) {
            mensagemDiv.innerHTML = `<p class="error">${data.error}</p>`;
        } else {
            mensagemDiv.innerHTML = `<p class="success">${data.message}</p>`;
        }
    })
    .catch(error => console.error('Erro:', error));
}
