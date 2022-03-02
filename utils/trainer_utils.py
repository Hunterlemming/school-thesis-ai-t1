import math
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from sklearn.metrics import mean_squared_error, r2_score


def show_learning_effectiveness_in_epochs(model: Sequential):
    '''Visualizes the loss in each epoch during the training of a Sequential model.'''
    plt.plot(range(len(model.history.history['loss'])), model.history.history['loss'])    # Check history loss
    plt.xlabel('Epoch number')
    plt.ylabel('Loss')
    plt.show()

def print_training_accuracy(test: np.ndarray, predictions: np.ndarray):
    RMSE = math.sqrt(mean_squared_error(test, predictions))
    Rsquare = r2_score(test, predictions)
    print(f"Root-mean-square-deviation = {RMSE}\nCoefficient of determination = {Rsquare}")

def show_training_result(test: np.ndarray, predictions: np.ndarray):
    plt.plot(test, color='red', label="Actual Values")
    plt.plot(predictions, color='blue', label="Predicted Values")
    plt.title('LSTM - Univariate Forecast')
    plt.xlabel('Time (h)')
    plt.ylabel('Solar Irradiance')
    plt.legend()
    plt.show()
