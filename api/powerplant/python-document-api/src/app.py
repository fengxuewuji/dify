from flask import Flask
from src.routes.word_routes import word_routes
from src.routes.pdf_routes import pdf_routes

app = Flask(__name__)

app.register_blueprint(word_routes)
app.register_blueprint(pdf_routes)

if __name__ == '__main__':
    app.run(debug=True)