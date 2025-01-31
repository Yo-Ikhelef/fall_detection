from flask import Flask

def create_app():
    app = Flask(__name__)


    from app.routes import setup_routes
    setup_routes(app)  

    return app


# --------------------------------------------------------

# from flask import Flask

# app = Flask(__name__)

# from app.routes import *

