import pandas as pd
import random

def get_data():
    list_df = []
    temp = []
    c=0
    while True:
            outputValue = random.choice(['100,8', '98,9', '65,6', '78,9', '88,5', '93,10', '116,14', '95,8', '104,10',
                        '81,9', '100,9', '96,9', '70,7', '80,9', '88,10', '95,9', '120,12', '98,8', '103,9', '60,5',
                        '86,9', '105,10', '69,6', '56,6', '82,10', '90,10', '72,8', '110,11', '87,8', '103,9', '67,6'])
            outputValue1 = random.choice([0.0, 0.2, 0.5, 0.26, 0.62, 0.23, 0.45, 0.23, 0.1, 0.4, 0.31, 0.51, 0.18,
                                          0.28, 0.19, 0.38, 0.41, 0.08, 0.44, 0.39])
            temp.append(outputValue+','+str(outputValue1))
            c+=1
            if c==4000:
                break
    print ('list foud')
    #print (temp)
    for value in temp:
        x,y,val = value.split(',')
        list_df.append([float(x), float(y), float(val)])

    df = pd.DataFrame(list_df, columns = ['X', 'Y','Value'])
    return(df)
    #df.to_csv('chartdata.csv', index = False)