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
    '''
    Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. 
    '''
    with open('university_towns.txt') as f:
        b = f.read()
    z =b
    z = z.split('[edit]')
    ggg = dict()
    ddd = list()
    for i in range(len(z)):
        if i < len(z) -1:
            ggg[z[i].split('\n')[-1]] =  z[i+1].split('\n')[1:-1]  

    for i, r in ggg.items():
        for j in r:
            ddd.append([i.strip(), j.strip()])
    df = pd.DataFrame(ddd, columns=["State", "RegionName"])
    df['RegionName']= df.RegionName.str.replace(r'\[\d+\]','')
    df['RegionName'] = df.RegionName.str.replace(r'\.$','')
    df['RegionName'] = df.RegionName.str.replace(r'\s*\(\s*.+\)*','')
    df['RegionName'] = df.RegionName.str.replace(r'\n','')
    df['State'] = df.State.str.replace(r'(\n)','')
    df['State'] = df.State.astype('category')
    return df



def get_recession_start():
    '''
    Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3
    '''
    df = pd.read_excel('gdplev.xls', header = 5)
    df = df[['Unnamed: 4' , 'GDP in billions of chained 2009 dollars.1' ]].tail(66) 
    df.columns = ['quarter', 'GDP in billions of chained 2009 dollars']
    df = df.reset_index()
    df = df[['quarter', 'GDP in billions of chained 2009 dollars']]
    for i in df.index:
        try:
            if df.loc[i,'GDP in billions of chained 2009 dollars'] > df.loc[i+1,'GDP in billions of chained 2009 dollars'] and df.loc[i+1,'GDP in billions of chained 2009 dollars'] > df.loc[i+2,'GDP in billions of chained 2009 dollars']:
                x = (df.loc[i+1,'quarter'])
                break
        except:
            pass
    return x


def get_recession_end():
    '''
    Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3
    '''
    df = pd.read_excel('gdplev.xls', header = 5)
    df = df[['Unnamed: 4' , 'GDP in billions of chained 2009 dollars.1' ]].tail(66)
    df.columns = ['quarter', 'GDP in billions of chained 2009 dollars']
    df = df[33:]
    df = df.reset_index()
    df = df[['quarter', 'GDP in billions of chained 2009 dollars']]
    for i in df.index:
        try:
            if df.loc[i,'GDP in billions of chained 2009 dollars'] < df.loc[i+1,'GDP in billions of chained 2009 dollars'] and df.loc[i+1,'GDP in billions of chained 2009 dollars'] < df.loc[i+2,'GDP in billions of chained 2009 dollars']:
                x = (df.loc[i+2,'quarter'])
                break
        except:
            pass
    return x



def get_recession_bottom():
    '''
    Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3
    '''
    df = pd.read_excel('gdplev.xls', header = 5)
    df = df.tail(66)[['Unnamed: 4' , 'GDP in billions of chained 2009 dollars.1' ]] 
    df.columns = ['quarter', 'GDP in billions of chained 2009 dollars']
    df = df.set_index('quarter')
    df = df[get_recession_start():get_recession_end()]
    x = df['GDP in billions of chained 2009 dollars'].idxmin()
    return x



