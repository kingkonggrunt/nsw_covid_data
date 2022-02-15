import pandas as pd
from data import CovidData

# TODO: integrate discontinued data because the arrg data only shows data after the 20-1-2020

class AgeGroup():

    def __init__(self, df):
        self._df = df
        self.data = self.df

        # self._data = CovidData()
        # self.df_current = self._data.load("Cases_AgeRange.csv", parse_dates=['notification_date'])
        # self.df_dis = self._data.load("Cases_AgeRange_Dis.csv", parse_dates=['notification_date'])


    def reset():
        """reset the dataframe"""
        self.data = self._df

    def age_group_totals():
        """return the total age group data"""
        self.data = self.data.groupby(["age_group"]).sum().to_dict(orient="dict")['confirmed_cases_count']

    def age_group_overtime(age_group):
        """return case data for an age group overtime"""
        self.data = df[df["age_group"] == f"AgeGroup_{age_group}"].drop('age_group', axis=1).set_index(['notification_date', 'confirmed_by_pcr']).to_dict(orient='index')['confirmed_cases_count']


class CaseLocation():

    def __init__(self, df):
        self._df = df
        self.data = self._df  # allow resetting of df

    def reset():
        """reset the dataframe"""
        self.data = self._df

    def list_locations(type):
        """acquire the list of locations of the location type - for use in the api

        Parameters
        ----------
        type : str
            location type to list (lhd, lga, postcode)
        """

        locations = {  # column names are order for human-readable output
            "lhd" : ['lhd_2010_name', 'lhd_2010_code'],
            "lga" : ['lga_name19', 'loga_code19'],
            "postcode" : ['postcode']
        }

        # process out df differently if the type is `postcode`
        _out = self.data[locations[type]].drop_duplicates()
        if type == "postcode":
            _out = _out.to_dict(orient='dict')[locations[type][0]]
        else:
            _out = _out.set_index(locations[type][0]).to_dict(orient='dict')[locations[type][1]]

        self.data = _out

    def postcode_overtime(code):
        _out = self.data,drop(['lhd_2010_code', 'lhd_2010_name', 'lga_code19', 'lga_name19'], axis=1)[df['postcode' == code]].set_index(['notification_date', 'confirmed_by_pcr']).to_dict(orient='dict')['postcode']
