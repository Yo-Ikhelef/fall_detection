
# from flask import Flask
# import threading
# from core.engine import Engine
# from app.routes import setup_routes 

# # Initialisation de Flask
# app = Flask(__name__)

# def create_app():
#     app = Flask(__name__)
#     setup_routes(app)
#     return app

# # Fonction pour démarrer Flask
# def run_flask():
#     app = create_app()
#     app.run(debug=False, host="0.0.0.0", port=8000, use_reloader=False)

# # Fonction pour démarrer l'engine
# def run_engine():
#     engine = Engine()
#     engine.run()

# if __name__ == "__main__":
#     # Lancer Flask et l'engine en parallèle
#     flask_thread = threading.Thread(target=run_flask, daemon=True)
#     engine_thread = threading.Thread(target=run_engine, daemon=True)

#     # Démarrage des threads
#     flask_thread.start()
#     engine_thread.start()

#     # Assurer que les deux threads fonctionnent
#     flask_thread.join()
#     engine_thread.join()

from flask import Flask
import threading
from core.engine import Engine
from app.routes import setup_routes
import time

# Initialisation de Flask
def create_app():
    app = Flask(__name__, static_folder="app/static", template_folder="app/templates")  # ✅ Indiquer où sont les templates
    setup_routes(app)
    return app

# Démarrer Flask normalement
app = create_app()

# Fonction pour démarrer l'engine en thread
def run_engine():
    print("🔥 Lancement de l'Engine...")  # ✅ Débogage
    time.sleep(3)  # Laisse le temps à Flask de se lancer
    engine = Engine()
    engine.run()

if __name__ == "__main__":
    # Démarrer l'engine dans un thread séparé
    engine_thread = threading.Thread(target=run_engine, daemon=True)
    engine_thread.start()

    # Lancer Flask dans le thread principal (avec debug activé)
    app.run(debug=True, host="0.0.0.0", port=8000, use_reloader=False)