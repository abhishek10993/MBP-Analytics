import pandas as pd
import random

def get_data():
    temp = []
    c=0
    while True:
            outputValue = random.choice([48, 98, 63, 78, 88, 93, 52, 95, 84, 81, 72, 57, 68, 75])
            outputValue1 = random.choice([20.0, 38.5, 48.0, 58.0, 72.5, 57.5, 34.0, 80.1, 72.5, 92.9, 65.0, 54.0, 51.0])
            temp.append([outputValue, outputValue1])
            c+=1
            if c==1500:
                break
    print ('list found')

    df = pd.DataFrame(temp, columns = ['feature', 'Value'])
    df.astype(float)
    return(df)