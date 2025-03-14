from app import create_app
from app.modelo_db import db

# Criar a aplicação
app = create_app()

# Rodar o servidor
if __name__ == "__main__":
    app.run(debug=True)
