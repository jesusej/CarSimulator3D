# Car Simulator 3D

## Requirements
Python 3.10.0
venv installed

## First time?
1. Install the recent version of python (You can do it downloading it directly from the [page](https://www.python.org/downloads/) or with the command `choco upgrade python -y`)
2. Install venv with `python -m pip install venv`
3. Create a virtual enviroment (preferably in the server folder) `python -m venv \path\to\venv`
4. Type `\path\to\venv\Scripts\activate` to start the virtual environment
5. Go to the server folder and install the packages with `python -m pip install -r .\requirements.txt`
6. When you're done type `deactivate` and you'll exit the virtual environment

## Instaling packages
If you want to install a new package remember that you have to type a `pip freeze > requirements.txt` while you are on the `server` folder. Remember that you also need to be into the virtual environment before you save the packages into the .txt or else you'll not save anything (or you could lose the requirements)