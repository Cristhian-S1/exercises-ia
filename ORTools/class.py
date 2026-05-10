class Kendy():
    def __init__(self, altura):
        self.__altura = altura
    
    def getAltura(self):
        return self.__altura

persona = Kendy(60)
print(persona.altura)