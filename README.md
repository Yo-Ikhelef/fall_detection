# Afin d'initialiser le projet pour développer localement suivre les étapes:

## 1. Installer Python 3.9.2 ( la derniere version 3.11.2 peux probablement fonctionner)
Sur le site https://www.python.org/downloads/  
ou  
sur mac et linux/wsl:
`sudo apt update`
`sudo apt install` `python3 python3-pip -y`


## 2. Installer l'environnement virtuel
Depuis le répertoire du projet cloné :
`python3 -m venv venv`

## 3. Activer l'environnement virtuel et installer les dépendances:
utiliser simplement le script bash, donner lui les droits avec `chmod +x setup.sh` et executer `./setup.sh`

sinon

**Activer l'environnement:**   
-Sur Linux/macOS: `source venv/bin/activate`

-Sur Windows: `venv\Scripts\activate`

**Installer les dépendances du projet:**  

`pip install -r requirements.txt`

sinon

openCV : `pip install opencv-python` `pip install opencv-contrib-python`  
numpy : `pip install numpy`  
twilio : `pip install twilio`  
Flask: `pip install flask`  


## 4. Installer les dépendances système :
OpenCV peut nécessiter certaines bibliothèques système pour fonctionner correctement.

Sur Linux :

`sudo apt install libopencv-dev python3-opencv -y`
`sudo apt install libatlas-base-dev libjpeg-dev libtiff-dev libpng-dev -y`

Sur Windows/macOS :

Ces dépendances sont incluses avec les versions pip d’OpenCV. Aucune installation supplémentaire n’est nécessaire.







