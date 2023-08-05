import csv
import os

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.wkb import dumps
from shapely.wkb import loads
from tqdm import tqdm


def max_grid():
    '''防止单个单元格文件过大而报错'''
    import sys
    maxInt = sys.maxsize
    decrement = True
    while decrement:
        decrement = False
        try:
            csv.field_size_limit(maxInt)
        except OverflowError:
            maxInt = int(maxInt / 10)
            decrement = True


def rdf(filepath):
    '''
    常用文件读取函数，支持.csv/.xlsx/.shp

    :param filepath: 文件路径
    :return: dataframe
    '''
    max_grid()
    if os.path.splitext(filepath)[1] == '.csv':
        try:
            df = pd.read_csv(filepath, engine='python', encoding='utf-8-sig')
        except:
            df = pd.read_csv(filepath, engine='python')
    elif os.path.splitext(filepath)[1] == '.xls':
        df = pd.read_excel(filepath)
    elif os.path.splitext(filepath)[1] == '.xlsx':
        df = pd.read_excel(filepath)
    elif os.path.splitext(filepath)[1] == '.shp':
        try:
            df = gpd.GeoDataFrame.from_file(filepath, encoding='utf-8-sig')
        except UnicodeEncodeError:
            df = gpd.GeoDataFrame.from_file(filepath, encoding='GBK')
    else:
        raise Exception('未知文件格式')
    return df


def save2csv(df, filename, encoding='GBK'):
    df.to_csv(filename, index=0, encoding=encoding)


def to_csv_by_line(filename, data):
    with open(filename, 'a') as f:
        csv_write = csv.writer(f, dialect='excel')
        csv_write.writerow(data)


def rename2lnglat(df):
    '''将df中的经纬度重命名为lng和lat'''
    col_dict = {'经度': 'lng', '纬度': 'lat', 'lon': 'lng', 'lng_WGS': 'lng', 'lat_WGS': 'lat', 'lon_WGS': 'lng',
                'longitude': 'lng', 'latitude': 'lat', "geom": "geometry"}
    df = df.rename(columns=col_dict)
    return df


def read_and_rename(file):
    '''读取文件并将经纬度统一为lng和lat，并按照经纬度排序'''
    df = rdf(file)
    df = rename2lnglat(df)
    if 'lat' in df.columns:
        df.sort_values(['lat', 'lng'], inplace=True)
        df = df.reset_index(drop=True)
    return df


def reset2name(df, origin: bool = False):
    '''
    重置索引，并重命名为name， 默认将索引重置为有序完整的数字（重置两次）

    :param origin: 为True时，将原来的索引作为name列（重置一次）
    '''
    if not origin:
        df = df.reset_index(drop=True)
    df = df.reset_index().rename(columns={'index': 'name'})
    return df


def pinyin(word: str):
    '''将中文转换为汉语拼音'''
    import pypinyin
    if isinstance(word, str):
        s = ''
        for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
            s += ''.join(i)
    else:
        raise TypeError('输入参数必须为字符串')
    return s


def mkdir_2(path):
    '''新建文件夹，忽略存在的文件夹'''
    if not os.path.isdir(path):
        os.makedirs(path)


def split_csv(filename, n=5):
    '''将文件拆分为多个同名文件，放置在与文件同名文件夹下的不同Part_文件夹中'''
    dir_name = os.path.splitext(os.path.basename(filename))[0]
    abs_path = os.getcwd()
    df = rdf(filename)
    t = len(df)
    p = int(t / n)
    for i in tqdm(range(n)):
        low = i * p
        high = (i + 1) * p
        dir_name2 = 'Part_' + str(i)
        save_path = os.path.join(abs_path, dir_name, dir_name2)
        savefile = os.path.join(save_path, filename)
        mkdir_2(save_path)
        if i == n - 1:
            add = df.iloc[low:, :]
        else:
            add = df.iloc[low: high, :]
        add.to_csv(savefile, index=0, encoding='utf-8')


def valid_check(polygon_geom):
    '''检验面的有效性'''
    df = polygon_geom.copy()
    df['geometry'] = df['geometry'].apply(lambda x: loads(x, hex=True))
    df = gpd.GeoDataFrame(df)
    df.crs = 'epsg:4326'
    df['flag'] = df['geometry'].apply(lambda x: 1 if x.is_valid else -1)
    if len(df[df['flag'] < 0]) == 0:
        print('Validity test passed.')
    else:
        raise Exception('有效性检验失败，请检查并修复面')


def shp2csv(shpfile_name):
    '''shapefile 转 csv 文件'''
    df = rdf(shpfile_name)
    df['geometry'] = df['geometry'].apply(lambda x: dumps(x, hex=True, srid=4326))
    df.crs = 'epsg:4326'
    save_path = os.path.splitext(shpfile_name)[0] + '.csv'
    df.to_csv(save_path, encoding='utf-8-sig', index=0)


