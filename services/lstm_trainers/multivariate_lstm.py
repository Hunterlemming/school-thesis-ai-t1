import numpy as np
import pandas as pd

from typing import List
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Dropout

from services.lstm_trainers.base_lstm import BaseLSTM
from utils.trainer_utils import print_training_accuracy, show_learning_effectiveness_in_epochs, show_training_result


MODEL_LOCATION = './trained_models/LSTM - Multivariate Productivity'


class MultiVariateTrainer(BaseLSTM):

    def __init__(self, data_location: str, target_column: int, independent_columns: List[int],
        test_size: float = 1/3, window_size: int = 7) -> None:
        super().__init__()
        df: pd.DataFrame = pd.read_csv(data_location, sep=';', parse_dates=['timestamp'])
        df.dropna(inplace=True)
        # Initializing helper variables
        self.relevant_columns = [target_column, *independent_columns]
        self.dim = len(self.relevant_columns)
        # Splitting csv into training and testing sets
        end_of_training_set = round(len(df.index) * (1 - test_size))
        self.train: np.ndarray = df.iloc[:end_of_training_set, self.relevant_columns].values
        self.test: np.ndarray = df.iloc[end_of_training_set:, self.relevant_columns].values
        # Scaling data (normalizing)
        self.scaler: MinMaxScaler = MinMaxScaler(feature_range=(0, 1))
        self.train_scaled: np.ndarray = self.scaler.fit_transform(self.train)
        self.test_scaled: np.ndarray = self.scaler.fit_transform(self.test)
        # We don't need the target variables, just the predictors (other variables) in the test set
        self.test_scaled = self.test_scaled[:, 1:]
        # Creating lookback windows
        x_train = []
        y_train = []
        for i in range (window_size, len(self.train_scaled)):
            x_train.append(self.train_scaled[i-window_size:i, :])   # The independent and target variables in the current window
            y_train.append(self.train_scaled[i, 0])                 # The next value of the target variable (based on window)
        self.lookback_window_size: int = window_size
        self.train_x_lookback: np.ndarray = np.array(x_train)
        self.train_y_lookback: np.ndarray = np.array(y_train)
        # Reshaping, in order to make sure that train_x_lookback is in a proper shape before training
        # Number of features (dimensions) = len(relevant_columns) (ex.: 2 = {productivity, other_actor})
        self.train_x_lookback = np.reshape(self.train_x_lookback, 
            (self.train_x_lookback.shape[0], self.train_x_lookback.shape[1], self.dim))

    def train_new_model(self) -> None:
        model = Sequential()
        # Input layer
        model.add(LSTM(units=70, return_sequences=True, 
            input_shape=(self.train_x_lookback.shape[1], self.dim)))
        model.add(Dropout(0.2))
        # Hidden layers
        model.add(LSTM(units=70, return_sequences=True))
        model.add(Dropout(0.2))
        model.add(LSTM(units=70, return_sequences=True))
        model.add(Dropout(0.2))
        # Output layer
        model.add(LSTM(units=70))
        model.add(Dropout(0.2))
        model.add(Dense(units=1))
        # Compile and fit
        model.compile(optimizer='adam', loss='mean_squared_error')
        model.fit(self.train_x_lookback, self.train_y_lookback, epochs=30, batch_size=7)
        show_learning_effectiveness_in_epochs(model)
        # Saving model
        # model.save(MODEL_LOCATION)
        self._model = model

    def run_model(self):
        trained_model: Sequential = self.get_model(MODEL_LOCATION)
        prediction_test = []
        # Creating a window-sized starting batch
        batch_one: np.ndarray = self.train_scaled[-self.lookback_window_size:]
        batch_new: np.ndarray = batch_one.reshape((1, self.lookback_window_size, self.dim))
        # Running the model on the test set
        for i in range(len(self.test_scaled)):
            # Predicting next value
            first_pred = trained_model.predict(batch_new)[0]
            prediction_test.append(first_pred)
            # Creating a new row, to base our next prediction on
            new_var = self.test_scaled[i,:]                             # We already know the independent variables,
            new_var = new_var.reshape(1, self.dim - 1)                  # so the only thing we have to do is creating
            new_test = np.insert(new_var, 0, [first_pred], axis=1)      # a new row with these and the freshly predicted
            new_test = new_test.reshape(1, 1, 2)                        # target variable (First_Pred)
            # Adding the prediction to the starting batch while removing its first value
            batch_new = np.append(batch_new[:,1:,:], new_test, axis=1)
        # We can't simply use the sc to convert our result back to the original scale,
        # since we used an array of self.dim to normalize and now we only have 1 value
        SI = MinMaxScaler(feature_range=(0,1))
        y_scale = self.train[:, [0]]
        SI.fit(y_scale)             # We can however create a scaler for the target column (first)
        # Converting the normalized values back to their original form
        prediction_test = np.array(prediction_test)
        predictions = SI.inverse_transform(prediction_test)
        real_values = self.test[:, 0]
        # Evaluating the result
        print_training_accuracy(real_values, predictions)
        show_training_result(real_values, predictions, 
            title='Univariate - LSTM', xlabel='Time (d)', ylabel='Productivity')
