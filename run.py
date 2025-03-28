from flask import Flask
from app import create_app

# Criar a aplicação
app = create_app()

app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)
