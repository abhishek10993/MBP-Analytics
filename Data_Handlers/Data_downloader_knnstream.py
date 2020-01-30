import time
import random

f= open("text.csv","a+")
count = 0
while True:
    outputValue = random.choice([48, 98, 63, 78, 88, 93, 52, 95, 84, 81, 72, 57, 68, 75])
    outputValue1 = random.choice([20.0, 38.5, 48.0, 58.0, 72.5, 57.5, 34.0, 80.1, 72.5, 92.9, 65.0, 54.0, 51.0])
    outputValue2 = random.choice([48, 98, 63, 78, 88, 93, 52, 95, 84, 81, 72, 57, 68, 75])
    data = str(outputValue) + ',' + str(outputValue1) + ',' + str(outputValue2)
    f = open("text.csv", "a+")
    f.write(data + "\n")
    f.close()
    count+=1
    if count==1000:
        break;

print("done")