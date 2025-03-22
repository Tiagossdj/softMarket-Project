from datetime import datetime, timedelta
from flask import Blueprint, Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from app.modelo_db import Usuario, db
from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import jsonify
from flask_jwt_extended import get_jwt


registra_usuario = Blueprint("registra_usuario", __name__)


@registra_usuario.route("/register", methods=["POST"])
def register():
    try:
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        confirm_password = request.json.get("confirm_password", None)
        role = request.json.get("role", None)  # "gerente" ou "funcionario"

        if not username or not password or not confirm_password:
            return (
                jsonify(
                    {"msg": "Usuário, senha e confirmação de senha são obrigatórios"}
                ),
                400,
            )

        if password != confirm_password:
            return jsonify({"msg": "As senhas não coincidem"}), 400

        if role not in ["gerente", "funcionario"]:
            return jsonify({"msg": "Role inválido"}), 400

        # Verifica se o usuário já existe
        user = Usuario.query.filter_by(username=username).first()
        if user:
            return jsonify({"msg": "Usuário já existe"}), 400

        # Cria o novo usuário e criptografa a senha
        new_user = Usuario(username=username, role=role)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"msg": "Usuário registrado com sucesso!"}), 201

    except Exception as e:
        print(f"Erro ao registrar usuário: {e}")
        return jsonify({"msg": "Ocorreu um erro ao registrar o usuário"}), 500


@registra_usuario.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username or not password:
        return jsonify({"msg": "Usuário e senha são obrigatórios"}), 400

    # Verifica se o usuário existe
    user = Usuario.query.filter_by(username=username).first()

    if user and user.check_password(password):
        # Gera o token JWT com o role do usuário
        access_token = create_access_token(
            identity=user.id,
            additional_claims={"username": user.username, "role": user.role.value},
        )
        return jsonify(access_token=access_token), 200

    else:
        return jsonify({"msg": "Credenciais inválidas"}), 401


def role_required(required_role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            claims = get_jwt()
            user_role = claims.get("role")
            if user_role != required_role:
                return jsonify({"msg": "Acesso negado, você não tem permissão."}), 403
            return fn(*args, **kwargs)

        return decorator

    return wrapper


@registra_usuario.route("/gerente_dashboard", methods=["GET"])
@jwt_required()
@role_required("gerente")
def gerente_dashboard():
    return jsonify({"msg": "Bem-vindo ao painel do gerente!"}), 200


@registra_usuario.route("/funcionario_dashboard", methods=["GET"])
@jwt_required()
@role_required("funcionario")  # Restringe a rota para funcionários
def funcionario_dashboard():
    return jsonify({"msg": "Bem-vindo ao painel do funcionário!"}), 200


## PERMISSÕES

PERMISSOES = {
    "gerente": ["estoque", "vendas", "relatorios", "produtos"],
    "funcionario": [
        "vendas",
        "produtos",
    ],  # Funcionario só pode acessar vendas e produtos
}


def tem_permissao(permissao):
    # Obtém o identity (user_id)
    user_id = get_jwt_identity()
    # Obtém as claims completas
    claims = get_jwt()
    user_role = claims.get("role")

    # Verifica se a permissão está disponível para o papel do usuário
    if permissao in PERMISSOES.get(user_role, []):
        return True
    return False
