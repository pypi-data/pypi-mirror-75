import numpy as np
import pandas as pd
import requests
import urllib
import platform
from io import StringIO

from tqdm.auto import tqdm

from ..constants import STRINDEX_SUBCATS

def accept_string_or_list(value):
    """
    1) Checks that value is appropriate type
    2) converts string to one item list; converts all other types to list
    """
    if not isinstance(value, (str, list, pd.core.series.Series, np.ndarray)):
        raise AttributeError('value {} must be type str, list, Series, ndarray'.format(value))
    else:
        return [value] if isinstance(value, str) else list(value)
        
def is_winos():
    return platform.system == 'Windows'

def get_baseframe(test=False, filename=''):
    main_pbar = tqdm(
        total=3 if not filename else 2, 
        desc='Find latest {}set...'.format('test' if test else 'data'), 
        ncols=600, 
        leave=False,
        bar_format='{desc}|{bar}{r_bar}'
    )
    if not filename:
        if test:
            url = 'https://raw.githubusercontent.com/ryanskene/see19/master/latest_testset.txt'
        else:
            url = 'https://raw.githubusercontent.com/ryanskene/see19/master/latest_dataset.txt'

        page = requests.get(url)
        main_pbar.update(1)
        

        df_url = 'https://raw.githubusercontent.com/ryanskene/see19/master/{}set/see19{}-{}.csv'.format('test' if test else 'data', '-TEST' if test else '', page.text)
    else:
        df_url = 'https://raw.githubusercontent.com/ryanskene/see19/master/{}set/{}'.format('test' if test else 'data', filename)
    
    main_pbar.set_description('Fetching table...')
    main_pbar.set_postfix_str('~65,000 rows')
    chunks = []
    for chunk in urllib.request.urlopen(df_url):
        chunks.append(str(chunk,'utf-8'))
        main_pbar.update(1)
    
    main_pbar.set_description('Converting to DataFrame...')
    
    table = StringIO(''.join(chunks))    
    df = pd.read_csv(table)
    df.date = pd.to_datetime(df.date).dt.tz_localize(None)
    for cat in STRINDEX_SUBCATS:
        df[cat] = df[cat].astype('float64')
    main_pbar.update(1)
    main_pbar.set_description('Complete!')
    
    return df
