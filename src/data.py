import csv
import requests
import json
from os import path, makedirs

import pandas as pd

def decode(string):
    """Decodes string for csv processing"""
    return string.decode('utf-8-sig', 'ignore')\
    .replace('\u200b', '')\
    .split(",")

def download_from_url(url, filename):
    """Download's csv's and json's from a url"""
    with requests.Session() as s:
        response = s.get(url)

        if url.endswith(".csv"):
            with open(f"{filename}.csv", 'w') as f:
                writer = csv.writer(f)
                for line in response.iter_lines():
                    writer.writerow(decode(line))

        elif url.endswith(".json"):
            with open(f"{filename}.json", 'w') as f:
                json.dump(response.json(), f)

class CovidData:
    """
    Class to download and load COVID NSW DATA
    """

    def __init__ (self, update=False):
        """Short summary.

        Parameters
        ----------
        update : type
            Description of parameter `update`.

        Returns
        -------
        __init__
            Description of returned object.

        """
        self._dir = "data/data" # Data dir

        self._sources = {
            "Cases_AgeRange":"https://data.nsw.gov.au/data/dataset/3dc5dc39-40b4-4ee9-8ec6-2d862a916dcf/resource/4b03bc25-ab4b-46c0-bb3e-0c839c9915c5/download/confirmed_cases_table2_age_group_agg.csv",
            "Cases_Location":"https://data.nsw.gov.au/data/dataset/aefcde60-3b0c-4bc0-9af1-6fe652944ec2/resource/5d63b527-e2b8-4c42-ad6f-677f14433520/download/confirmed_cases_table1_location_agg.csv",
            "Tests_Location":"https://data.nsw.gov.au/data/dataset/60616720-3c60-4c52-b499-751f31e3b132/resource/fb95de01-ad82-4716-ab9a-e15cf2c78556/download/pcr_testing_table1_location_agg.csv",
            # "Clinics":"https://data.nsw.gov.au/data/dataset/21c72b00-0834-464d-80f1-75fec38454ce/resource/85da884f-a9f5-4cb3-95e8-d6b81b0d2e3a/download/nsw-health-covid-19-test-clinics-20210920-1630.csv",
        }
        
        self._dist = {
            "Cases_AgeRange_Dis":"https://data.nsw.gov.au/data/dataset/3dc5dc39-40b4-4ee9-8ec6-2d862a916dcf/resource/24b34cb5-8b01-4008-9d93-d14cf5518aec/download/confirmed_cases_table2_age_group.csv",
            "Cases_Location_Dis":"https://data.nsw.gov.au/data/dataset/aefcde60-3b0c-4bc0-9af1-6fe652944ec2/resource/21304414-1ff1-4243-a5d2-f52778048b29/download/confirmed_cases_table1_location.csv",
        }
        
        if update:
            self.update()

    def update(self):
        """update (download) the sources"""
        
        if not path.exists(self._dir):
            makedirs(self._dir)
             
        # Only download the discontinued datasets once
        for d_source, url in self._dist.items():
            if not path.exists(path.join(self._dir, d_source)):
                download_from_url(url, path.join(self._dir, d_source))
                             
        
        for source, url in self._sources.items():
            download_from_url(url, path.join(self._dir, source))

    # TODO: update logging

    def load_csv(self, filename, **kwargs):
        """Loads a pandas dataframe, from a dataset"""
        df = pd.read_csv(path.join(self._dir,filename), **kwargs)
        return df
