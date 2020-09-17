import pandas as pd
import numpy as np


# Assignment 3 - More Pandas
# This assignment requires more individual learning then the last one did - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.

# ### Question 1 (20%)
# Load the energy data from the file `Energy Indicators.xls`, which is a list of indicators of [energy supply and renewable electricity production](Energy%20Indicators.xls) from the [United Nations](http://unstats.un.org/unsd/environment/excel_file_tables/2013/Energy%20Indicators.xls) for the year 2013, and should be put into a DataFrame with the variable name of **energy**.
# 
# Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:
# 
# `['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']`
# 
# Convert `Energy Supply` to gigajoules (there are 1,000,000 gigajoules in a petajoule). For all countries which have missing data (e.g. data with "...") make sure this is reflected as `np.NaN` values.
# 
# Rename the following list of countries (for use in later questions):
# 
# ```"Republic of Korea": "South Korea",
# "United States of America": "United States",
# "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
# "China, Hong Kong Special Administrative Region": "Hong Kong"```
# 
# There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these, 
# 
# e.g. 
# 
# `'Bolivia (Plurinational State of)'` should be `'Bolivia'`, 
# 
# `'Switzerland17'` should be `'Switzerland'`.
# 
# <br>
# 
# Next, load the GDP data from the file `world_bank.csv`, which is a csv containing countries' GDP from 1960 to 2015 from [World Bank](http://data.worldbank.org/indicator/NY.GDP.MKTP.CD). Call this DataFrame **GDP**. 
# 
# Make sure to skip the header, and rename the following list of countries:
# 
# ```"Korea, Rep.": "South Korea", 
# "Iran, Islamic Rep.": "Iran",
# "Hong Kong SAR, China": "Hong Kong"```
# 
# <br>
# 
# Finally, load the [Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology](http://www.scimagojr.com/countryrank.php?category=2102) from the file `scimagojr-3.xlsx`, which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame **ScimEn**.
# 
# Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15). 
# 
# The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
#        'Citations per document', 'H index', 'Energy Supply',
#        'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008',
#        '2009', '2010', '2011', '2012', '2013', '2014', '2015'].
# 
# *This function should return a DataFrame with 20 columns and 15 entries.*

# ### Question 2 (6.6%)
# The previous question joined three datasets then reduced this to just the top 15 entries. When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?
# 
# *This function should return a single number.*

def answer_one():
    # First DataFrame
    da1 = pd.read_excel('Energy Indicators.xls', usecols=[2, 3, 4, 5],
                        names=['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable'],
                        skiprows=17, skipfooter=38)

    da1['Energy Supply'] *= 1000000

    for row in da1.index:
        if type(da1.loc[row, 'Energy Supply']) is not int:
            da1.loc[row, 'Energy Supply'] = np.nan
        if type(da1.loc[row, 'Energy Supply per Capita']) is not int:
            da1.loc[row, 'Energy Supply per Capita'] = np.nan

    da1['Country'] = (da1['Country']
                      .str.replace("\d+", "")
                      .str.replace(r"\(.*\)", "")
                      .str.strip()
                      .replace({"Republic of Korea": "South Korea",
                                "United States of America": "United States",
                                "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
                                "China, Hong Kong Special Administrative Region": "Hong Kong"}))

    energy = da1

    # Second DataFrame
    da2 = (pd.read_csv('world_bank.csv', skiprows=4)
           .replace({"Korea, Rep.": "South Korea",
                     "Iran, Islamic Rep.": "Iran",
                     "Hong Kong SAR, China": "Hong Kong"})
           .rename(columns={'Country Name': 'Country'})
           .drop((['Country Code', 'Indicator Name', 'Indicator Code'] + [str(year) for year in range(1960, 2006)]),
                 axis=1))

    GPD = da2

    # Third DataFrame
    da3 = pd.read_excel('scimagojr-3.xlsx')

    ScimEn = da3

    # Merging all the DataFrames 

    ans1 = (pd.merge(pd.merge(ScimEn, energy, how='inner', left_on='Country', right_on='Country'),
                     GPD, how='inner', left_on='Country', right_on='Country').set_index('Country')
            .sort_values(by='Rank')
            .head(15))

    return ans1


