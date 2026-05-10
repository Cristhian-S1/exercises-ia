import numpy 

listx = [[1,2,3],
         [4,5,6],
         [7,8,9]]

for i in listx:
    for j in i:
        print(j)

values = [(fila, columna) for fila in range(4) for columna in range(4)]
print(values)

matrizx = [[(r,c) for r in range(4)] for c in range(4)] 
print(matrizx)

lst1 = [1,2,3,4]
map_1 = map(lambda value_list: value_list**2, lst1)
filter_1 = filter(lambda value_list: value_list%2 == 0, lst1)
print(*map_1)
print(*filter_1)


class Car():
    global_var = 67

    def __init__(self, model, color):
        self.__model = model
        self.__color = color
    
    @property
    def modelo(self):
        return self.__model

    @modelo.setter
    def model(self, new_model):
        self.__model = new_model

    def sound(self):
        print("Rum rum!")    

class Thing(Car):
    def __init__(self, model, color, des):
        super().__init__(model, color)
        self.__des = des

    @property
    def des(self):
        print(self.__des)

    def sound(self):
        super().sound()
        print("Ram ram")

#Car    
car = Car("Toyota", "Blue")
print(car.modelo)
car.model = "BMW"
print(car.modelo)
car.sound()
print()

#Thing
thing = Thing("Mazda", "White", "Des")
thing.des
thing.sound()