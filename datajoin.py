import pandas as pd
import re

sat_file_name = "/Users/pc/OneDrive/바탕 화면/CSE 163 Summary Notes/test/cse_group_dataset/SAT_mean_score_by_state.csv"
covid_file_name = "/Users/pc/OneDrive/바탕 화면/CSE 163 Summary Notes/test/cse_group_dataset/US_covid_cases_by_state.csv"
school_file_name = "/Users/pc/OneDrive/바탕 화면/CSE 163 Summary Notes/test/cse_group_dataset/US_school_enrollment.csv"
gdp_file_name = "/Users/pc/OneDrive/바탕 화면/CSE 163 Summary Notes/test/cse_group_dataset/GDP_by_state.csv"
population_file_name = "C:/Users/pc/OneDrive/바탕 화면/CSE 163 Summary Notes/test/cse_group_dataset/population_by_state.csv"

sat_data = pd.read_csv(sat_file_name, header=1, usecols=[0, 8], skiprows=[2, 3, 4, 5, 6, 58, 59, 60])
covid_data = pd.read_csv(covid_file_name)
enrollment_data = pd.read_csv(school_file_name, header=2, skiprows=[3, 4, 5, 6, 7, 8, 9, 10, 11, 12], usecols=[0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20], nrows=61)
gdp_data = pd.read_csv(gdp_file_name, skiprows=[1, 53, 54, 55, 56, 57, 58, 59, 60, 61], usecols=[1, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30])
population_data = pd.read_csv(population_file_name)
enrollment_data = enrollment_data.rename(columns={"Unnamed: 0": "States"})

def normalize_token(token: str) -> str:
    """
    Returns a "normalized" version of the given token (str). A normalized
    token is one where all letters are converted to lowercase and all
    non-letters (e.g., punctuation) are removed.
    """
    return re.sub(r'\W+', '', str(token).lower())


def gdp_format(file: pd.DataFrame) -> pd.DataFrame:
    gdp_data["GeoName"] = gdp_data["GeoName"].apply(normalize_token)
    gdp_data = gdp_data.dropna()
    return file


def sat_format(file:pd.DataFrame) -> pd.DataFrame:
    sat_data = sat_data.rename(columns={"2018": "Sat Scores in 2018"})
    return file


def merge_data(file1:pd.DataFrame, file2:pd.DataFrame) -> pd.DataFrame:
    merged_data = enrollment_data.merge(gdp_data, left_on='States', right_on='GeoName', how='left')
    merged_data = merged_data.dropna()
    return merged_data


def enrollment_format(file: pd.DataFrame) -> pd.DataFrame:
    enrollment_data["States"] = enrollment_data['States'].apply(normalize_token)
    enrollment_data = enrollment_data.dropna()
    return file


def covid_format(file:pd.DataFrame) -> pd.DataFrame:
    covid_date = covid_data['submission_date']
    list_year = []
    for line in covid_date:
        date = line.split('/')
        for year in date:
            year = date[2]
        list_year.append(year)
    covid_data['Year'] = list_year
    covid_data = covid_data[['Year', 'state', 'tot_cases']]
    """
    state_conversion = {'AL': 'Alabama', 'AK': 'Alaska',
                            'AZ': 'Arizona', 'AR': 'Arkansas',
                            'CA': 'California', 'CO': 'Colorado',
                            'CT': 'Connecticut', 'DE': 'Delaware',
                            'DC': 'District of Columbia',
                            'FL': 'Florida', 'GA': 'Georgia',
                            'HI': 'Hawaii', 'ID': 'Idaho',
                            'IL': 'Illinois', 'IN': 'Indiana',
                            'IA': 'Iowa', 'KS': 'Kansas',
                            'KY': 'Kentucky', 'LA': 'Louisiana',
                            'ME': 'Maine', 'MD': 'Maryland',
                            'MA': 'Massachusetts', 'MI': 'Michigan',
                            'MN': 'Minnesota', 'MS': 'Mississippi',
                            'MO': 'Missouri', 'MT': 'Montana',
                            'NE': 'Nebraska', 'NV': 'Nevada',
                            'NH': 'New Hampshire', 'NJ': 'New Jersey',
                            'NM': 'New Mexico', 'NY': 'New York',
                            'NC': 'North Carolina', 'ND': 'North Dakota',
                            'OH': 'Ohio', 'OK': 'Oklahoma',
                            'OR': 'Oregon', 'PA': 'Pennsylvania',
                            'RI': 'Rhode Island', 'SC': 'South Carolina',
                            'SD': 'South Dakota', 'TN': 'Tennessee',
                            'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont',
                            'VA': 'Virginia', 'WA': 'Washington',
                            'WV': 'West Virginia', 'WI': 'Wisconsin',
                            'WY': 'Wyoming'}
    for i in covid_data['state']:
        if i in state_conversion:
            covid_data = covid_data.replace(i, state_conversion[i])
    """
    covid_data = covid_data.pivot_table('tot_cases', ['Year', 'state'])
    covid_data = covid_data.reset_index()

    total_case = []
    total_state = []
    case_2020 = []
    state_2020 = []
    case_2021 = []
    state_2021 = []
    case_2022 = []
    state_2022 = []

    for total in covid_data['tot_cases']:
        total_case.append(total)

    for each in covid_data['state']:
        total_state.append(each)

    for i in range(len(total_case)):
        if i < 60:
            case_2020.append(total_case[i])
            state_2020.append(total_state[i])
        elif i > 60 and i < 120:
            case_2021.append(total_case[i])
            state_2021.append(total_state[i])
        else:
            case_2022.append(total_case[i])
            state_2022.append(total_state[i])

    new_covid_data = pd.DataFrame(list(zip(state_2020, case_2020, state_2021, case_2021, state_2022, case_2022)),
                columns =['state_2020', 'case_2020', 'state_2021', 'case_2021', 'state_2022', 'case_2022'])
    return new_covid_data


def main():
    print(enrollment_format(enrollment_data))
    

if __name__ == '__main__':
    main()