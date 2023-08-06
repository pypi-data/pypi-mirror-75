import numpy as np
import pandas as pd


class Blueprint:

    def __init__(self, data):
        self.data = data


    def create_plan(self):
        self.plan = dict()


    def __include_on_list(self, plan, key, features):

        if plan.get(key, True) is True:            
            plan[key] = features
        else:
            plan[key] = plan[key] + features
        return plan

    def __include_on_pairwise_list(self, plan, key, features, value):

        if plan.get(key, True) is True:
            plan[key] = {}
            if len(value) == 1:
                value = value * len(features)
            plan[key]["var"] = features
            plan[key]["value"] = value
        else:
            plan[key]["var"] = plan[key]["var"] + features
            plan[key]["value"] = plan[key]["value"] + value
        return plan

    # Original Feature

    def keep_original_feature(self, features):
        key = "keep_original_feature"
        self.plan = self.__include_on_list(self.plan, key, features)
    
    # Imputation methods

    def impute_missing_as_category(self, features):
        key = "impute_missing_as_category"
        self.plan = self.__include_on_list(self.plan, key, features)
        return self


    def impute_missing_as_inf(self, features):
        key = "impute_missing_as_inf"
        self.plan = self.__include_on_list(self.plan, key, features)
        return self

    
    def impute_missing_as_zero(self, features):
        key = "impute_missing_as_zero"
        self.plan = self.__include_on_list(self.plan, key, features)
        return self


    def impute_missing_as_number(self, features, number):
        key = "impute_missing_as_number"
        self.plan = self.__include_on_pairwise_list(self.plan, key, features, number)
        return self