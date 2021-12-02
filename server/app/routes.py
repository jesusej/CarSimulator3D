from app import app
from micromodelo import createJson

@app.route('/')
@app.route('/generate-simulation')
def getSimulation():
  return createJson()