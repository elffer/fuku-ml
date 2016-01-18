#encoding=utf8

import os
import random
import numpy as np


class BinaryClassifier(object):

    status = 'empty'
    train_X = []
    train_Y = []
    W = []
    data_num = 0
    data_demension = 0
    tune_times = 0
    test_data_x = []
    test_data_y = 0
    test_X = []
    test_Y = []
    avg_error = float('Inf')

    def __init__(self):

        self.status = 'empty'
        self.train_X = []
        self.train_Y = []
        self.W = []
        self.data_num = 0
        self.data_demension = 0
        self.tune_times = 0
        self.test_data_x = []
        self.test_data_y = 0
        self.test_X = []
        self.test_Y = []

    def load_train_data(self, input_data_file=''):

        '''
        Load train data
        Please check dataset/pla_binary_train.dat to understand the data format
        Each feature of data x separated with spaces
        And the ground truth y put in the end of line separated by a space
        '''

        self.status = 'load_train_data'

        if (input_data_file == ''):
            input_data_file = os.path.normpath(os.path.join(os.path.join(os.getcwd(), os.path.dirname(__file__)), "dataset/pla_binary_train.dat"))
        else:
            if (os.path.isfile(input_data_file) is not True):
                print("Please make sure input_data_file path is correct.")
                return self.train_X, self.train_Y

        X = []
        Y = []
        with open(input_data_file) as f:
            for line in f:
                data = line.split()
                x = [1] + [float(v) for v in data[:-1]]
                X.append(x)
                Y.append(float(data[-1]))

        self.train_X = np.array(X)
        self.train_Y = np.array(Y)

        return self.train_X, self.train_Y

    def load_test_data(self, input_data_file=''):

        '''
        Load test data
        Please check dataset/pocket_pla_binary_test.dat to understand the data format
        Each feature of data x separated with spaces
        And the ground truth y put in the end of line separated by a space
        '''

        if (input_data_file == ''):
            input_data_file = os.path.normpath(os.path.join(os.path.join(os.getcwd(), os.path.dirname(__file__)), "dataset/pocket_pla_binary_test.dat"))
        else:
            if (os.path.isfile(input_data_file) is not True):
                print("Please make sure input_data_file path is correct.")
                return self.test_X, self.test_Y

        X = []
        Y = []
        with open(input_data_file) as f:
            for line in f:
                data = line.split()
                x = [1] + [float(v) for v in data[:-1]]
                X.append(x)
                Y.append(float(data[-1]))

        self.test_X = np.array(X)
        self.test_Y = np.array(Y)

        return self.test_X, self.test_Y

    def init_W(self):

        '''
        Init the W
        Simple way is init W all zeros
        '''

        if (self.status != 'load_train_data') and (self.status != 'train'):
            print("Please load train data first.")
            return self.W

        self.status = 'init'

        self.data_num = len(self.train_Y)
        self.data_demension = len(self.train_X[0])
        self.W = np.zeros(self.data_demension)

        return self.W

    def score_function(self, x, W):

        '''
        Score function to calculate score
        '''

        score = np.sign(np.inner(x, W))

        return score

    def error_function(self, y_prediction, y_truth):

        '''
        Error function to calculate error
        '''

        if y_prediction != y_truth:
            return 1
        else:
            return 0

    def calculate_avg_error(self, X, Y, W):

        '''
        Get current avg error from X, Y, W
        '''

        data_num = len(Y)
        error_num = 0

        for i in range(data_num):
            error_num = error_num + self.error_function(self.score_function(X[i], W), Y[i])

        avg_error = error_num / float(data_num)

        return avg_error

    def train(self, mode='naive_cycle', alpha=1):

        '''
        Train Perceptron Learning Algorithm
        From f(x) = WX
        Find best h(x) = WX similar to f(x)
        Output W
        '''

        if (self.status != 'init'):
            print("Please load train data and init W first.")
            return self.W

        self.status = 'train'

        if (mode is 'random'):
            data_check_order = range(self.data_num)
            data_check_order = random.sample(data_check_order, self.data_num)
        elif (mode is 'naive_cycle'):
            data_check_order = range(self.data_num)
        else:
            data_check_order = range(self.data_num)

        self.tune_times = 0
        k = 0
        flag = True

        while True:
            if (self.tune_times > (2 * self.data_num)):
                print("Dataset not linear separable.")
                break

            if k == self.data_num:
                if flag:
                    break
                k = 0
                flag = True

            point_wise_i = data_check_order[k]

            if self.error_function(self.score_function(self.train_X[point_wise_i], self.W), self.train_Y[point_wise_i]):
                flag = False
                self.tune_times += 1
                self.W = self.W + alpha * (self.train_Y[point_wise_i] * self.train_X[point_wise_i])
            k += 1

        return self.W

    def prediction(self, test_data=''):

        '''
        Make prediction
        input test data
        output the prediction
        '''

        prediction = 0

        if (self.status != 'train'):
            print("Please load train data and init W then train the W first.")
            return prediction

        if (test_data == ''):
            print("Please input test data for prediction.")
            return prediction

        data = test_data.split()
        self.test_data_x = [1] + [float(v) for v in data[:-1]]
        self.test_data_y = float(data[-1])

        prediction = self.score_function(self.test_data_x, self.W)

        return prediction