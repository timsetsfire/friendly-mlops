import yaml
import logging
from abc import ABC, abstractmethod



class HumilityRules(object):
    def __init__(self):
        ## logging.
        logging.basicConfig(
                format="{} - %(levelname)s - %(asctime)s - %(message)s".format(__name__),
        )
        self.logger = logging.getLogger("humility")
        self.logger.setLevel("INFO")
        self.counter = 0
    @abstractmethod
    def humility(self, **kwargs):
        pass


class KnownCategories(HumilityRules):
    def __init__(self, **kwargs):
        self.known_values = kwargs["known_values"]
        self.feature = kwargs["feature"]
        super(KnownCategories, self).__init__()

    def humility(self, df):
        data = df.copy()
        data[f"{self.feature}_unknown_value"] = data[self.feature].apply(
            lambda x: x not in self.known_values
        )
        self.counter += data[data[f"{self.feature}_unknown_value"] == True].shape[0]
        new_levels = data[data[f"{self.feature}_unknown_value"] == True][self.feature].unique()
        if len(new_levels) > 0:
            self.logger.warn(f"new levels detected for feature {self.feature}: {new_levels}")
        return data


class OutlyingInput(HumilityRules):
    def __init__(self, **kwargs):
        self.lower_bound = kwargs["bounds"]["lower_bound"]
        self.upper_bound = kwargs["bounds"]["upper_bound"]
        self.feature = kwargs["feature"]
        super(OutlyingInput, self).__init__()

    def humility(self, df):
        data = df.copy()
        data[f"{self.feature}_outlying_input"] = data[self.feature].apply(
            lambda x: (x > self.upper_bound) & (x < self.lower_bound)
        )
        temp = self.counter
        self.counter += data[data[f"{self.feature}_outlying_input"] != True].shape[0]
        if temp < self.counter:
            self.logger.warn(f"input not in [{self.lower_bound}, {self.upper_bound}] for feature {self.feature}")
        return data


class UncertainPrediction(HumilityRules):
    def __init__(self, **kwargs):
        self.lower_bound = kwargs["bounds"]["lower_bound"]
        self.upper_bound = kwargs["bounds"]["upper_bound"]
        self.prediction_column = kwargs["prediction_column"]
        super(UncertainPrediction, self).__init__()

    def humility(self, df):
        data = df.copy()
        data["uncertain_prediction"] = data[
            self.prediction_column
        ].apply(lambda x: (x <= self.upper_bound) & (x >= self.lower_bound))
        temp = self.counter
        self.counter += data[data["uncertain_prediction"] == True].shape[0]
        if temp < self.counter:
            self.logger.warning("uncertain prediction made")
        return data


class Humility(object):
    def __init__(self, config_file, log_file=None, logging_level="INFO"):
        with open(config_file, "r") as f:
            self.config_dict = yaml.load(f, Loader=yaml.FullLoader)
        self.humility_rules = []

        self.humility_counter = {
            "categorical": 0,
            "outlying_input": 0,
            "uncertain_prediction": 0,
        }
        self.new_columns_features = []
        self.new_columns_prediction = []


        for entry in self.config_dict:
            if entry["rule"] == "categorical":
                rule = (entry["feature"], KnownCategories(**entry))
                self.new_columns_features.append( f"{entry['feature']}_unknown_value")
            elif entry["rule"] == "outlying_input":
                rule = (entry["feature"], OutlyingInput(**entry))
                self.new_columns_features.append( f"{entry['feature']}_outlying_input")
            elif entry["rule"] == "uncertain_prediction":
                rule = (entry["prediction_column"], UncertainPrediction(**entry))
                self.new_columns_prediction.append( "uncertain_prediction" )
            else:
                print(f"unknown rule {entry['rule']} not supported")
            self.humility_rules.append(rule)

    def check_input_humility(self, data):
        for rule in self.humility_rules:
            if type(rule[1]) is UncertainPrediction:
                pass
            elif type(rule[1]) is KnownCategories:
                data = rule[1].humility(data)
            elif type(rule[1]) is OutlyingInput:
                data = rule[1].humility(data)
            else:
                raise Exception("unknown humility rule")
        return data
    def check_output_humility(self, data):
        for rule in self.humility_rules:
            if type(rule[1]) is UncertainPrediction:
                data = rule[1].humility(data)
            else:
                pass
        return data
