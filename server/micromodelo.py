"""micromodelo.py

Variación del python notebook original implementado para servidores

El archivo original se encuentra aquí:
    https://colab.research.google.com/drive/1Y-1WfxmVbwLfa14ab3hQLrhFLU1o5nQb

Elaborado por:
- Jesús Enríquez Jaime
- Valter Kuhne
- José Emilio Flores Figueroa
- Guillermo Williams
"""

# Model design
import agentpy as ap

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns
import IPython
from random import randrange, uniform
from matplotlib.animation import FuncAnimation

# Json Library
import json

class CarAG(ap.Agent):

    def setup(self):
        """ Initiate agent attributes. """
        self.grid = self.model.grid
        self.random = self.model.random
        self.typeColor = 0
        self.status = 0
        self.stopped = False
        self.direction = None
        self.turning = 0

    def move_right(self, posCar, moves):
        """ Move to random free spot and update free spots. """
        self.grid.move_by(self, (0, 1))
        self.direction = "right"
        self.typeColor = 6

    def move_left(self, posCar, moves):
        """ Move to random free spot and update free spots. """
        self.grid.move_by(self, (0, -1))
        self.direction = "left"
        self.typeColor = 5

    def move_up(self, posCar, moves):
        """ Move to random free spot and update free spots. """
        self.grid.move_by(self, (-1, 0))
        self.direction = "up"
        self.typeColor = 4

    def move_down(self, posCar, moves):
        """ Move to random free spot and update free spots. """
        self.grid.move_by(self, (1, 0))
        self.direction = "down"
        self.typeColor = 7

    def redLight(self, posCar, moves):
        self.grid.move_by(self, (0, 0))

    def turn(self):
        turn = randrange(0,2)
        return turn

class SemaforoAG(ap.Agent):

    def setup(self):
        """ Initiate agent attributes. """
        self.grid = self.model.grid
        self.random = self.model.random
        self.typeColor = 1

    def semaforo(self):
    
        if self.typeColor == 1:
          self.typeColor = 2

        else:
          self.typeColor = 1

class TrafficModel(ap.Model):

    def setup(self):

        # Parameters
        h = self.p.height
        w = self.p.width
        d = self.d = int(self.p.density * (w * h))
        n = self.n = self.p.n_agents
        semaforos = 4
        cars = 5

        self.TIME_LIMIT = 4
        self.time = 0
        
        self.num_moves = 0
        self.moved = 0

        # Create grid and agents
        self.grid = ap.Grid(self, (h, w), torus=True,track_empty=True, check_border=True)
        self.carAgents = ap.AgentList(self, cars, CarAG)
        self.semaforoAgents = ap.AgentList(self, semaforos, SemaforoAG)

        self.grid.add_agents(self.semaforoAgents, positions = tuple( [(5,4), (7,5), (4,6), (6,7)] ), empty=False, random=True)
        self.grid.add_agents(self.carAgents, positions = tuple( [(6,3), (0,6), (11,5), (6,11), (5,1)] ), empty=True, random=False)
        #self.grid.add_agents(self.carAgents, positions = tuple( [(0,6), (2,6)] ), empty=True, random=False)

        for car in self.carAgents:
          car.record('posCar', self.grid.positions[car])
        
        for semaforo in self.semaforoAgents:
          self.posSem = posSem = self.grid.positions[semaforo]

          semaforo.record('posSem', posSem)

          if posSem == (5,4) or posSem == (6,7):
            semaforo.typeColor = 1
            print(semaforo)
          elif posSem == (7,5) or posSem == (4,6):
            semaforo.typeColor = 2
            print(semaforo)
          
          semaforo.record('typeColor')

    def update(self):
        # 
        self.allRobots = self.carAgents.select(self.carAgents.id > 0)
        self.allGreens = self.semaforoAgents.select(self.semaforoAgents.typeColor == 1)

        self.allReds = self.semaforoAgents.select(self.semaforoAgents.typeColor == 2)
        
        self.allSemaforos = self.semaforoAgents.select(self.semaforoAgents.id > 0)


        # Stop simulation if no fire is left
        if self.d == 0:
            self.stop()
    
    def findTrafficLights(self, car, posCar):
      for neighbor in self.grid.neighbors(car):
        posNeighbor = self.grid.positions[neighbor]

        if (posNeighbor == posCar):
          return neighbor

    def findNearestCar(self, car, position):
      for neighbor in self.grid.neighbors(car):

        if (neighbor.type == "CarAG" and neighbor.stopped == True and car.direction == neighbor.direction):
          return neighbor
    
    def changeTrafficLight(self):
      if self.time == self.TIME_LIMIT:
        for semaforo in self.semaforoAgents:
          semaforo.semaforo()
          semaforo.record('typeColor')
        
        self.time = 0
      else:
        self.time += 1
    
    

    def step(self):

      self.record('num_moves')
      self.changeTrafficLight()
    
      for agent in self.allRobots:
        self.posCar = posCar = self.grid.positions[agent]
        nearTrafficLight = self.findTrafficLights(agent, posCar)
        nearCar = self.findNearestCar(agent, posCar)
        
        if (nearTrafficLight != None):
          if(nearTrafficLight.typeColor == 2):
            agent.stopped = True
            #print("Car: ", agent.id, " at: ", self.num_moves, " is Stopped 'cause traffic light")
          else:
            agent.stopped = False
        
        elif (nearCar != None and nearCar.stopped):
          agent.stopped = True
        else:
          agent.stopped = False
        

        if (not agent.stopped):
          agent.turning = 0
          # While car is in position (6, 5) move randomly left or up
          if posCar == (6,5) and agent.turn() == 0:
            agent.move_up(self.posCar, self.num_moves)
            # print(self.num_moves ,posCar,agent.turn())
          elif posCar == (6,5) and agent.turn() == 1 and agent.turning == 0:
            agent.turning = 1
            agent.move_left(self.posCar, self.num_moves)
            # print(self.num_moves ,posCar,agent.turn())

          # While car is in position (6, 6) move randomly left or down
          elif posCar == (6,6) and agent.turn() == 0:
            agent.move_left(self.posCar, self.num_moves)
            # print(self.num_moves ,posCar,agent.turn())
          elif posCar == (6,6) and agent.turn() == 1 and agent.turning == 0:
            agent.turning = 1
            agent.move_down(self.posCar, self.num_moves)  
            # print(self.num_moves ,posCar,agent.turn())
          
          # While car is in position (5, 5) move randomly right or up
          elif posCar == (5,5) and agent.turn() == 1 and agent.turning == 0:
            agent.turning = 1
            agent.move_up(self.posCar, self.num_moves)
            #print(self.num_moves ,posCar,agent.turn())
          elif posCar == (5,5) and agent.turn() == 0:
            agent.move_right(self.posCar, self.num_moves)
            #print(self.num_moves ,posCar,agent.turn())
          
          # While car is in position (5, 6) move randomly right or down
          elif posCar == (5,6) and agent.turn() == 0:
            agent.move_down(self.posCar, self.num_moves)
            # print(self.num_moves ,posCar,agent.turn())
          elif posCar == (5,6) and agent.turn() == 1 and agent.turning == 0:
            agent.turning = 1
            agent.move_right(self.posCar, self.num_moves)
            #print(self.num_moves ,posCar,agent.turn())

          # While car is in position is in road move right, down, up or left

          elif posCar[0] == 5 and (posCar != (5, 6) or posCar != (5, 5)):
            agent.move_right(self.posCar, self.num_moves)
          

          elif posCar[1] == 6 and (posCar != (5, 6) or posCar != (6, 6)):
            agent.move_down(self.posCar, self.num_moves)
            

          elif posCar[1] == 5 and (posCar != (6, 5) or posCar != (5, 5)):
            agent.move_up(self.posCar, self.num_moves)
      
          
          elif posCar[0] == 6 and (posCar != (6, 6) or posCar != (6, 5)):
            agent.move_left(self.posCar, self.num_moves)
  
        
        agent.record('posCar', posCar)
        #self.record('posCar')
        #self.record('agent.stopped')
        #self.record('agent.direction')
        #self.record('agent.turning')

      # self.num_moves += self.p.n_agents
      self.num_moves += 1
      # print(self.num_moves)