def answer_two():
    # First DataFrame
    da1 = pd.read_excel('Energy Indicators.xls', usecols=[2, 3, 4, 5],
                        names=['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable'],
                        skiprows=17, skipfooter=38)

    da1['Energy Supply'] *= 1000000

    for row in da1.index:
        if type(da1.loc[row, 'Energy Supply']) is not int:
            da1.loc[row, 'Energy Supply'] = np.nan
        if type(da1.loc[row, 'Energy Supply per Capita']) is not int:
            da1.loc[row, 'Energy Supply per Capita'] = np.nan

    da1['Country'] = (da1['Country']
                      .str.replace("\d+", "")
                      .str.replace(r"\(.*\)", "")
                      .str.strip()
                      .replace({"Republic of Korea": "South Korea",
                                "United States of America": "United States",
                                "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
                                "China, Hong Kong Special Administrative Region": "Hong Kong"}))

    energy = da1

    # Second DataFrame
    da2 = (pd.read_csv('world_bank.csv', skiprows=4)
           .replace({"Korea, Rep.": "South Korea",
                     "Iran, Islamic Rep.": "Iran",
                     "Hong Kong SAR, China": "Hong Kong"})
           .rename(columns={'Country Name': 'Country'})
           .drop((['Country Code', 'Indicator Name', 'Indicator Code'] + [str(year) for year in range(1960, 2006)]),
                 axis=1))

    GPD = da2

    # Third DataFrame
    da3 = pd.read_excel('scimagojr-3.xlsx')

    ScimEn = da3

    # Calculating value

    ans1 = len(pd.merge(pd.merge(ScimEn, energy, how='inner', left_on='Country', right_on='Country'),
                        GPD, how='inner', left_on='Country', right_on='Country').set_index('Country'))

    ans2 = len(pd.merge(pd.merge(ScimEn, energy, how='outer', left_on='Country', right_on='Country'),
                        GPD, how='outer', left_on='Country', right_on='Country').set_index('Country')) - ans1

    return ans2


# ## Answer the following questions in the context of only the top 15 countries by Scimagojr Rank (aka the DataFrame returned by `answer_one()`)

# ### Question 3 (6.6%)
# What is the average GDP over the last 10 years for each country? (exclude missing values from this calculation.)
# 
# *This function should return a Series named `avgGDP` with 15 countries and their average GDP sorted in descending order.*

def answer_three():
    Top15 = answer_one()
    ans3 = (
        pd.Series(np.mean(Top15[[str(year) for year in range(2006, 2016)]], axis=1), index=Top15.index, name='avgGDP')
            .sort_values(ascending=False))

    return ans3


# ### Question 4 (6.6%)
# By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?
# 
# *This function should return a single number.*

def answer_four():
    Top15 = answer_one()
    Top6 = \
        (pd.Series(np.mean(Top15[[str(year) for year in range(2006, 2016)]], axis=1), index=Top15.index, name='avgGDP')
         .sort_values(ascending=False)).index[5]
    ans4 = Top15.loc[Top6, '2015'] - Top15.loc[Top6, '2006']

    return ans4


# ### Question 5 (6.6%)
# What is the mean `Energy Supply per Capita`?
# 
# *This function should return a single number.*

def answer_five():
    Top15 = answer_one()
    ans5 = np.mean(Top15['Energy Supply per Capita'], axis=0)

    return float(ans5)


# ### Question 6 (6.6%)
# What country has the maximum % Renewable and what is the percentage?
# 
# *This function should return a tuple with the name of the country and the percentage.*

def answer_six():
    Top15 = answer_one()
    ans6 = Top15['% Renewable'].argmax(), Top15['% Renewable'].max()

    return ans6


# ### Question 7 (6.6%)
# Create a new column that is the ratio of Self-Citations to Total Citations. 
# What is the maximum value for this new column, and what country has the highest ratio?
# 
# *This function should return a tuple with the name of the country and the ratio.*

def answer_seven():
    Top15 = answer_one()
    Top15['Ratio Sc/Tc'] = Top15['Self-citations'] / Top15['Citations']
    ans7 = Top15['Ratio Sc/Tc'].argmax(), Top15['Ratio Sc/Tc'].max()

    return ans7


# ### Question 8 (6.6%)
# 
# Create a column that estimates the population using Energy Supply and Energy Supply per capita. 
# What is the third most populous country according to this estimate?
# 
# *This function should return a single string value.*

def answer_eight():
    Top15 = answer_one()
    Top15['PopEst'] = (Top15['Energy Supply'] / Top15['Energy Supply per Capita'])
    ans8 = Top15['PopEst'].sort_values(ascending=False).index[2]

    return ans8


# ### Question 9 (6.6%)
# Create a column that estimates the number of citable documents per person. 
# What is the correlation between the number of citable documents per capita and the energy supply per capita? Use the `.corr()` method, (Pearson's correlation).
# 
# *This function should return a single number.*
# 
# *(Optional: Use the built-in function `plot9()` to visualize the relationship between Energy Supply per Capita vs. Citable docs per Capita)*

def answer_nine():
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']
    ans9 = (Top15['Citable docs per Capita'].astype(float)).corr((Top15['Energy Supply per Capita'].astype(float)))

    return ans9


# ### Question 10 (6.6%)
# Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median.
# 
# *This function should return a series named `HighRenew` whose index is the country name sorted in ascending order of rank.*

def answer_ten():
    Top15 = answer_one()
    median = np.median(Top15['% Renewable'], axis=0)

    for country in Top15.index:
        if Top15.loc[country, '% Renewable'] >= median:
            Top15.loc[country, 'RenAvg'] = 1
        else:
            Top15.loc[country, 'RenAvg'] = 0
    ans10 = pd.Series(Top15['RenAvg'], dtype='int64', name='HighRenew')

    return ans10


