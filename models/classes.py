from collections import deque

class Queue:
    def __init__(self):
        self.items = deque()
    
    def enqueue(self, elemento):
        self.items.append(elemento)
    
    def dequeue(self):
        if not self.is_empty():
            return self.items.popleft()
        return None
    
    def is_empty(self):
        return len(self.items) == 0 
    
    def peek(self):
        if not self.is_empty():
            return self.items[0]
        return None

class Citizen:
    def __init__(self, id, name, type_of_procedure, time):
        self.id = id
        self.name = name
        self.type_of_procedure = type_of_procedure
        self.time = time
    
    def __str__(self):
        return f"Ciudadano {self.id}: {self.name} , {self.type_of_procedure} , Hora de llegada: {self.time}"