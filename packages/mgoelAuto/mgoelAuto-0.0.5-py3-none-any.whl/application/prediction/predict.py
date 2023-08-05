import os

from fileOperations.file_methods import FileOperation
from logger.appLogger import AppLogger
from dataPreprocessing.preProcess import Preprocessor
class CustomException(Exception):
    pass

class Prediction():
    """
        This class shall  be used for prediction.

        Written By: iNeuron Intelligence
        Version: 1.0
        Revisions: None

        """

    def __init__(self):
        """
                        Method Name: __init__
                        Description: This method is for attributes initialization
                        Output: attributes

                        Written By: iNeuron Intelligence
                        Version: 1.0
                        Revisions: None

                """
        self.file_object = open('logs/predictionLogs.txt', 'a+')
        self.logger = AppLogger()
        self.file_operation = FileOperation()
        self.models_directory = 'models'
        self.preprocessor = Preprocessor()

    def predict_results(self, data, target_column, orig_data_col):
        """
            Method Name: predict_results
            Description: This method is for predicting the results of the test data
            Output: attributes
            Written By: iNeuron Intelligence
            Version: 1.0
            Revisions: None
      """
        model_name = os.chdir(self.models_directory)
        model_file_name = os.listdir()[0]
        os.chdir('../')
        #loading the best model from the directory
        model = self.file_operation.load_model(model_file_name)
        #adding the dummy target column for preprocessing the predict data
        data[target_column]=0
        difList = [string for string in orig_data_col if string not in data.columns]
        if len(difList)>0:
            self.logger.log(self.file_object,
                                   'The predict data structure is differing from trained data structure')
            raise RuntimeError("The predict data structure is differing from trained data structure. Please provide valid data ")
        try:
            #preprocess the data
            x, y = self.preprocessor.preprocess(data, target_column)
            self.logger.log(self.file_object,
                                   'Preprocessing the data to be predicted')
        except Exception as e:
            self.logger.log(self.file_object,
                                   'E : Exception occured during Preprocessing of Predictable Data' + str(
                                       e))
            raise Exception()
        self.logger.log(self.file_object,
                               'After preprocessing the data to be predicted')
        try:
            results = model.predict(x)
            data['prediction'] = results
            data.drop(target_column, axis=1, inplace=True)
        except Exception as e:
            self.logger.log(self.file_object,
                                   'E : Exception occured during predicting the data after preprocessing' + str(
                                       e))
            raise Exception()
        self.logger.log(self.file_object,
                               'Model Prediction completed')
        return data
