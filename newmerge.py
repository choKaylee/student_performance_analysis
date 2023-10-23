# dataset.py

import pandas as pd
from cse163_utils import normalize_token


class Dataset:
    def __init__(self, census_older: str, census_new: str,
                 enrollment: str, gdp: str, sat: str) -> None:
        GDP = pd.read_csv(gdp, skiprows=[1, 53, 54, 55, 56, 57, 58, 59,
                                         60, 61, 62, 63])
        state_population_old = pd.read_csv(census_older,
                                           skiprows=[1, 2, 3, 4, 5, 57])
        state_population_new = pd.read_csv(census_new,
                                           skiprows=[1, 2, 3, 4, 5, 6, 7,
                                                     8, 9, 10, 11, 12, 13,
                                                     14, 66])
        SAT_scores = pd.read_csv(sat, header=1, skiprows=[2, 3, 4, 5,
                                                          6, 58, 59, 60])
        enroll_data = pd.read_csv(enrollment, header=2,
                                  skiprows=[3, 4, 5, 6, 7, 8, 9, 10, 62,
                                            63, 64, 65, 66, 67, 68, 69,
                                            70, 71, 72, 73, 74, 75, 76,
                                            77, 78])
        enroll_data = enroll_data.rename(columns={'Unnamed: 0':
                                                  'state',
                                                  'Fall 2018':
                                                  'Enrollment 2018',
                                                  'Fall 2020':
                                                  'Enrollment 2020'})
        enroll_data = enroll_data[['state', 'Enrollment 2018',
                                   'Enrollment 2020']]
        enroll_data['state'] = \
            enroll_data['state'].apply(normalize_token)
        enroll_data['Enrollment 2018'] = \
            enroll_data['Enrollment 2018'].apply(normalize_token)
        enroll_data['Enrollment 2020'] = \
            enroll_data['Enrollment 2020'].apply(normalize_token)
        enroll_data['Enrollment 2018'] = \
            pd.to_numeric(enroll_data['Enrollment 2018'])
        enroll_data['Enrollment 2020'] = \
            pd.to_numeric(enroll_data['Enrollment 2020'])
        population_data = \
            state_population_old.merge(state_population_new, left_on='NAME',
                                       right_on='NAME', how='left')
        population_data = population_data[['NAME', 'POPESTIMATE2018',
                                           'POPESTIMATE2020']]
        population_data = population_data.rename(columns={'NAME': 'state'})
        population_data['state'] = \
            population_data['state'].apply(normalize_token)
        SAT_scores = SAT_scores[['State', '2018']]
        SAT_scores = SAT_scores.rename(columns={'State': 'state',
                                                '2018': 'SAT Scores 2018'})
        SAT_scores["state"] = \
            SAT_scores['state'].apply(normalize_token)
        GDP = GDP[['GeoName', '2018']]
        GDP = GDP.rename(columns={'GeoName': 'state', '2018': 'GDP 2018'})
        GDP["state"] = GDP['state'].apply(normalize_token)
        united_data = enroll_data.merge(population_data, left_on='state',
                                        right_on='state', how='left')
        united_data = united_data.merge(SAT_scores, left_on='state',
                                        right_on='state', how='left')
        united_data = united_data.merge(GDP, left_on='state',
                                        right_on='state', how='left')
        united_data = Dataset.enrollment_averages(united_data)
        united_data = Dataset.name_to_acronym_conversion(united_data)
        self._combined_data: pd.DataFrame = united_data

    def get_data(self) -> pd.DataFrame:
        """
        returns the processed and completed dataset
        """
        return self._combined_data

    def enrollment_averages(dataset: pd.DataFrame) -> pd.DataFrame:
        dataset['Percent Enrolled 2018'] = \
            (dataset['Enrollment 2018'] /
             dataset['POPESTIMATE2018'])
        dataset['Percent Enrolled 2020'] = \
            (dataset['Enrollment 2020'] /
             dataset['POPESTIMATE2020'])
        return dataset

    def name_to_acronym_conversion(dataset: pd.DataFrame) -> pd.DataFrame:
        state_conversion = {'alabama': 'AL', 'alaska': 'AK',
                            'arizona': 'AZ', 'arkansas': 'AR',
                            'california': 'CA', 'colorado': 'CO',
                            'connecticut': 'CT', 'delaware': 'DE',
                            'districtofcolumbia': 'DC',
                            'florida': 'FL', 'georgia': 'GA',
                            'hawaii': 'HI', 'idaho': 'ID',
                            'illinois': 'IL', 'indiana': 'IN',
                            'iowa': 'IA', 'kansas': 'KS',
                            'kentucky': 'KY', 'louisiana': 'LA',
                            'maine': 'ME', 'maryland': 'MD',
                            'massachusetts': 'MA', 'michigan': 'MI',
                            'minnesota': 'MN', 'mississippi': 'MS',
                            'missouri': 'MO', 'montana': 'MT',
                            'nebraska': 'NE', 'nevada': 'NV',
                            'newhampshire': 'NH', 'newjersey': 'NJ',
                            'newmexico': 'NM', 'newyork': 'NY',
                            'northcarolina': 'NC', 'northdakota': 'ND',
                            'ohio': 'OH', 'oklahoma': 'OK',
                            'oregon': 'OR', 'pennsylvania': 'PA',
                            'rhodeisland': 'RI', 'southcarolina': 'SC',
                            'southdakota': 'SD', 'tennessee': 'TN',
                            'texas': 'TX', 'utah': 'UT', 'vermont': 'VT',
                            'virginia': 'VA', 'washington': 'WA',
                            'westvirginia': 'WV', 'wisconsin': 'WI',
                            'wyoming': 'WY'}
        acronym = []
        for state in dataset['state']:
            acronym.append(state_conversion[state])
        dataset['state acronym'] = acronym
        return dataset