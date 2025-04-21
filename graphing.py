import main
import pandas as pd
import matplotlib.pyplot as plt
GENRE = 'romance'

def getValues():
    movies = main.readFile()
    linearX = []
    hashX = []
    recs = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000, 3100, 3200, 3300, 3400, 3500, 3600, 3700, 3800, 3900, 4000, 4100, 4200, 4300, 4400, 4500, 4600, 4700, 4800, 4900, 5000, 5100, 5200, 5300, 5400, 5500, 5600, 5700, 5800, 5900, 6000, 6100, 6200, 6300, 6400, 6500, 6600, 6700, 6800, 6900, 7000, 7100, 7200, 7300, 7400, 7500, 7600, 7700, 7800, 7900, 8000, 8100, 8200, 8300, 8400, 8500, 8600, 8700, 8800, 8900, 9000]
    for i, rec in enumerate(recs):
        linearTime = main.linearSearch(movies, GENRE, rec)
        hashTime = main.hashTable(movies, GENRE, rec)
        linearX.append(linearTime)
        hashX.append(hashTime)
    return linearX, hashX, recs

def plotGraph(linearX, hashX, recs):
    plt.plot(recs, linearX, label='linear search', marker='x')
    plt.plot(recs, hashX, label='hash table', marker='x')
    plt.xlabel('number of recommendations')
    plt.ylabel('time taken (s)')
    plt.title('Exploring time complexity by comparing search algorithms')
    plt.legend()
    plt.grid(True)
    plt.show()

def main2():
    linearX, hashX, recs = getValues()
    plotGraph(linearX, hashX, recs)

main2()
