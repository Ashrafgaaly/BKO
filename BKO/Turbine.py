from gekko import GEKKO
import math



class Turbine:


    def __init__(self, generator_watts, exhaust_temp, inlet_temp, discharge_press, discharge_temp, pram):

      '''
      The features of this class are the power generated value, and all dependent variable values in the dataset except IGV.
      In addition to that, the model parameters
      '''
      self.generator_watts = generator_watts
      self.exhaust_temp = exhaust_temp
      self.inlet_temp = inlet_temp
      self.discharge_press = discharge_press
      self.discharge_temp = discharge_temp
      self.pram = pram



    def igv(self, solver=GEKKO()):
        '''
        Once an object of the class is created, the model function is solved to minimize the different between the actual power generated value,
        and the predicted value given that IGV is a variable
        '''
        b = self.pram[0]
        a1 = self.pram[1]
        a2 = self.pram[2]
        a3 = self.pram[3]
        a4 = self.pram[4]
        a5 = self.pram[5]

        x3 = solver.Var()


        solver.Minimize(((b*(math.e**(-self.exhaust_temp*a1)+
                            math.e**(-self.inlet_temp*a2)+
                            math.e**(-x3*a3)+
                            math.e**(-self.discharge_press*a4)+
                            math.e**(-self.discharge_temp*a5)
                          )
                        ) - self.generator_watts)**2
                       )


        solver.options.IMODE = 2
        solver.options.SOLVER = 1
        solver.solve(disp = False)
        print("The estimated GT1 IGV angle is {} degrees".format(x3.value[0]))
        return x3.value[0]



