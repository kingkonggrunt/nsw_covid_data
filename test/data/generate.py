"""Generates Test Data"""

import pandas as pd

def generate_agerange_data():
    """AgeRange"""
    df = pd.read_csv("../../data/data/Cases_AgeRange_Dis.csv")
    df.head(100).to_csv("_test_Cases_AgeRange_Dis.csv")

    df = pd.read_csv("../../data/data/Cases_AgeRange.csv")
    df.head(100).to_csv("_test_Cases_AgeRange.csv")


def generate_location_data():
    """Location"""
    df = pd.read_csv("../../data/data/Cases_Location_Dis.csv")
    df.head(100).to_csv("_test_Cases_Location_Dis.csv")

    df = pd.read_csv("../../data/data/Cases_Location.csv")
    df.head(100).to_csv("_test_Cases_Location.csv")


def generate_tests_data():
    """Tests"""
    df = pd.read_csv("../../data/data/Tests_Location.csv")
    df.head(100).to_csv("_test_Tests_Location.csv")


def main():
    """Main"""
    generate_agerange_data()
    generate_tests_data()
    generate_location_data()

if __name__ == '__main__':
    main()
