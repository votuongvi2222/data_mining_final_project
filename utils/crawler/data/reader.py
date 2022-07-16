import pandas as pd
import os
def read_csv(file_path, sep=',', header=None, encoding='utf-8'):
    '''
        Read csv file then print to the console (depends on read_csv() of pandas)
    '''
    df = pd.read_csv(filepath=file_path, sep=sep, header=header, encoding=encoding)
    print(df.to_string())

def read_txt(save_path, file_name, encoding='utf8'):
    '''
        Read text file then print to the console
    '''
    with open(os.path.join('D:\XU LY DU LIEU LON\MIDTERM\out', file_name), encoding=encoding,mode= 'r') as f:
        print(f.read())
        f.close()