from flask import Flask
from endpoints import register_endpoints

app = Flask(__name__)
register_endpoints(app)

if __name__ == '__main__':
    app.run(port=8080)