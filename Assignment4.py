import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


def get_list_of_university_towns():
    """Returns a DataFrame of towns and the states they are in from the
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ],
    columns=["State", "RegionName"]  )

    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. """
    
    da = pd.read_csv('university_towns.txt', header=None, index_col=False, encoding='utf-8', delimiter="\n")[0]
    
    state = np.nan
    city = np.nan
    state_and_city = []
    
    for name in da:
        if '[edit]' in name:
            state = name.replace('[edit]', '')
        else:
            city = name.split('(')[0].rstrip()
            state_and_city.append([state, city])
    
    ans1 = pd.DataFrame(state_and_city, columns=['State', 'RegionName'])
    
    return ans1


def get_recession_start():
    """Returns the year and quarter of the recession start time as a
    string value in a format such as 2005q3"""

    da = pd.read_excel('gdplev.xls', header=5, skiprows=[n for n in range(6, 220)], usecols=[4, 5, 6]).rename(columns={'Unnamed: 4': 'Quarter'})

    GDP = 'GDP in billions of chained 2009 dollars.1'
    recession_start = np.nan

    for index in range(0, len(da) - 1):
        if da.loc[index][GDP] > da.loc[index + 1][GDP] > da.loc[index + 2][GDP]:
            recession_start = da.loc[index + 1]['Quarter']
            break

    ans2 = recession_start

    return ans2


def get_recession_end():
    """Returns the year and quarter of the recession end time as a
    string value in a format such as 2005q3"""

    da = pd.read_excel('gdplev.xls', header=5, skiprows=[n for n in range(6, 220)], usecols=[4, 5, 6]).rename(columns={'Unnamed: 4': 'Quarter'})

    GDP = 'GDP in billions of chained 2009 dollars.1'
    recession_end = np.nan

    recession_start = get_recession_start()
    
    for index in range(da[da['Quarter'] == recession_start].index[0], len(da) - 1):
        if da.iloc[index][GDP] < da.iloc[index + 1][GDP] < da.iloc[index + 2][GDP]:
            recession_end = da.iloc[index + 2]['Quarter']
            break
    
    ans3 = recession_end
    
    return ans3


def get_recession_bottom():
    """Returns the year and quarter of the recession bottom time as a
    string value in a format such as 2005q3"""

    da = pd.read_excel('gdplev.xls', header=5, skiprows=[n for n in range(6, 220)], usecols=[4, 5, 6]).rename(columns={'Unnamed: 4': 'Quarter'})

    GDP = 'GDP in billions of chained 2009 dollars.1'

    recession_start = get_recession_start()
    recession_end = get_recession_end()
    
    start_index = da[da['Quarter'] == recession_start].index[0]
    end_index = da[da['Quarter'] == recession_end].index[0]
    
    da = da.iloc[start_index:end_index]
    
    ans4 = da[da[GDP] == da[GDP].min()]['Quarter'].iloc[0]
    
    return ans4


def convert_housing_data_to_quarters():
    """Converts the housing data to quarters and returns it as mean
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].

    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.

    The resulting dataframe should have 67 columns, and 10,730 rows.
    """
    
    da = pd.read_csv('City_Zhvi_AllHomes.csv', usecols=(list(range(0, 6)) + list(range(51, 251))))
    
    quarters = []  # Its possible to create this using comprehensions?? I will try latter
    for year in range(2000, 2017): 
        if year != 2016:    
            for quarter in range(1, 5):
                quarters.append(str(year) + str('q') + str(quarter))
        else:
            for quarter in range(1, 4):
                quarters.append(str(year) + str('q') + str(quarter))
    
    column = 6  # First value: 2000-1 
    for quarter in quarters:
        if column != 204:  # Doing this because the last quarter has only 2 months!
            da[quarter] = da.iloc[:, column:(column + 3)].mean(axis=1)
        else:
            da[quarter] = da.iloc[:, column:(column + 2)].mean(axis=1)
        column += 3
 
    ans5 = (da.loc[:, (['State', 'RegionName'] + quarters)]
            .set_index(['State', 'RegionName'])
            .rename(index=states)
            .sort_index())
    
    return ans5


def run_ttest():
    """First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values,
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence.

    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss)."""
    
    start, bottom = get_recession_start(), get_recession_bottom()
    
    all_cities = convert_housing_data_to_quarters().loc[:, start:bottom]
    uni_cities = get_list_of_university_towns()
    
    merged = (pd.merge(all_cities, uni_cities, how='outer', indicator=True, left_index=True, right_on=['State', 'RegionName']).set_index(['State', 'RegionName']))
    da_uni = merged[merged['_merge'] == 'both'].drop('_merge', axis=1)  # Getting only the university cities where we have information about
    da_city = merged[merged['_merge'] == 'left_only'].drop('_merge', axis=1)  # Getting only the non university cities 
    
    da_uni['PriceRatio'] = da_uni[start]/da_uni[bottom]
    da_city['PriceRatio'] = da_city[start]/da_city[bottom]

    # Hypothesis: University towns have their mean housing prices less effected by recessions.
    # Run a t-test to compare the ratio of the mean price of houses in university towns the quarter
    # before the recession starts compared to the recession bottom.
    # (price_ratio=quarter_before_recession/recession_bottom)
    
    p = ttest_ind(da_uni.dropna()['PriceRatio'], da_city.dropna()['PriceRatio'])[1]
    different = p < 0.01
    if da_uni['PriceRatio'].mean() < da_city['PriceRatio'].mean():
        better = 'university town'
    else:
        better = 'non-university town'
    
    return different, p, better


if __name__ == '__main__':
    print('Ex1:\n', get_list_of_university_towns(), end='\n\n')
    print('Ex2:\n', get_recession_start(), end='\n\n')
    print('Ex3:\n', get_recession_end(), end='\n\n')
    print('Ex4:\n', get_recession_bottom(), end='\n\n')
    print('Ex5:\n', convert_housing_data_to_quarters(), end='\n\n')
    print('Ex6:\n', run_ttest(), end='\n\n')

