import threading

import collections
import random
import time

BUFFER_SIZE = 10
REPONEDORES = random.randint(0,2)
CLIENTES = random.randint(3,6) 
nombres_c = []

# DECLARACIÓN DEL MONITOR

class maquina(object):

  def __init__(self, arg):
    self.nRep = REPONEDORES
    self.nCli = CLIENTES
    self.replenishing = False
    self.nSodas = 0
    self.mutex = threading.Lock()
    self.canConsume = threading.Condition(self.mutex)
    self.canReplenish = threading.Condition(self.mutex)

  # OPERACIONES

  def consumir(self, name, consumiciones):
    with self.mutex:

      cons_done = 0

      while cons_done != consumiciones: 
        if (self.nRep > 0):

          while self.replenishing or self.nSodas == 0:
            self.canConsume.wait()

          self.nSodas = self.nSodas - 1

          self.canConsume.notify()

          time.sleep(random.randint(1,2))

          cons_done = cons_done + 1

          print ("        ",name, "coge un refresco - consumición: ", (cons_done))

          self.canReplenish.notify()

        else:

          consumiciones = 0
          print(name, "Aquí nadie repone la máquina!")
              
      self.nCli = self.nCli - 1
      print("--->" + name + " se'n va, queden " + str(self.nCli) + " clients")

  def rellenarMaquina(self, id):
    with self.mutex:
      while self.nCli > 0:

        while self.nSodas == BUFFER_SIZE and self.nCli > 0:
          self.canReplenish.wait()

        self.replenishing = True

        counter = 0
        while self.nSodas != BUFFER_SIZE:
          self.nSodas = self.nSodas + 1
          counter = counter + 1

        time.sleep(random.randint(2,4))

        if counter > 0:
          print("Reposador", id[7:9], " reposa la màquina, hi ha ", str((self.nSodas-counter)), " i en posa ", str(counter))
        
        self.replenishing = False
        self.canConsume.notify()

      print("Reposador", id[7:9], "se'n va")

  # PRESENTACIONES 

  def r_saluda(self, id):
    with self.mutex:
      print ("Reposador", id[7:9], "arriba")

  def c_saluda(self, name, consumiciones):
    with self.mutex:
      print ("  ", name, "arriba i farà", str(consumiciones), "consumicions")

# PROCESOS QUE INTERVIENEN

def clientes(monitor, name):     # consumidores
  consumiciones = random.randint(0,6)
  monitor.c_saluda(name, consumiciones)
  monitor.consumir(name, consumiciones)

def reponedores(monitor):       # productores
  id = threading.current_thread().name
  monitor.r_saluda(id)
  monitor.rellenarMaquina(id)
    
# MÉTODO MAIN

def main():
  threads = []
  monitor = maquina(BUFFER_SIZE)
  n = 0

  # Print donde hacemos recuento de los clientes de la maquina
  print ("COMENÇA LA SIMULACIÓ")
  print ("Avui hi ha ",str(CLIENTES), "clientes i", str(REPONEDORES), "reposadors" )
  print ("La màquina de refrescs està buida, hi caben ", str(BUFFER_SIZE), "refrescs")
  
  for i in range(CLIENTES):
    num = random.randint(1, 250)
    file = open(r"/content/drive/My Drive/LlistaNoms.txt", "r", encoding="utf8")
    lines = file.readlines()
    name = lines[num]
    name = name.rstrip('\n')
    nombres_c.append(name)
    file.close()

  
  for i in range(CLIENTES):
    c = threading.Thread(target=clientes, args=(monitor, str(nombres_c[n]),))
    n = n + 1
    threads.append(c)

  for i in range(REPONEDORES):
    p = threading.Thread(target=reponedores, args=(monitor,))
    threads.append(p)

  # Empiezan todos los threads
  for t in threads:
    t.start()

  # Espera a la finalizacion de los threads
  for t in threads:
    t.join()

if __name__ == "__main__":
  main()