def csv2shp(filename):
    '''csv文件 转 shapefile'''
    import fiona
    df = rdf(filename)
    df = df.rename(columns={'名称': 'name',
                            'geom': 'geometry'})
    df = gpd.GeoDataFrame(df)
    df['geometry'] = df['geometry'].apply(lambda x: loads(x, hex=True))
    df.crs = 'epsg:4326'
    save_path = os.path.splitext(filename)[0] + '.shp'
    try:
        df.to_file(save_path, encoding='utf-8')
    except fiona.errors.SchemaError:
        df.columns = [pinyin(i) for i in df.columns]
        df.to_file(save_path, encoding='utf-8')
        print('已将列名转为汉语拼音进行转换')


def to_float(string,
             rex_method: str = '',
             rex_warning: bool = True):
    '''
    字符串转换为float，无法转换的转为空值，可用选正则表达式提取所有数字的最大最小或均值

    :param string:  包含数字的字符串
    :param rex_method: 正则表达式提取一个或多个值后的求值方法，max/min/sum/mean
    :param rex_warning: 当使用正则方法且有百分号时出现的警告
    :return:
    '''
    string = str(string)
    if rex_method != '':
        if rex_warning & ('%' in string):
            import warnings
            message = '''Using 'rex_method' will ignore a value with a percent sign '%', 
                        try 'rex_warning=False' to avoid this warning. '''
            warnings.warn(message)
        string = str(extract_num(string, num_type='float', method=rex_method))
    if '%' in string:
        string = string.replace('%', '')
        string = str(to_float(string) / 100)
    if string != None:
        try:
            f = float(string)
        except ValueError:
            f = np.nan
    else:
        f = np.nan
    return f


def serise_to_float(serise, rex_method='', rex_warning=False):
    '''
    pandas.Series: str --> float

    :param serise: pandas的列
    :param rex_method: 正则表达式提取一个或多个值后的求值方法，max/min/sum/mean
    :param rex_warning: 当使用正则方法且有百分号时出现的警告
    :return:
    '''
    return serise.apply(lambda x: to_float(x, rex_method=rex_method, rex_warning=rex_warning))


def extract_num(string,
                num_type: str = 'str',
                method: str = '',
                join_list: bool = False):
    '''
    提取字符串中的数值，默认返回所有数值组成的列表

    :param method: 可选max/min/mean，返回为数值
    :return: list or float
    '''
    import re
    from warnings import warn
    string = str(string)
    lis = re.findall(r"\d+\.?\d*", string)
    if (num_type == 'float') or (num_type == 'int'):
        lis2 = [float(i) for i in lis]
        if num_type == 'int':
            lis2 = [int(i) for i in lis2]
        if method != '':
            if method == 'max':
                res = max(lis2)
            elif method == 'min':
                res = min(lis2)
            elif method == 'mean':
                res = np.mean(lis2)
            elif method == 'sum':
                res = np.sum(lis2)
            else:
                raise Exception("method方法错误，请选择'max', 'min', 'sum' or 'mean'")
        else:
            res = lis2
        if join_list:
            warn('计算结果无法join')
    elif num_type == 'str':
        res = lis
        if join_list:
            res = ''.join([str(j) for j in res])
    else:
        raise Exception('num_type指定错误，可选项为str, float, int')
    return res


def ensure_list(val):
    """将标量值和Collection类型都统一转换为LIST类型"""
    if val is None:
        return []
    if isinstance(val, list):
        return val
    if isinstance(val, (set, tuple)):
        return list(val)
    return [val]


def segment(x, gap, sep: str = '-', unit: str = ''):
    '''
    区间段划分工具

    :param x: 数值
    :param gap: 间隔
    :param unit: 单位，末尾
    :param sep: 分隔符，中间
    :return: 区间段 'num1分隔符num2单位'：‘80-100米’
    '''

    def between_list(x, lis):
        for i in reversed(range(len(lis) - 1)):
            if x >= lis[i]:
                return lis[i], lis[i + 1]

    if isinstance(gap, list):
        gap = sorted(list(set(gap)))
        if x < gap[0]:
            return '%d%s以下' % (gap[0], unit)
        elif x >= gap[-1]:
            return '%d%s以上' % (gap[-1], unit)
        else:
            l = between_list(x, gap)[0]
            h = between_list(x, gap)[1]
            s = '%d%s%d%s' % (l, sep, h, unit)
    else:
        if x >= 0:
            l = int(x / gap) * gap
            h = l + gap
            s = '%d%s%d%s' % (l, sep, h, unit)
        else:
            l = int(x / gap) * gap
            h = l - gap
            s = '%d%s%d%s' % (h, sep, l, unit)
    return s


def standard(serise, q=0.01, min_score=0, minus=False):
    if minus:
        serise = 1 / (serise + 1)
    max_ = serise.quantile(1 - q)
    min_ = serise.quantile(q)
    serise = serise.apply(lambda x: (x - min_) / (max_ - min_) * (100 - min_score) + min_score)
    serise[serise >= 100] = 100
    serise[serise <= min_score] = min_score
    return serise
