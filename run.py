from app import app
from os import urandom

if __name__ == '__main__':
    app.secret_key = urandom(12)
    app.run()