def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    df  =pd.read_csv('City_Zhvi_AllHomes.csv')
    df['State'] = df.State.replace(states)
    df =df[['RegionID','RegionName','State','Metro','CountyName','SizeRank',
 '2000-01','2000-02','2000-03','2000-04', '2000-05','2000-06','2000-07','2000-08','2000-09',
 '2000-10','2000-11','2000-12','2001-01','2001-02', '2001-03', '2001-04', '2001-05', '2001-06',
 '2001-07', '2001-08', '2001-09','2001-10', '2001-11', '2001-12', '2002-01', '2002-02',
 '2002-03', '2002-04', '2002-05', '2002-06', '2002-07', '2002-08', '2002-09', '2002-10',
 '2002-11', '2002-12', '2003-01', '2003-02', '2003-03', '2003-04', '2003-05', '2003-06', '2003-07', '2003-08', '2003-09',
 '2003-10', '2003-11', '2003-12', '2004-01', '2004-02', '2004-03', '2004-04', '2004-05',
 '2004-06', '2004-07', '2004-08', '2004-09', '2004-10', '2004-11', '2004-12', '2005-01',
 '2005-02', '2005-03', '2005-04', '2005-05', '2005-06', '2005-07', '2005-08', '2005-09', '2005-10',
 '2005-11', '2005-12', '2006-01', '2006-02', '2006-03', '2006-04', '2006-05', '2006-06',
 '2006-07', '2006-08', '2006-09', '2006-10', '2006-11', '2006-12', '2007-01', '2007-02',
 '2007-03', '2007-04', '2007-05', '2007-06', '2007-07', '2007-08', '2007-09', '2007-10',
 '2007-11', '2007-12', '2008-01', '2008-02', '2008-03', '2008-04', '2008-05', '2008-06',
 '2008-07', '2008-08', '2008-09', '2008-10', '2008-11', '2008-12', '2009-01', '2009-02',
 '2009-03', '2009-04', '2009-05', '2009-06', '2009-07', '2009-08', '2009-09', '2009-10', '2009-11', '2009-12', '2010-01', '2010-02',
 '2010-03', '2010-04', '2010-05', '2010-06', '2010-07', '2010-08', '2010-09', '2010-10', '2010-11', '2010-12', '2011-01',
 '2011-02', '2011-03', '2011-04', '2011-05', '2011-06', '2011-07', '2011-08', '2011-09',
 '2011-10', '2011-11', '2011-12', '2012-01', '2012-02', '2012-03', '2012-04', '2012-05',
 '2012-06', '2012-07', '2012-08', '2012-09', '2012-10', '2012-11', '2012-12', '2013-01',
 '2013-02', '2013-03', '2013-04', '2013-05', '2013-06', '2013-07', '2013-08', '2013-09',
 '2013-10', '2013-11', '2013-12', '2014-01', '2014-02', '2014-03', '2014-04', '2014-05',
 '2014-06', '2014-07', '2014-08', '2014-09', '2014-10', '2014-11', '2014-12', '2015-01',
 '2015-02', '2015-03', '2015-04', '2015-05', '2015-06', '2015-07', '2015-08', '2015-09',
 '2015-10', '2015-11', '2015-12', '2016-01', '2016-02','2016-03','2016-04','2016-05','2016-06','2016-07','2016-08']]
    daf = df.iloc[:,6:].T.reset_index()
    def gc(x):
        q = x.quarter 
        uu = x.year
        return str(uu)+'q'+str(q)
    daf = daf.rename(columns={'index':'das'})
    daf['das'] = pd.to_datetime(daf['das'])
    daf['das'] = daf.das.apply(gc)
    daf = daf.groupby('das').mean().T
    df = df[['State', 'RegionName']]
    df = df.merge(daf, how= 'inner', right_index=True ,left_index=True)
    df = df.set_index(['State', 'RegionName'])
    return df 


def run_ttest():
    '''
    First creates new data showing the decline or growth of housing prices
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
    reduced market loss).
    '''
    df = convert_housing_data_to_quarters()
    df_uni = get_list_of_university_towns()
    beg = get_recession_start() 
    bloc = df.columns.get_loc(beg)
    rbm = get_recession_bottom()
    rbmloc = df.columns.get_loc(rbm)
    df_rec = df.iloc[:,bloc:rbmloc+1]
    df_rec['grdc'] = (df_rec[beg] - df_rec[rbm]) / df_rec[beg] 
    df_rec = df_rec[~df_rec.grdc.isnull()]
    df_rec = df_rec.reset_index()
    df_rec['pp'] = "(" + df_rec['State'] + df_rec['RegionName'] + ')'
    df_rec = df_rec[~df_rec.pp.duplicated()]
    df_rec_uni = pd.merge(df_rec,df_uni, how = 'inner',left_on =['State','RegionName'], right_on =['State','RegionName'])
    ss = list(df_rec_uni.State)
    ci = list(df_rec_uni.RegionName)
    df_rec_non_uni = df_rec[~((df_rec['State'].isin(ss)) & (df_rec['RegionName'].isin(ci)))] 
    p = .01
    test = ttest_ind(df_rec_uni.grdc,df_rec_non_uni.grdc)
    if df_rec_uni.grdc.mean() < df_rec_non_uni.grdc.mean():
        if test[1] < p:
            return (True,test[1],'university town')
        else:
            return (False,test[1],'university town')
    else:
        if test[1] < p:
            return (True,test[1],'non-university town')
        else:
            return (False,test[1],'non-university town')


if __name__ == '__main__':
    print('==== list of university towns ====')
    print(get_list_of_university_towns())
    print('==== recession start ====')
    print(get_recession_start())
    print('==== recession end ====')
    print(get_recession_end())
    print('==== recession bottom ====')
    print(get_recession_bottom())
    print('==== convert housing data to quarters ====')
    print(convert_housing_data_to_quarters())
    print('==== t-test ====')
    print(run_ttest())