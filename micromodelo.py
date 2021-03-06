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

# Json Library
import json

# Misc.
from random import randrange, uniform

dictToSend = {'Cars': []}

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

        dictToSend['length'] = len(self.carAgents)

        for car in self.carAgents:
          dictToSend["Cars"].append({ 
              "CarId": car.id,
              "Position": {
                "x": self.grid.positions[car][0],
                "y": 0,
                "z": self.grid.positions[car][1]
              }
         })
        
        for semaforo in self.semaforoAgents:
          self.posSem = posSem = self.grid.positions[semaforo]

          if posSem == (5,4) or posSem == (6,7):
            semaforo.typeColor = 1
            print(semaforo)
          elif posSem == (7,5) or posSem == (4,6):
            semaforo.typeColor = 2
            print(semaforo)
          
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
        
        self.time = 0
      else:
        self.time += 1
    
    

    def step(self):
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
  
        dictToSend["Cars"].append({ 
              "CarId": agent.id,
              "Position": {
                "x": posCar[0],
                "y": 0,
                "z": posCar[1]
              }
         })

      # self.num_moves += self.p.n_agents
      self.num_moves += 1
      # print(self.num_moves)


parameters = {
    'n_agents': 4, 
    'density': 0.3, # Density of population
    'height': 20,
    'width': 20,
    'steps': 100  # Maximum number of steps
    }

def animation_plot(model, ax):
    gridPosition = model.grid.attr_grid('typeColor')
    color_dict = {0:'#687068', 1:'#43f00a', 2:'#f00a0a', 3:'#2be809', 4:'#26d7ff', 5:'#b05f13', 6:'#00420e', 7:'#ffe926', None:'#ffffff'}
    ap.gridplot(gridPosition, ax=ax, color_dict=color_dict, convert=True)
    ax.set_title(f"Traffic model \n Time-step: {model.t}, # of Moves: {model.num_moves}")

def createJson():
  model = TrafficModel(parameters)
  model.run()

  return dictToSend