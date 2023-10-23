'''
This is a test program for our project's outputs.
The program tests whether our program correctly
pre-processes and returns a correct merged dataset,
and if our graphs correctly reflect our data by comparing
expected values such as dataset dimensions or high/low
statistics found in the map and dataset to the actual
outputs.
'''
from dataset import Dataset
from graphing import Graphing
from cse163_utils import assert_equals
import pandas as pd


def test_dataset(dataset: pd.DataFrame) -> pd.DataFrame:
    '''
    Function takes in the merged dataset checks if our program correctly
    pre-processed our data. It checks for the expected number
    of states including the District of Columbia, if our program's data
    pre-processing has filtered and merged the correct
    columns by testing the dataset shape, if the
    program has built the state acronym in the correct order,
    and if our Percent Enrolled columns store the correct
    percentage of students enrolled per state.
    '''
    # we are expecting 51 rows for 50 states and DC,
    # and 10 column values as our program should have
    # filtered for them during pre-processing. These columns are:
    # state, Enrollment 2018, Enrollment 2020, POPESTIMATE2018,
    # POPESTIMATE2020, SAT Scores 2018, GDP 2018, Percent Enrolled 2018,
    # Percent Enrolled 2020, and state acronym.
    assert_equals((51, 10), dataset.shape)
    assert_equals((['state', 'Enrollment 2018', 'Enrollment 2020',
                    'POPESTIMATE2018', 'POPESTIMATE2020',
                    'SAT Scores 2018', 'GDP 2018',
                    'Percent Enrolled 2018', 'Percent Enrolled 2020',
                    'state acronym']), dataset.columns)
    # checks first and last state and state acronym column values
    # to make sure they line up in the same rows.
    assert_equals('alabama', dataset.loc[0, 'state'])
    assert_equals('AL', dataset.loc[0, 'state acronym'])
    assert_equals('wyoming', dataset.loc[50, 'state'])
    assert_equals('WY', dataset.loc[50, 'state acronym'])
    # tests percentage of state population enrolled in education.
    assert_equals(dataset.loc[0, 'Enrollment 2018'] /
                  dataset.loc[0, 'POPESTIMATE2018'],
                  dataset.loc[0, 'Percent Enrolled 2018'])
    assert_equals(dataset.loc[0, 'Enrollment 2020'] /
                  dataset.loc[0, 'POPESTIMATE2020'],
                  dataset.loc[0, 'Percent Enrolled 2020'])
    # tests the name_to_acronym_conversion function in dataset.py
    assert_equals('CA', Dataset.name_to_acronym_conversion('california'))
    assert_equals('DC',
                  Dataset.name_to_acronym_conversion('districtofcolumbia'))
    assert_equals('California',
                  Dataset.name_to_acronym_conversion('California'))
    assert_equals('CSE', Dataset.name_to_acronym_conversion('CSE'))


def test_graphing_accuracy(dataset: pd.DataFrame) -> pd.DataFrame:
    '''
    Function takes in the merged dataset and tests if the data
    reflected on our graphs and plots are what we
    expected from our dataset.
    '''
    # tests if the mean values match what is reported on our bar graph
    assert_equals(0.153979, dataset['Percent Enrolled 2018'].mean())
    assert_equals(0.148018, dataset['Percent Enrolled 2020'].mean())
    # tests if our dataset reflects the choropleth map values by
    # testing the highest statistics from our maps and
    # comparing them to the highest values from our data
    # to see if they match up.
    assert_equals(44, dataset['Percent Enrolled 2018'].idxmax())
    assert_equals('utah', dataset.loc[44, 'state'])
    assert_equals(0.2146885, dataset['Percent Enrolled 2018'].max())
    assert_equals(44, dataset['Percent Enrolled 2020'].idxmax())
    assert_equals('utah', dataset.loc[44, 'state'])
    assert_equals(0.2072788, dataset['Percent Enrolled 2020'].max())
    # suprising because DC is a county! Zoom in on Maryland and you'll
    # find it!
    assert_equals(8, dataset['GDP 2018'].idxmax())
    assert_equals('districtofcolumbia', dataset.loc[8, 'state'])
    assert_equals(176498, dataset.loc[8, 'GDP 2018'])
    # tests SAT max scores
    assert_equals(23, dataset['SAT Scores 2018'].idxmax())
    assert_equals('minnesota', dataset.loc[23, 'state'])
    assert_equals(1298, dataset.loc[23, 'SAT Scores 2018'])


def main():
    gdp_file = './SAGDP10N__ALL_AREAS_1997_2018.csv'
    census_population_old_file = './nst-est2019-alldata.csv'
    census_population_new_file = './NST-EST2022-ALLDATA.csv'
    SAT_file = './tabn226.40.csv'
    enrollment_file = './tabn203.20.csv'
    data_formatted = Dataset(census_population_old_file,
                             census_population_new_file,
                             enrollment_file, gdp_file, SAT_file)
    super_set = data_formatted.get_data()

    test_dataset(super_set)
    test_graphing_accuracy(super_set)
    dataset = Graphing(super_set)
    dataset.bar_plot_visualize()
    dataset.data_gdp_visualize()
    dataset.data_enrollment_visualize_2018()
    dataset.data_enrollment_visualize_2020()
    dataset.data_sat_visualize()


if __name__ == '__main__':
    main()
