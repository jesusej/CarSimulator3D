# Car Simulator 3D

## Requirements

### Server

Python 3.10.0  
venv installed

### Client

Unity v2020.3.21f1

## Running first time

### Server

1. Install the recent version of python (You can do it downloading it directly from the [page](https://www.python.org/downloads/) or with the command `choco upgrade python -y`)
2. Install venv with `python -m pip install venv`
3. Create a virtual enviroment `python -m venv \path\to\venv`
4. Type `\path\to\venv\Scripts\activate` to start the virtual environment
5. Install the packages with `python -m pip install -r .\requirements.txt`
6. Run the server with `python server.py`
7. When you're done type `deactivate` and you'll exit the virtual environment

### Client

1. Download and install Unity Hub from [Unity](https://unity3d.com/es/get-unity/download)
2. From Unity Hub install Unity v2020.3.21f1
3. Select the ADD button and select the path to Unity Model ex. `\path\to\repo\UnityModel\`
4. Select the version of Unity as v2020.3.21f1

## Instaling packages
If you want to install a new package to server remember that you have to type a `pip freeze > requirements.txt` while you are on root. Remember that you that the virtual environment needs to be loaded before you save the packages into the .txt or else you'll not save anything (or you could lose the requirements)