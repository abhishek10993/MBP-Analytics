import pandas as pd
import random

def get_data():
    temp = []
    c=0
    while True:
            outputValue = random.choice([100, 98, 65, 78, 88, 93, 116, 95, 104, 81])
            outputValue1 = random.choice([0.0, 20.0, 18.5, 6.0, 8.0, 12.5, 17.5, 14.0, 10.1, 11.5, 12.9, 15.0])
            temp.append([outputValue, outputValue1])
            c+=1
            if c==1500:
                break
    print ('list found')

    df = pd.DataFrame(temp, columns = ['feature', 'Value'])
    df.astype(float)
    return(df)