# ### Question 11 (6.6%)
# Use the following dictionary to group the Countries by Continent, then create a dateframe that displays the sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated population of each country.
# 
# ```python
# ContinentDict  = {'China':'Asia', 
#                   'United States':'North America', 
#                   'Japan':'Asia', 
#                   'United Kingdom':'Europe', 
#                   'Russian Federation':'Europe', 
#                   'Canada':'North America', 
#                   'Germany':'Europe', 
#                   'India':'Asia',
#                   'France':'Europe', 
#                   'South Korea':'Asia', 
#                   'Italy':'Europe', 
#                   'Spain':'Europe', 
#                   'Iran':'Asia',
#                   'Australia':'Australia', 
#                   'Brazil':'South America'}
# ```
# 
# *This function should return a DataFrame with index named Continent `['Asia', 'Australia', 'Europe', 'North America', 'South America']` and columns `['size', 'sum', 'mean', 'std']`*

def answer_eleven():
    Top15 = answer_one()
    ContinentDict = {'China': 'Asia',
                     'United States': 'North America',
                     'Japan': 'Asia',
                     'United Kingdom': 'Europe',
                     'Russian Federation': 'Europe',
                     'Canada': 'North America',
                     'Germany': 'Europe',
                     'India': 'Asia',
                     'France': 'Europe',
                     'South Korea': 'Asia',
                     'Italy': 'Europe',
                     'Spain': 'Europe',
                     'Iran': 'Asia',
                     'Australia': 'Australia',
                     'Brazil': 'South America'}

    ContinentDataFrame = pd.DataFrame.from_dict(data=ContinentDict, orient='index').rename(columns={0: 'Continent'})
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    framed = pd.merge(ContinentDataFrame, Top15, how='inner', left_index=True, right_index=True).reset_index().rename(
        columns={'index': 'Country'})

    da = pd.DataFrame()
    da['size'] = framed.groupby('Continent')['Country'].size()
    da['sum'] = framed.groupby('Continent')['PopEst'].sum()
    da['mean'] = framed.groupby('Continent')['PopEst'].apply(lambda x: np.mean(x))
    da['std'] = framed.groupby('Continent')['PopEst'].apply(lambda x: np.std(x))
    ans11 = da

    return ans11


# ### Question 12 (6.6%)
# Cut % Renewable into 5 bins. Group Top15 by the Continent, as well as these new % Renewable bins. How many countries are in each of these groups?
# 
# *This function should return a __Series__ with a MultiIndex of `Continent`, then the bins for `% Renewable`. Do not include groups with no countries.*

def answer_twelve():
    Top15 = answer_one()
    ContinentDict = {'China': 'Asia',
                     'United States': 'North America',
                     'Japan': 'Asia',
                     'United Kingdom': 'Europe',
                     'Russian Federation': 'Europe',
                     'Canada': 'North America',
                     'Germany': 'Europe',
                     'India': 'Asia',
                     'France': 'Europe',
                     'South Korea': 'Asia',
                     'Italy': 'Europe',
                     'Spain': 'Europe',
                     'Iran': 'Asia',
                     'Australia': 'Australia',
                     'Brazil': 'South America'}

    ContinentDataFrame = pd.DataFrame.from_dict(data=ContinentDict, orient='index').rename(columns={0: 'Continent'})
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    framed = (pd.merge(ContinentDataFrame, Top15, how='inner', left_index=True, right_index=True)
              .reset_index().rename(columns={'index': 'Country'}))
    framed['Cut %Ren'] = pd.cut(framed['% Renewable'], 5)
    ans12 = framed.groupby(['Continent', 'Cut %Ren'])['Cut %Ren'].count()

    return ans12


# ### Question 13 (6.6%)
# Convert the Population Estimate series to a string with thousands separator (using commas). Do not round the results.
# 
# e.g. 317615384.61538464 -> 317,615,384.61538464
# 
# *This function should return a Series `PopEst` whose index is the country name and whose values are the population estimate string.*

def answer_thirteen():
    Top15 = answer_one()
    Top15['PopEst'] = (Top15['Energy Supply'] / Top15['Energy Supply per Capita'])
    Top15['PopEst'] = Top15.apply(lambda x: "{:,}".format(x['PopEst']), axis=1)
    ans13 = Top15['PopEst']

    return ans13


if __name__ == '__main__':
    print('Ex1:\n', answer_one(), end='\n\n')
    print('Ex2:\n', answer_two(), end='\n\n')
    print('Ex3:\n', answer_three(), end='\n\n')
    print('Ex4:\n', answer_four(), end='\n\n')
    print('Ex5:\n', answer_five(), end='\n\n')
    print('Ex6:\n', answer_six(), end='\n\n')
    print('Ex7:\n', answer_seven(), end='\n\n')
    print('Ex8:\n', answer_eight(), end='\n\n')
    print('Ex9:\n', answer_nine(), end='\n\n')
    print('Ex10:\n', answer_ten(), end='\n\n')
    print('Ex11:\n', answer_eleven(), end='\n\n')
    print('Ex12:\n', answer_twelve(), end='\n\n')
    print('Ex13:\n', answer_thirteen(), end='\n\n')
