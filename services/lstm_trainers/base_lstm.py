from abc import abstractmethod
from keras.models import Sequential, load_model


DEFAULT_LOCATION = './trained_models/LSTM - BASE'


class BaseLSTM:
    
    def __init__(self) -> None:
        # Registering the model as a private variable
        self._model: Sequential = None

    @abstractmethod
    def train_new_model(self) -> None:
        '''Trains a new model from the data passed to the constructor.'''
        pass

    @abstractmethod
    def run_model(self, model_location: str) -> None:
        '''Runs the model on the test dataset and evaluates the result.'''
        pass

    def get_model(self, model_location: str, new_model: bool = False) -> Sequential:
        '''Returning the model, while making sure we have one.'''
        if new_model:
            # Creating a new model
            self.train_new_model()
        if self._model is None:
            try:
                # Loading already exiting model
                self._model = load_model(model_location)
            except OSError:
                # Creating a new model
                self.train_new_model()
        return self._model