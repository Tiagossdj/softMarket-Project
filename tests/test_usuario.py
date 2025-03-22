import json


# Teste de Registro
def test_register(client):
    # Dados para o registro do usuário
    register_data = {
        "username": "teste_usuario",
        "password": "senha123",
        "confirm_password": "senha123",
        "role": "gerente",
    }

    # Envia uma requisição POST para o endpoint de registro
    response = client.post("/auth/register", json=register_data)

    # Verifica se o status do response é 201 (Criado)
    assert response.status_code == 201

    data = json.loads(response.data)
    assert "msg" in data
    assert data["msg"] == "Usuário registrado com sucesso!"


def test_login(client):
    # Cria um usuário com nome único para este teste
    import uuid

    unique_username = f"login_teste_{uuid.uuid4().hex[:8]}"

    # Registra o usuário
    register_data = {
        "username": unique_username,
        "password": "senha123",
        "confirm_password": "senha123",
        "role": "gerente",
    }
    register_response = client.post("/auth/register", json=register_data)
    print(f"Register status code: {register_response.status_code}")
    print(f"Register data: {register_response.data}")

    # Tenta fazer login
    login_data = {"username": unique_username, "password": "senha123"}
    login_response = client.post("/auth/login", json=login_data)
    print(f"Login status code: {login_response.status_code}")
    print(f"Login data: {login_response.data}")

    assert login_response.status_code == 200
    data = json.loads(login_response.data)
    assert "access_token" in data
