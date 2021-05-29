import numpy as np
import scipy.special
import random
from defs import *


class Neural:
    def __init__(self, num_input, num_hidden, num_output):
        self.num_input = num_input #ilosc danych wejsciowych
        self.num_hidden = num_hidden
        self.num_output = num_output
        self.weight_input_hidden = np.random.uniform(-0.5, 0.5, size=(self.num_hidden, self.num_input))
        self.weight_output_hidden = np.random.uniform(-0.5, 0.5, size=(self.num_output, self.num_hidden))
        self.activation = lambda x: scipy.special.expit(x)

    def outputs(self, inputs_list):
        inputs = np.array(inputs_list, ndmin=2).T
        #print('inputs', inputs, sep='\n') #wypisanie inputow w konsoli
        hidden_inputs = np.dot(self.weight_input_hidden, inputs) #mnozenie macierzy wagi x wejscia
        #print('hidden_inputs', hidden_inputs, sep='\n')
        hidden_outputs = self.activation(hidden_inputs)
        #print('hidden_outputs', hidden_outputs, sep='\n')  # wypisanie wartosci w hidden node po funkcji aktywacji w konsoli
        final_outputs = np.dot(self.weight_output_hidden, hidden_outputs)
        #print('final_outputs', final_outputs, sep='\n')
        return final_outputs

    def get_max_value(self, inputs_list):
        outputs = self.outputs(inputs_list)
        return np.max(outputs)

    def random_mutation(self):
        mutation(self.weight_input_hidden)
        mutation(self.weight_output_hidden)

    def reproduce_neural(self, neural1, neural2):
        self.weight_output_hidden = reproduce(neural1.weight_input_hidden, neural2.weight_input_hidden)
        self.weight_output_hidden = reproduce(neural1.weight_output_hidden, neural2.weight_output_hidden)


def mutation(arr):
    for x in np.nditer(arr, op_flags=['readwrite']):
        if random.random() < MUTATION_CHANCE:
            x[...] = np.random.random_sample()-0.5


def reproduce(arr1, arr2):
    total = arr1.size
    rows = arr1.shape[0]
    cols = arr1.shape[1]
    # ret = [rows][cols]
    ret = np.empty([rows, cols])
    x = int(total*MIX_PERC)
    for i in range(0, rows):
        for j in range(0, cols):
            if x < cols*rows+i:
                ret[i][j] = arr1[i][j]
            else:
                ret[i][j] = arr2[i][j]
    return ret


