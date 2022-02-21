import pandas as pd
from .data import CovidData


def filter_before_discontinued_date_and_convert_dt_to_string(df: pd.DataFrame):
    """
    discontinued datasets needs data from the 2022-01-20 onwards to be removed
    (new datasets start from then) and have the datetime columns to be regularised 
    back to string format
    """

    dis_date = "2022-01-20"
    out = df[df['notification_date'] < dis_date].copy()
    out['notification_date'] = out['notification_date'].apply(lambda x: "%d-%02d-%02d" % (x.year, x.month, x.day))
        # 20-02-2020: performance fix. using apply to create date strings is 60% faster than using dt.strfrtime. This is also the fastest string formatting method.
    return out

class AgeGroup():
    """AgeGroup Data Class"""
    
    data = "Cases_AgeRange.csv"
    data_dis = "Cases_AgeRange_Dis.csv"
    _covid = CovidData()

    def __init__(self):
        self.df = self._covid.load_csv(self.data)
        self.df_dis = filter_before_discontinued_date_and_convert_dt_to_string(
            self._covid.load_csv(self.data_dis, parse_dates=['notification_date'])
            )

    def age_group_totals(self):
        """return the total age group data"""

        d_new = self.df.groupby('age_group').sum().to_dict('dict')['confirmed_cases_count']
        d_dis = self.df_dis.groupby(['age_group']).count().to_dict('dict')['notification_date']

        # update the new data with the discounted data
        for group in d_new:
            d_new[group] += d_dis[group]
            
        return d_new
        
    def age_group_overtime(self, age_group):
        """return case data for an age group overtime"""
        
        d_new = self.df[self.df["age_group"] == f"AgeGroup_{age_group}"].drop('age_group', axis=1).groupby('notification_date').sum().to_dict(orient='dict')['confirmed_cases_count']
        d_dis = self.df_dis[self.df_dis['age_group'] == f"AgeGroup_{age_group}"].groupby('notification_date').count().to_dict('dict')['age_group']
        
        d_dis.update(d_new)
        return d_dis


class CaseLocation():
    """Case Location Data Class"""
    
    data = "Cases_Location.csv"
    data_dis = "Cases_Location_Dis.csv"
    _covid = CovidData()

    def __init__(self):
        self.df: pd.DataFrame = self._covid.load_csv(self.data)
        self.df_dis = filter_before_discontinued_date_and_convert_dt_to_string(
            self._covid.load_csv(self.data_dis, parse_dates=['notification_date'])
            )

    def list_locations(self, type: str):
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
        _out = self.df[locations[type]].drop_duplicates()
        if type != "postcode":
            return _out.set_index(locations[type][0]).to_dict(orient='dict')[locations[type][1]]
        return _out.to_dict(orient='dict')[locations[type][0]]

    def postcode(self, postcode):
        """Return daily postcode case data"""
        dropped_cols = ['lhd_2010_code', 'lhd_2010_name', 'lga_code19', 'lga_name19']
        d_new = self.df.drop(dropped_cols, axis=1)[self.df['postcode'] == postcode].groupby('notification_date').sum().to_dict(orient='dict')['confirmed_cases_count']
        d_dis = self.df_dis.drop(dropped_cols, axis=1)[self.df_dis['postcode'] == postcode].groupby('notification_date').count().to_dict('dict')['postcode']
        d_dis.update(d_new)
        return d_dis
     
    def lga(self, lga):
        """Return daily lga case data"""
        if lga.isdigit():
            dropped_cols = ['lhd_2010_code', 'lhd_2010_name', 'lga_name19', 'postcode']
            d_new = self.df.drop(dropped_cols, axis=1)[self.df['lga_code19'] == lga].groupby('notification_date').sum().to_dict(orient='dict')['confirmed_cases_count']
            d_dis = self.df_dis.drop(dropped_cols, axis=1)[self.df_dis['lga_code19'] == lga].groupby('notification_date').count().to_dict('dict')['lga_code19']
            d_dis.update(d_new)
            return d_dis
        else:
            dropped_cols = ['lhd_2010_code', 'lhd_2010_name', 'lga_code19', 'postcode']
            d_new = self.df.drop(dropped_cols, axis=1)[self.df['lga_name19'] == lga].groupby('notification_date').sum().to_dict(orient='dict')['confirmed_cases_count']
            d_dis = self.df_dis.drop(dropped_cols, axis=1)[self.df_dis['lga_name19'] == lga].groupby('notification_date').count().to_dict('dict')['lga_name19']
            d_dis.update(d_new)
            return d_dis

    def lhd(self, lhd):
        """Return daily lhd case data"""
        if (lhd.startswith("X")) or (lhd == "HotelQ"):
            dropped_cols = ['lhd_2010_name', 'postcode', 'lga_name19', 'lga_name19']
            d_new = self.df.drop(dropped_cols, axis=1)[self.df['lhd_2010_code'] == lhd].groupby('notification_date').sum().to_dict(orient='dict')['confirmed_cases_count']
            d_dis = self.df_dis.drop(dropped_cols, axis=1)[self.df_dis['lhd_2010_code'] == lhd].groupby('notification_date').count().to_dict('dict')['lhd_2010_code']
            d_dis.update(d_new)
            return d_dis
        else:
            dropped_cols = ['lhd_2010_code', 'postcode', 'lga_name19', 'lga_name19']
            d_new = self.df.drop(dropped_cols, axis=1)[self.df['lhd_2010_name'] == lhd].groupby('notification_date').sum().to_dict(orient='dict')['confirmed_cases_count']
            d_dis = self.df_dis.drop(dropped_cols, axis=1)[self.df_dis['lhd_2010_name'] == lhd].groupby('notification_date').count().to_dict('dict')['lhd_2010_name']
            d_dis.update(d_new)
            return d_dis


class Tests():
    """Tests Data Class"""
    
    data = "Tests_Location.csv"
    _covid = CovidData()
    
    def __init__(self):
        self.df = self._covid.load_csv(self.data)

    def postcode(self, postcode):
        """return postcode test data overtime"""
        return self.df[self.df['postcode'] == postcode].groupby('test_date').sum().to_dict(orient='dict')['test_count']

    def lga(self, lga):
        """return lga test data overtime

        Parameters
        ----------
        lga : str
            can be a lga code or lga name
        """

        # checks if an lga code (numeric) is given, else assume an lga name
        if lga.isdigit():
            return self.df[self.df['lga_code19'] == lga].groupby('test_date').sum().to_dict(orient='dict')['test_count']
        else:
            return self.df[self.df['lga_name19'] == lga].groupby('test_date').sum().to_dict(orient='dict')['test_count']

    def lhd(self, lhd):
        """return lhd test data over time

        Parameters
        ----------
        lhd : str
            can be lhd code or lhd name
        """

        # checks if lhd is code is given, else assume lhd name
        if (lhd.startswith("X")) or (lhd == "HotelQ"):
            return self.df[self.df['lhd_2010_code'] == lhd].groupby('test_date').sum().to_dict(orient='dict')['test_count']
        else:
            return self.df[self.df['lhd_2010_name'] == lhd].groupby('test_date').sum().to_dict(orient='dict')['test_count']
