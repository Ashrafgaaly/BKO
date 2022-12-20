import logging

import azure.functions as func
from .predict import *
from .Turbine import *
import pandas as pd
import os.path

# Check whether the model has been predicted and the parameters are saved. Otherwise, Run the prediction model
if os.path.exists('pram.txt'):
    my_file = open("pram.txt", "r")
    data = my_file.read()
    pram = data.split("\n")
    pram = pram[:-1]
    pram = list(map(float, pram))
    my_file.close()

else:
    df = pd.read_excel("interview data.xlsx")
    pram = predict(df)



def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
 The input values to this function is a list of:

    GT1 Exhaust Temp Median Corrected By Average {Avg}
    GT1 Compressor Inlet Temperature {Avg}
    GT1 Compressor Discharge Press Max Select {Avg}
    GT1 Compressor Discharge Temperature {Avg}
    GT1 Generator Watts Max Selected {Avg}'

    This function takes these values in that order and uses gekko solver to estimate the GT1 IGV angle in deg {Avg} by creating
    an object of class Turbine.
 '''
    logging.info('Python HTTP trigger function processed a request.')


    input_values = req.params.get('input_values')

    if not input_values:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            input_values = req_body.get('input_values')

    if input_values:
            # an object of class Turbine is created with the submitted values for the variables and the estimated model parameters
            test = Turbine(input_values[0], input_values[1],input_values[2], input_values[3], input_values[4], pram)
            igv_est = test.igv()

            return func.HttpResponse(f"The IGV value is {igv_est} degrees.")




    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a list of value in the query string or in the request body for a personalized response.",
             status_code=200
        )
