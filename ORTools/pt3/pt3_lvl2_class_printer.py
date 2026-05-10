from ortools.sat.python import cp_model

#Aplicamos herencia para la clase CpSolverSolutionCallback que viene en el modulo de cp_model
class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print solutions"""

    def __init__(self, variables: list[cp_model.IntVar]):
        super().__init__()
        self.__variables = variables
        self.__solution_count = 0

    def on_solution_callback(self):
        self.__solution_count += 1
        for v in self.__variables:
            print(f"{v} = {self.value(v)}", end=" ")
        print()
    
    @property
    def solution_count(self):
        return self.__solution_count
