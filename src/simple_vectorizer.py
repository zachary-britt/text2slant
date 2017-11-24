
import spacy
import pandas as pd
import numpy as np
from multiprocessing import Pool


def calc_append_tensors(args):
    i, df = args
    print('Started process: {}'.format(i))
    nlp = spacy.load('en')
    df['tensor'] = df.content.apply( lambda text: nlp(text).tensor )
    print('Completed process: {}'.format(i))
    return df


def parallelize_tensor_calcs_and_save(df, out_loc):
    from simple_vectorizer import calc_append_tensors

    n_workers = 4

    # Multi processing setup for tensor calcs
    n2 = df_part.shape[0]
    Ns2 = np.linspace(0,n2,n_workers+1).astype(np.int)
    df_sub_parts = [ df_part.iloc[Ns2[j]:Ns2[j+1]] for j in range(n_workers) ]

    jobs = enumerate(df_sub_parts)
    func = calc_append_tensors

    pool = Pool(n_workers)
    df_sub_parts = pool.map(func, jobs)
    pool.close()
    pool.join()

    df_part = pd.concat(df_sub_parts)
    df_part.to_pickle(out_loc)
    print('saved df_partition: {}'.format(i))


if __name__ == '__main__':
    in_path = '/home/zachary/dsi/capstone/data/formatted_arts.pkl'
    out_dir = '/home/zachary/dsi/capstone/data/df_w_tensors/'

    df = pd.read_pickle(in_path)

    df_part_count = 20

    # split df into df_part_count partitions for seperate saving
    # (reduces RAM burden)
    n = df.shape[0]
    Ns = np.linspace(0,n,df_part_count+1).astype(np.int)
    df_parts = [ df.iloc[Ns[i]:Ns[i+1]] for i in range(df_part_count) ]

    # Enumerate over parts and save
    for i, df_part in enumerate(df_parts):
        print('started batch: {}'.format(i))
        out_loc = out_dir + 'df_{}.pkl'.format(i)
        parallelize_tensor_calcs_and_save( df_part, out_loc )