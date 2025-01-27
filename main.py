# from flask import Flask
# import threading
# from core.engine import Engine

# # Initialisation de Flask
# app = Flask(__name__)

# # Route Flask pour la page principale
# @app.route('/')
# def home():
#     return "Interface Flask en cours d'exécution. Les vidéos sont enregistrées automatiquement."

# # Fonction pour démarrer Flask
# def run_flask():
#     app.run(debug=False, host="0.0.0.0", port=8000)

# # Fonction pour démarrer l'engine
# def run_engine():
#     engine = Engine()
#     engine.run()

# if __name__ == "__main__":
#     # Lancer Flask et l'engine en parallèle
#     flask_thread = threading.Thread(target=run_flask)
#     engine_thread = threading.Thread(target=run_engine)

#     # Démarrage des threads
#     flask_thread.start()
#     engine_thread.start()

#     # Assurer que les deux threads fonctionnent
#     flask_thread.join()
#     engine_thread.join()

from core.engine import Engine

if __name__ == "__main__":
    # Instancier l'engine
    engine = Engine()
    # Lancer l'engine
    engine.run()
