#Regression models
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import r2_score, mean_squared_error
import xgboost as xgb
from sklearn.neighbors import KNeighborsRegressor
import logger


class RegressionModelTuner():
    """
            This class shall be used to get the best suited Regression model

            Written By: iNeuron
            Version: 1.0
            Revisions: None

    """

    def __init__(self):
        self.file_object = open('RegressionLogs.txt', 'a+')
        self.logger_object = logger.App_Logger()

    def get_tuned_knn_model(self, x_train, y_train):
        """
            Method Name : get_tuned_knn_model

            Description : This method will be used to get the hypertuned KNN Model

            x_train : Feature Columns of Training DataSet

            y_train : Target Column of Training DataSet

            output : A hyper parameter tuned model object

            Written By: Purvansh Singh

            Version : 1.0

            Revision : None
        """
        try:
            self.logger_object.log(self.file_object,
                                   "KNN Model Training Started.")
            knn_parameters = {'n_neighbors': [50, 100, 200, 250, 300, 350],
                              'weights': ['uniform', 'distance'],
                              'algorithm': ['ball_tree', 'kd_tree'],
                              'leaf_size': [20, 25, 30, 35, 40, 45, 50],
                              }
            rmdsearch = RandomizedSearchCV(KNeighborsRegressor(), knn_parameters, n_iter=10, cv=10, random_state=22,
                                           n_jobs=-1)
            rmdsearch.fit(x_train, y_train)
            hyperparameters = rmdsearch.best_params_
            n_neighbors, weights, algorithm, leaf_size = hyperparameters['n_neighbors'], hyperparameters['weights'], \
                                                         hyperparameters['algorithm'], hyperparameters['leaf_size']
            model = KNeighborsRegressor(n_neighbors=n_neighbors,
                                        weights=weights,
                                        algorithm=algorithm,
                                        leaf_size=leaf_size,
                                        n_jobs=-1)
            model.fit(x_train, y_train)
            self.logger_object.log(self.file_object,
                                   "KNN Model successfully trained.")
            return model
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in performing Model Building and Tuning. Exception message: ' + str(
                                       e))
            raise Exception()

    def get_tuned_random_forest_model(self, x_train, y_train):
        """
        Method Name: get_tuned_random_forest_classifier

        Description: This method will be used to build RandomForestRegressor model

        Input Description:

        x_train : Feature Columns of Training DataSet

        y_train : Target Column of Training DataSet

        On Failure: Raise Exception

        Written By: Purvansh Singh

        Version: 1.0

        Revisions: None

        """
        try:
            self.logger_object.log(self.file_object,
                                   "Random Forest Model Training Started.")
            self.rf_parameters = {
                'max_depth': [5, 10, 15, 20, 25, None],
                'n_estimators': range(10, 500, 50),
                'criterion': ['mse', 'mae'],
                'bootstrap': [True, False],
                'min_samples_split': range(2, 10, 1),
                'max_features': ['auto', 'log2'],
                'min_samples_leaf': range(1, 10),
            }

            self.rmdsearch = RandomizedSearchCV(RandomForestRegressor(), self.rf_parameters, n_iter=10, cv=10,
                                                random_state=22,
                                                n_jobs=-1)
            self.rmdsearch.fit(x_train, y_train)
            hyperparameters = self.rmdsearch.best_params_
            max_depth, n_estimators, criterion, bootstrap, min_samples_split, max_features, min_samples_leaf = \
                hyperparameters['max_depth'], hyperparameters['n_estimators'], hyperparameters['criterion'], \
                hyperparameters['bootstrap'], hyperparameters['min_samples_split'], hyperparameters['max_features'], \
                hyperparameters['min_samples_leaf']

            self.model = RandomForestRegressor(n_estimators=n_estimators,
                                               max_depth=max_depth,
                                               criterion=criterion,
                                               min_samples_leaf=min_samples_leaf,
                                               max_features=max_features,
                                               min_samples_split=min_samples_split,
                                               bootstrap=bootstrap,
                                               random_state=25,
                                               n_jobs=-1)

            self.model = RandomForestRegressor(n_jobs=-1)
            self.model.fit(x_train, y_train)
            self.logger_object.log(self.file_object,
                                   "Random Forest Model successfully Trained.")
            return self.model
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in performing Model Building and Tuning. Exception message: ' + str(
                                       e))
            raise Exception()

    def get_tuned_xgboost_model(self, x_train, y_train):
        """
        Method Name: get_tuned_xgboost_model

        Description: This method will be used to build XGBoost Regressor model

        Input Description:

        x_train : Feature Columns of Training DataSet

        y_train : Target Column of Training DataSet

        On Failure: Raise Exception

        Written By: Purvansh Singh

        Version: 1.0

        Revisions: None

        """
        try:
            self.logger_object.log(self.file_object,
                                   "Xgboost Model Training Started.")
            self.xg_parameters = {"n_estimators": [10, 50, 100, 200],
                                  "learning_rate": [0.05, 0.10, 0.15, 0.20, 0.25, 0.30],
                                  "max_depth": [3, 4, 5, 6, 8, 10, 12, 15, 20],
                                  "min_child_weight": [1, 3, 5, 7],
                                  "gamma": [0.0, 0.1, 0.2, 0.3, 0.4, 0.5],
                                  "colsample_bytree": [0.3, 0.4, 0.5, 0.7]
                                  }

            self.rmdsearch = RandomizedSearchCV(xgb.XGBRegressor(objective='reg:squarederror'),param_distributions=self.xg_parameters, n_iter=10, cv=10, n_jobs=-1)
            self.rmdsearch.fit(x_train, y_train)
            hyperparameters = self.rmdsearch.best_params_
            n_estimators, min_child_weight, max_depth, learning_rate, gamma, colsample_bytree = hyperparameters[
                                                                                                    'n_estimators'], \
                                                                                                hyperparameters[
                                                                                                    'min_child_weight'], \
                                                                                                hyperparameters[
                                                                                                    'max_depth'], \
                                                                                                hyperparameters[
                                                                                                    'learning_rate'], \
                                                                                                hyperparameters[
                                                                                                    'gamma'], \
                                                                                                hyperparameters[
                                                                                                    'colsample_bytree']
            self.xgboost_model = xgb.XGBRegressor(n_estimators=n_estimators,
                                               learning_rate=learning_rate,
                                               gamma=gamma,
                                               min_child_weight=min_child_weight,
                                               max_depth=max_depth,
                                               colsample_bytree=colsample_bytree)

            self.xgboost_model = xgb.XGBRegressor(objective='reg:squarederror',n_jobs=-1)
            self.xgboost_model.fit(x_train, y_train)
            self.logger_object.log(self.file_object,
                                   "Xgboost Model Training Started.")
            return self.xgboost_model
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in performing Model Building and Tuning. Exception message: ' + str(
                                       e))
            raise Exception()