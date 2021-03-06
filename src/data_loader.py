import sys, os
DATA_PATH = os.environ['DATA_PATH']
import zutils
import pandas as pd
import pickle
from datetime import datetime as dt
import dateutil.parser
import ipdb
import numpy as np


def fill_dates(df):
    inds_missing = df[df.date=='None' ].index.values
    for i in inds_missing:
        df['date'].iloc[i] = df['date'].iloc[i-1]
    return df


def load_dfs():

    #open mongo collectoins as pandas dataframes
    fox_df = zutils.open_as_df('fox')   #fox
    hp_df = zutils.open_as_df('hp')     #huffpost
    reu_df = zutils.open_as_df('reuters')
    mj_df = zutils.open_as_df('mj')     #motherjones
    bb_df = zutils.open_as_df('bb')     #Breitbart
    od_df = zutils.open_as_df('od')     #occupydemocrats
    ads_df = zutils.open_as_df('ads')   #political advertisements


    # match up df format
    fox_df['source']='fox'
    ads_df=ads_df[ads_df['supports'].isin(('Hillary Clinton','Donald Trump'))]
    hp_df.drop('author', axis=1, inplace=True)
    mj_df = fill_dates(mj_df)
    hp_df['source'] = 'hp'
    hp_df['date']= hp_df.date.apply( lambda date: dt.strftime(date, '%Y-%m-%d'))
    reu_df['source'] = 'reu'
    reu_df['date']= reu_df.date.apply( lambda date: dt.strftime(date, '%Y-%m-%d'))

    # create bias metric
    od_df['bias'] = 1;     od_df['orient'] = 'left';
    mj_df['bias'] = 1;     mj_df['orient'] = 'left';
    hp_df['bias'] = 0.5;   hp_df['orient'] = 'left'
    reu_df['bias'] = 0;     reu_df['orient']= 'center'
    fox_df['bias'] = 0.5;   fox_df['orient']= 'right'
    bb_df['bias'] = 1;      bb_df['orient'] = 'right'
    ads_df['bias'] = 1
    ads_df['orient'] = np.where( ads_df.supports=='Donald Trump', 'right', 'left' )


    dfs = {'fox':fox_df, 'hp':hp_df, 'reu':reu_df, 'mj':mj_df, 'ads':ads_df,
            'bb':bb_df, 'od':od_df}

    drops = ['author','supports']
    for name in dfs:
        for col in drops:
            try: dfs[name].drop(col, axis=1, inplace=True)
            except: pass
    return dfs

def load_holdout():
    ai_df = zutils.open_as_df('ai')     #addicting info
    gp_df = zutils.open_as_df('gp')     #the gateway pundit
    nyt_df = zutils.open_as_df('nyt')   #new york times

    ai_df['bias'] = 1;      ai_df['orient']= 'left';
    gp_df['bias'] = 1;      gp_df['orient']= 'right';
    nyt_df['bias']=0;       nyt_df['orient']='center';

    import bson

    nyt_df['_id'] = nyt_df['_id'].apply(bson.ObjectId)
    nyt_df['date'] = nyt_df['pub_date'].apply(lambda datestr: str(dateutil.parser.parse(datestr).date()))
    nyt_df['title'] = nyt_df['headline'].apply(lambda x: x['main'])
    nyt_df['link'] = nyt_df['web_url']

    drops = ['headline','pub_date', 'new_desk', 'score', 'type_of_material', 'web_url']
    nyt_df.drop(drops, axis=1, inplace=True)

    dfs = {'ai':ai_df, 'gp':gp_df, 'nyt':nyt_df}
    return dfs

def load_reddit():
    from dateutil import tz

    left_df = zutils.open_as_df('left_reddit')
    right_df = zutils.open_as_df('right_reddit')
    neutral_df = zutils.open_as_df('neutral_reddit')


    left_df['bias'] = 1;   left_df['orient'] = 'left';      left_df['source'] = 'lred';
    right_df['bias']= 1;    right_df['orient'] = 'right';   right_df['source']= 'rred';
    neutral_df['bias']=0;   neutral_df['orient']='center';  neutral_df['source']='cred';

    df = pd.concat([left_df,neutral_df,right_df], ignore_index=True)
    drops = ['author','score','subreddit']
    df.drop(drops, axis=1, inplace=True)
    df.rename(columns={'body':'content','created_utc':'date'}, inplace=True)

    return df


def load_reddit_no_center():
    from dateutil import tz

    left_df = zutils.open_as_df('left_reddit')
    right_df = zutils.open_as_df('right_reddit')

    left_df['bias'] = 1;   left_df['orient'] = 'left'
    right_df['bias']= 1;    right_df['orient'] = 'right'

    df = pd.concat([left_df,right_df], ignore_index=True)
    drops = ['author','score','subreddit']
    df.drop(drops, axis=1, inplace=True)
    df.rename(columns={'body':'content','created_utc':'date'}, inplace=True)
    return df


def ultra_holdout():
    cnn_df = zutils.open_as_df('cnn')
    cnn_df.rename(columns={'contents':'content'}, inplace=True)
    return cnn_df



if __name__ == '__main__':
    dfs = load_dfs()
