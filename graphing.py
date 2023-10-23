'''
This program represents the Graphing Class, which
takes in a dataset and contains functions that
plot choropleth maps and a bar graph.
'''
import pandas as pd
import plotly.graph_objects as go


class Graphing:
    """
    A Graphing object contains functions that can plot
    choropleth and bar graph from a given dataset.
    This dataset must contain the correct columns:
    state, Enrollment 2018, Enrollment 2020, POPESTIMATE2018,
    POPESTIMATE2020, SAT Scores 2018, GDP 2018,
    Percent Enrolled 2018, Percent Enrolled 2020, and
    state acronym.
    """
    def __init__(self, dataset: pd.DataFrame) -> None:
        """
        Initializes a Graphing object for a combined dataset,
        made up of all the relevant columns from all the given
        datasets, along with a state acronym column, and two
        columns for the percent of people enrolled in education
        per state.
        """
        self._superset: pd.DataFrame = dataset

    def data_enrollment_visualize_2020(self) -> pd.DataFrame:
        """
        Represents the merged Dataset, which is made up of all
        the relevant columns from all the given datasets, along
        with a state acronym column, and two columns for the
        percent of people enrolled in education per state.
        """
        fig = go.Figure(data=go.Choropleth(
                        locations=self._superset['state acronym'],
                        z=self._superset['Percent Enrolled 2020'].
                        astype(float),
                        locationmode='USA-states',
                        colorscale='Reds',
                        colorbar_title='Percent of Students Enrolled',
                        ))
        fig.update_layout(
            title_text='Percent of Students Enrolled in Education in 2020 \
(During Covid)',
            geo_scope='usa')
        fig.show()

    def data_enrollment_visualize_2018(self) -> pd.DataFrame:
        """
        Takes a merged dataset and produces a choropleth map
        showing the average student enrollment of each state
        for the year of 2018
        """
        fig = go.Figure(data=go.Choropleth(
            locations=self._superset['state acronym'],
            z=self._superset['Percent Enrolled 2018'].astype(float),
            locationmode='USA-states',
            colorscale='Reds',
            colorbar_title='Percent of Students Enrolled',
        ))
        fig.update_layout(
            title_text='Percent of Students Enrolled in Education in 2018 \
(Pre-Covid)',
            geo_scope='usa')
        fig.show()

    def data_gdp_visualize(self) -> pd.DataFrame:
        """
        Takes a merged dataset and produces a choropleth map
        showing the GDP of each state for the year of 2018
        """
        fig = go.Figure(data=go.Choropleth(
            locations=self._superset['state acronym'],
            z=self._superset['GDP 2018'].astype(float),
            locationmode='USA-states',
            colorscale='Blues',
            colorbar_title='GDP',
        ))
        fig.update_layout(
            title_text='GDP by State in 2018',
            geo_scope='usa',
        )
        fig.show()

    def bar_plot_visualize(self) -> pd.DataFrame:
        """
        Takes a merged dataset and produces a barplot
        showing the average percentage of student enrollment
        for the year of 2018 and 2020
        """
        x = ['Pre-Covid (2018)', 'During Covid (2020)']
        y = [self._superset['Percent Enrolled 2018'].mean(),
             self._superset['Percent Enrolled 2020'].mean()]
        # Use the hovertext kw argument for hover text
        fig = go.Figure(data=[go.Bar(x=x, y=y,
                        hovertext=['average percentage of \
                                   students enrolled',
                                   'average percentage \
                                   of students enrolled'])])
        # Customize aspect
        fig.update_traces(marker_color='rgb(158,202,225)',
                          marker_line_color='rgb(8,48,107)',
                          marker_line_width=1.5, opacity=0.6)
        fig.update_layout(title_text='Average percentage of students \
enrolled in 2018/2020')
        fig.show()

    def data_sat_visualize(self) -> pd.DataFrame:
        """
        Takes a merged dataset and produces a choropleth map
        showing the average SAT Scores of each state for the
        year of 2018
        """
        fig = go.Figure(data=go.Choropleth(
            locations=self._superset['state acronym'],
            z=self._superset['SAT Scores 2018'].astype(float),
            locationmode='USA-states',
            colorscale='Blues',
            colorbar_title='Average SAT Scores',
        ))
        fig.update_layout(
            title_text='Average SAT scores of 2018 for each state',
            geo_scope='usa',
        )
        fig.show()
