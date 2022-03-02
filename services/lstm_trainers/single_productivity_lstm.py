import numpy as np
import pandas as pd
import math

from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Dropout


from utils.trainer_utils import print_training_accuracy, show_learning_effectiveness_in_epochs, show_training_result


MODEL_LOCATION = './trained_models/LSTM - Single Productivity'


class SingleProductivityTrainer:

    def __init__(self, data_location: str, test_size: float = 1/3, window_size: int = 7) -> None:
        df: pd.DataFrame = pd.read_csv(data_location, sep=';', parse_dates=['timestamp'])
        df.dropna(inplace=True)
        # Splitting csv into training and testing sets
        end_of_training_set = round(len(df.index) * (1 - test_size))
        self.train: np.ndarray = df.iloc[:end_of_training_set, 1:2].values
        self.test: np.ndarray = df.iloc[end_of_training_set:, 1:2].values
        # Scaling data (normalizing)
        self.scaler: MinMaxScaler = MinMaxScaler(feature_range=(0, 1))
        self.train_scaled: np.ndarray = self.scaler.fit_transform(self.train)
        self.test_scaled: np.ndarray = self.scaler.fit_transform(self.test)
        # Creating lookback windows
        x_train = []
        y_train = []
        for i in range (window_size, len(self.train_scaled)):
            x_train.append(self.train_scaled[i-window_size:i, 0:1])
            y_train.append(self.train_scaled[i, 0])
        self.lookback_window_size: int = window_size
        self.train_x_lookback: np.ndarray = np.array(x_train)
        self.train_y_lookback: np.ndarray = np.array(y_train)
        # Registering the model as a private variable
        self._model: Sequential = None

    def get_model(self, new_model: bool = False) -> Sequential:
        '''Returning the model, while making sure we have one.'''
        if new_model:
            # Creating a new model
            self.train_new_model()
        if self._model is None:
            try:
                # Loading already exiting model
                self._model = load_model(MODEL_LOCATION)
            except OSError:
                # Creating a new model
                self.train_new_model()
        return self._model

    def train_new_model(self) -> None:
        '''Trains a new model from the data passed to the constructor.'''
        # Creating the model base
        model = Sequential()
        # Creating the INPUT layer
        model.add(LSTM(
            # Number of neurons in this layer (hyperparameter, adjustable)
            units=60,
            # Whether to return the last output or the full sequence (True untill the last)
            return_sequences=True,
            # The shape and dimension (features) of the input, used at weight creation
            input_shape=(self.train_x_lookback.shape[1], 1)
        ))
        # Avoiding overfitting
        model.add(Dropout(0.2))                             # Drop 20% of the neurons (hyperparameter, adjustable)
        # Adding more HIDDEN layers
        model.add(LSTM(units=60, return_sequences=True))    # We don't need to specify the input_shape anymore
        model.add(Dropout(0.2))
        model.add(LSTM(units=60, return_sequences=True))
        model.add(Dropout(0.2))
        # Creating the OUTPUT layer
        model.add(LSTM(units=60))                           # The return_sequences' default value is False
        model.add(Dropout(0.2))
        model.add(Dense(units=1))                           # We want a single ouptut (prediction)
        # Compiling our model
        model.compile(optimizer='adam', loss='mean_squared_error')
        # Fitting the model
        model.fit(self.train_x_lookback, self.train_y_lookback, epochs=30, batch_size=7)
        show_learning_effectiveness_in_epochs(model)
        # Saving model
        # model.save(MODEL_LOCATION)
        self._model = model

    def run_model(self):
        '''Runs the model on the test dataset and evaluates the result.'''
        trained_model: Sequential = self.get_model()
        prediction_test = []
        # Creating a window-sized starting batch
        batch_one: np.ndarray = self.train_scaled[-self.lookback_window_size:]
        batch_new: np.ndarray = batch_one.reshape((1, self.lookback_window_size, 1))
        # Running the model on the test set
        for i in range(len(self.test_scaled)):
            # Predicting the next value based on the starting batch
            first_pred = trained_model.predict(batch_new)[0]
            prediction_test.append(first_pred)
            # Adding the prediction to the starting batch while removing its first value
            batch_new = np.append(batch_new[:,1:,:], [[first_pred]], axis=1)
        # Converting the normalized values back to their original form
        prediction_test = np.array(prediction_test)
        predictions = self.scaler.inverse_transform(prediction_test)
        # Evaluating the result
        print_training_accuracy(self.test, predictions)
        show_training_result(self.test, predictions)
