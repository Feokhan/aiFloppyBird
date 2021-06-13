import numpy as np
import os.path
import matplotlib.pyplot as plt


def graph(filename):
    if not os.path.isfile(filename):
        print("brak pliku")
        return 0
    data = np.load(filename)
    graph_data_worst = data['worst']
    graph_data_avg = data['avg']
    graph_data_best = data['best']
    fig, ax = plt.subplots()
    print(graph_data_best)
    print(graph_data_avg)
    print(graph_data_worst)
    #ax.plot(graph_data_best, label='Fitness najlepszego ptaka')
    ax.plot(graph_data_avg, label='Średni fitness')
    ax.plot(graph_data_worst, label='Fitness najgorszego ptaka')
    ax.set_title('Wykres wartości Fitness')
    ax.legend()
    plt.show()


if __name__ == "__main__":
    graph("data/iteration134.npz")