import random
import pandas as pd

def get_data(size):
    temp = []
    c=0
    while True:
            efficiency = random.choice([94, 98, 65, 78, 88, 41, 22, 54, 56, 81])
            temperature = random.choice([5.0, 20.0, 18.5, 6.0, 8.0, 12.5, 17.5, 14.0, 10.1, 11.5, 12.9, 15.0])
            current = random.choice([0.0, 20.0, 18.5, 6.0, 8.0, 12.5, 17.5, 14.0, 10.1, 11.5, 12.9, 15.0])
            #status = random.choice(['Good', 'Serious', 'Moderate', 'Normal', 'Severe'])
            status = random.choice([1,2,3,4,5])
            temp.append([temperature, current, efficiency, status])
            c+=1
            if c==size:
                break

    print ('list found')
    return temp
