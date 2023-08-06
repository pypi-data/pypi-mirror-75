from numpy import random, zeros, array, dot, exp


def sigmoid(x):
    """ Функция ктивации нейрона """
    return 1 / (1 + exp(-x))


def sigmoid_derivative(x):
    """ Функция деактивации """
    return x * (1 - x)


class Seciva:

    """ Класс нейронной сети реализует логику прямого прохождения сигнала по сети
    и обратное распространение ошибки с корректировкой весов связей"""

    # Конструктор принимает параметры нейронной сети - layers
    # передаем список, длина которого = количество слоев,
    # а каждое значение = количество нейронов в соответствующем слое
    def __init__(self, layers: list, name=None):
        self.__layers = [zeros(layer) for layer in layers]
        self.__errors = [zeros(layer) for layer in layers]
        self.__weights = []
        self.__generate_weights()
        self.__size = len(self.__layers)
        self.__name = name if name is not None else self.__hash__()

    def save(self, name=None):
        pass

    def solution(self, input_data: list):
        """ Метод для решения (прямого распространения) входных данных input_data """
        self.__in(data=input_data)
        for i in range(self.__size - 1):
            next_neurones = dot(self.__layers[i], self.__weights[i])
            self.__layers[i+1] = sigmoid(next_neurones)
        # возвращаем значения нейронов выходного слоя
        return self.__out()

    def train(self, input_data: list, output_data: list, iterations: int = 1000):
        """ Метод обучения по входным и выходным данным """
        i = iterations
        while iterations > 0:
            solution = self.solution(input_data)
            error = output_data - solution
            self.__back(error)
            progress = 100 - (iterations / i) * 100
            if progress % 5 == 0:
                print(int(progress), '%')
            iterations -= 1

    def __back(self, error: list):
        """ Метод обратного распространения ошибки """
        self.__errors[self.__size - 1] = error
        for i in range(self.__size-2, -1, -1):
            e = dot(self.__errors[i+1], self.__weights[i].T)
            self.__errors[i] = e

        for i in range(self.__size - 1):
            delta = dot(self.__layers[i].T, self.__errors[i+1] * sigmoid_derivative(self.__layers[i+1]))
            self.__weights[i] += delta

    def __generate_weights(self):
        """ Метод генерирует матрицы весов """
        for i, layer in enumerate(self.__layers[:-1]):
            self.__weights.append(random.random((len(layer), len(self.__layers[i + 1]))))

    def __in(self, data: list = None):
        return self.__layer(data=data, index=0)

    def __out(self, data: list = None):
        return self.__layer(data=data, index=(len(self.__layers) - 1))

    def __layer(self, data: list = None, index: int = 0):
        """ Метод реализует сеттер и геттер для self.__layers """
        if data is not None:
            self.__layers[index] = array(data)
        return self.__layers[index]
