from flask import Blueprint, request, jsonify
from app import db
from app.modelo_db import Compra
from datetime import datetime

realiza_compra = Blueprint("realiza_compra", __name__)


@realiza_compra.route("/realizaCompra", methods=["POST"])
def realiza_compra_func():
    try:
        data = request.get_json()
        cliente_id = data["cliente_id"]
        data_compra = datetime.fromisoformat(data["data"])
        total = data["total"]

        # Criar uma nova compra
        nova_compra = Compra(cliente_id=cliente_id, data=data_compra, total=total)

        # Adicionar a compra ao banco
        db.session.add(nova_compra)
        db.session.commit()

        return jsonify({"message": "Compra realizada com sucesso!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
