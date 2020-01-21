import random

def get_data():
    temp = ''
    c=0
    while True:
            efficiency = random.choice([94, 98, 65, 78, 88, 41, 22, 54, 56, 81])
            temperature = random.choice([5.0, 20.0, 18.5, 6.0, 8.0, 12.5, 17.5, 14.0, 10.1, 11.5, 12.9, 15.0])
            current = random.choice([0.0, 20.0, 18.5, 6.0, 8.0, 12.5, 17.5, 14.0, 10.1, 11.5, 12.9, 15.0])
            if efficiency>90:
                efficiency = 'e_veryhigh'
            elif efficiency>70:
                efficiency = 'e_high'
            elif efficiency>50:
                efficiency = 'e_med'
            else:
                efficiency = 'e_low'

            if temperature > 15.0:
                temperature = 't_high'
            elif temperature > 8.0:
                temperature = 't_med'
            else:
                temperature = 't_low'

            if current > 15.0:
                current = 'c_high'
            elif current > 8.0:
                current = 'c_med'
            else:
                current = 'c_low'
            temp = temp + temperature + ' ' + current + ' ' + efficiency + '\n'
            c+=1
            if c==1500:
                break
    print ('list found')
    filename = 'data.txt'
    f = open(filename, "a+")
    f.write(temp)
    f.close()
    return filename

df = get_data()
print(df)