parameters = {
    'n_agents': 4, 
    'density': 0.3, # Density of population
    'height': 20,
    'width': 20,
    'steps': 200  # Maximum number of steps
    }

def animation_plot(model, ax):
    gridPosition = model.grid.attr_grid('typeColor')
    color_dict = {0:'#687068', 1:'#43f00a', 2:'#f00a0a', 3:'#2be809', 4:'#26d7ff', 5:'#b05f13', 6:'#00420e', 7:'#ffe926', None:'#ffffff'}
    ap.gridplot(gridPosition, ax=ax, color_dict=color_dict, convert=True)
    total = model.p.height * model.p.width
    percent = (total - model.d) * 100 / (total)
    ax.set_title(f"Traffic model \n Time-step: {model.t}, # of Moves: {model.num_moves}")

def redefineTrafficLights(trafficLights):
  posSem = {}
  idList = []
  for i in trafficLights['posSem']:
    if trafficLights['posSem'][i] != None:
      id = i[0]
      posSem[id] = trafficLights['posSem'][i]
      idList.append(id)


  trafficLights['posSem'] = posSem

  colorKey = [[] for i in idList]
  colorValues = [[] for i in idList]
  id = 0
  j = -1
  for i in trafficLights['typeColor']:
    if (id != i[0]):
      id = i[0]
      j += 1
    colorKey[j].append(i[1])
    colorValues[j].append(trafficLights['typeColor'][i])

  typeColor = {}
  for i in range(len(idList)):
    zipIterator = zip(colorKey[i], colorValues[i])
    typeColor[idList[i]] = dict(zipIterator)

  trafficLights['typeColor'] = typeColor

  return trafficLights

def redefineCarResults(carResults):
  idList = []
  keyList = []
  valuesList = []
  id = 0
  j = -1
  for i in carResults['posCar']:
    if i[0] != id:
      id = i[0]
      idList.append(id)
      keyList.append([])
      valuesList.append([])
      j += 1

    keyList[j].append(i[1])
    valuesList[j].append(carResults['posCar'][i]) 
  
  posCar = {}
  for i in range(len(idList)):
    zipIterator = zip(keyList[i], valuesList[i])
    posCar[idList[i]] = dict(zipIterator)
  
  carResults['posCar'] = posCar

  return carResults

fig, ax = plt.subplots()
model = TrafficModel(parameters)
results = model.run()

carResults = results['variables']['CarAG'].to_dict()
trafficLights = results['variables']['SemaforoAG'].to_dict()

trafficLights = redefineTrafficLights(trafficLights)
carResults = redefineCarResults(carResults)

finalDict = {'trafficLights': trafficLights, 'carResults': carResults}

finalJson = json.dumps(finalDict, indent = 4)
print(finalJson)

#animation = ap.animate(model, fig, ax, animation_plot)
#IPython.display.HTML(animation.to_jshtml())