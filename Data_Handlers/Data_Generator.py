import pandas as pd
import random

def get_data():
    list_df = []
    temp = []
    c=0
    while True:
            outputValue = random.choice(['100,8', '98,9', '65,6', '78,9', '88,5', '93,10', '116,14', '95,8', '104,10', '81,9'])
            outputValue1 = random.choice([0.0, 20.0, 18.5, 6.0, 8.0, 12.5, 17.5, 14.0, 10.1, 11.5, 12.9, 15.0])
            temp.append(outputValue+','+str(outputValue1))
            c+=1
            if c==1000:
                break
    print ('list foud')
    #print (temp)
    for value in temp:
        x,y,val = value.split(',')
        list_df.append([float(x), float(y), float(val)])

    df = pd.DataFrame(list_df, columns = ['X', 'Y','Value'])
    return(df)
    #df.to_csv('chartdata.csv', index = False)