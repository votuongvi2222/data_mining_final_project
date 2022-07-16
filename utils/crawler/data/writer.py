from operator import mod
import pandas as pd
import os
def to_csv(file_name, data=None, index=False, columns=None, dtype=None, copy=None, \
        sep=',', encoding='utf-8'):
    '''
        Save data to csv file (depends on to_csv() method of pandas)
    '''
    df = pd.DataFrame(data, index, columns, dtype, copy)
    df.to_csv(file_path=os.path.join('D:\XU LY DU LIEU LON\MIDTERM\out', file_name),index=index, sep=sep, na_rep='unknown', header=columns, encoding=encoding)

def to_txt(file_name, data, mode='w', encoding='utf-8'):
    '''
        Save data to txt file
    '''
    with open( os.path.join('D:\XU LY DU LIEU LON\MIDTERM\out', file_name), mode=mode, encoding=encoding, errors='strict', buffering=1) as f:
        f.write(data)
        f.close()