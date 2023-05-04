# Validated function for calculating PMI for accounts based on twitter followers and a class
import numpy as np
import pandas as pd

def calc_pmi(df_pmi):
    df_pmi = df_pmi[['twitter_id','account','class']]
    df_pmi['freq_account'] = df_pmi.groupby('account')['account'].transform('count')
    df_pmi['freq_account_class'] = df_pmi.groupby(['account', 'class'])['account'].transform('count')
    total_users_count = df_pmi['twitter_id'].nunique()
    df_pmi['total_users_count'] = total_users_count

    class_count = df_pmi.drop_duplicates(subset='twitter_id').groupby('class').count()['twitter_id']
    def get_total_class(x):
        return class_count[x]
    
    df_pmi['this_class_count'] = df_pmi['class'].progress_apply(get_total_class)
    df_pmi['pr_account_class'] = df_pmi['freq_account_class'] / df_pmi['this_class_count']
    df_pmi['pr_account'] = df_pmi['freq_account'] / df_pmi['total_users_count']
    df_pmi['pr_class'] = df_pmi['this_class_count'] / df_pmi['total_users_count']
    df_pmi['pmi'] = np.log2(   ( df_pmi['pr_account_class']*df_pmi['pr_class']) / 
                           ( df_pmi['pr_account'] * df_pmi['pr_class']))

    df_pmi.drop(columns='twitter_id', inplace = True)
    df_pmi.drop_duplicates(subset= ['account', 'class', 'freq_account', 'freq_account_class',
       'total_users_count', 'this_class_count', 'pr_account_class',
       'pr_account', 'pr_class', 'pmi'], inplace=True)
    
    return df_pmi
    
    
    
    
