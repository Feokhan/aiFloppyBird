import numpy as np
import scipy.special


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
