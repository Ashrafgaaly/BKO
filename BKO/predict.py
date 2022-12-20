import numpy as np
from gekko import GEKKO
import math


def predict(df):
    '''
    This function takes the dataset and tries to fit a curve. The equation used is exponential and solved using gekko to minimize the residuals
    '''

    xm1 = np.array(df['GT1 Exhaust Temp Median Corrected By Average {Avg}'])
    xm2 = np.array(df['GT1 Compressor Inlet Temperature {Avg}'])
    xm3 = np.array(df['GT1 IGV angle in deg {Avg}'])
    xm4 = np.array(df['GT1 Compressor Discharge Press Max Select {Avg}'])
    xm5 = np.array(df['GT1 Compressor Discharge Temperature {Avg}'])
    ym = np.array(df['GT1 Generator Watts Max Selected {Avg}'])


    m = GEKKO()
    a1 = m.FV(lb=-100.0,ub=100.0)
    a2 = m.FV(lb=-100.0,ub=100.0)
    a3 = m.FV(lb=-100.0,ub=100.0)
    a4 = m.FV(lb=-100.0,ub=100.0)
    a5 = m.FV(lb=-100.0,ub=100.0)
    b = m.FV(lb=-100.0,ub=100.0)
    x1 = m.Param(value=xm1)
    x2 = m.Param(value=xm2)
    x3 = m.Param(value=xm3)
    x4 = m.Param(value=xm4)
    x5 = m.Param(value=xm5)
    z = m.Param(value=ym)
    y = m.Var()

    m.Equation(y==b*(math.e**(-x1*a1)+math.e**(-x2*a2)+math.e**(-x3*a3)+math.e**(-x4*a4)+math.e**(-x5*a5)))


    m.Minimize((y-z)**2)
    # Options
    a1.STATUS = 1
    a2.STATUS = 1
    a3.STATUS = 1
    a4.STATUS = 1
    a5.STATUS = 1
    b.STATUS = 1

    m.options.IMODE = 2
    m.options.SOLVER = 1

    m.solve(disp=False)


    l = [b.value[0],a1.value[0], a2.value[0], a3.value[0], a4.value[0],a5.value[0]]

    with open("pram.txt", "w") as output:
        for i in l:
            output.write("{}\n".format(i))

    return l
