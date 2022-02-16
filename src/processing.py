import pandas as pd
from .data import CovidData

# TODO: integrate discontinued data because the arrg data only shows data after the 20-1-2020

class AgeGroup():

    def __init__(self, df):
        self._df = df
        self.data = self._df

        # self._data = CovidData()
        # self.df_current = self._data.load("Cases_AgeRange.csv", parse_dates=['notification_date'])
        # self.df_dis = self._data.load("Cases_AgeRange_Dis.csv", parse_dates=['notification_date'])


    def reset(self):
        """reset the dataframe"""
        self.data = self._df

    def age_group_totals(self):
        """return the total age group data"""
        self.data = self.data.groupby(["age_group"]).sum().to_dict(orient="dict")['confirmed_cases_count']

    def age_group_overtime(self, age_group):
        """return case data for an age group overtime"""
        self.data = self.data[self.data["age_group"] == f"AgeGroup_{age_group}"].drop('age_group', axis=1).groupby('notification_date').sum().to_dict(orient='dict')['confirmed_cases_count']


class CaseLocation():

    def __init__(self, df):
        self._df = df
        self.data = self._df  # allow resetting of df

    def reset(self):
        """reset the dataframe"""
        self.data = self._df

    def list_locations(self, type):
        """acquire the list of locations of the location type - for use in the api

        Parameters
        ----------
        type : str
            location type to list (lhd, lga, postcode)
        """

        locations = {  # column names are order for human-readable output
            "lhd" : ['lhd_2010_name', 'lhd_2010_code'],
            "lga" : ['lga_name19', 'lga_code19'],
            "postcode" : ['postcode']
        }

        # process out df differently if the type is `postcode`
        _out = self.data[locations[type]].drop_duplicates()
        if type == "postcode":
            _out = _out.to_dict(orient='dict')[locations[type][0]]
        else:
            _out = _out.set_index(locations[type][0]).to_dict(orient='dict')[locations[type][1]]

        self.data = _out

    def postcode(self, postcode):
        self.data = self.data.drop(['lhd_2010_code', 'lhd_2010_name', 'lga_code19', 'lga_name19'], axis=1)[self.data['postcode'] == postcode].groupby('notification_date').sum().to_dict(orient='dict')['confirmed_cases_count']

    def lga(self, lga):

        if lga.isdigit():
            self.data = self.data.drop(['lhd_2010_code', 'lhd_2010_name', 'lga_name19', 'postcode'], axis=1)[self.data['lga_code19'] == lga].groupby('notification_date').sum().to_dict(orient='dict')['confirmed_cases_count']
        else:
            self.data = self.data.drop(['lhd_2010_code', 'lhd_2010_name', 'lga_code19', 'postcode'], axis=1)[self.data['lga_name19'] == lga].groupby('notification_date').sum().to_dict(orient='dict')['confirmed_cases_count']

    def lhd(self, lhd):

        if (lhd.startswith("X")) or (lhd == "HotelQ"):
            self.data = self.data.drop(['lhd_2010_name', 'postcode', 'lga_name19', 'lga_name19'], axis=1)[self.data['lhd_2010_code'] == lhd].groupby('notification_date').sum().to_dict(orient='dict')['confirmed_cases_count']
        else:
            self.data = self.data.drop(['lhd_2010_code', 'postcode', 'lga_name19', 'lga_name19'], axis=1)[self.data['lhd_2010_name'] == lhd].groupby('notification_date').sum().to_dict(orient='dict')['confirmed_cases_count']


class Tests():
    def __init__(self, df):
        self._df = df
        self.data = self._df  # allow resetting of df

    def reset(self):
        """reset the dataframe"""
        self.data = self._df

    def postcode(self, postcode):
        """return postcode test data overtime"""
        self.data = self.data[self.data['postcode'] == postcode].groupby('test_date').sum().to_dict(orient='dict')['test_count']

    def lga(self, lga):
        """return lga test data overtime

        Parameters
        ----------
        lga : str
            can be a lga code or lga name
        """

        # checks if an lga code (numeric) is given, else assume an lga name
        if lga.isdigit():
            self.data = self.data[self.data['lga_code19'] == lga].groupby('test_date').sum().to_dict(orient='dict')['test_count']
        else:
            self.data = self.data[self.data['lga_name19'] == lga].groupby('test_date').sum().to_dict(orient='dict')['test_count']

    def lhd(self, lhd):
        """return lhd test data over time

        Parameters
        ----------
        lhd : str
            can be lhd code or lhd name
        """

        # checks if lhd is code is given, else assume lhd name
        if (lhd.startswith("X")) or (lhd == "HotelQ"):
            self.data = self.data[self.data['lhd_2010_code'] == lhd].groupby('test_date').sum().to_dict(orient='dict')['test_count']
        else:
            self.data = self.data[self.data['lhd_2010_name'] == lhd].groupby('test_date').sum().to_dict(orient='dict')['test_count']
