# -*-coding: GBK -*-
import ast

import pandas as pd
import requests
from tqdm import tqdm

from ricco.coord_trans import BD2WGS
from ricco.util import reset2name


def get_lnglat(addr: str,
               addr_type: str,
               city: str):
    '''
    ���ݵ�ַ��ȡ��γ��

    :param addr: ��ַ
    :param addr_type: ��ַ������addr;��ַ �� name����Ŀ����
    :param city: ����
    :return:
    '''

    def get_address_bd(keywords, city):
        key = 'csxAwMRuLWFnOm2gK6vrR30uyx7CSAjW'
        basic_ads = 'http://api.map.baidu.com/geocoding/v3/?city={}&address={}&output=json&ak={}'
        address = basic_ads.format(city, keywords, key)
        return address

    def get_proj_bd(keywords, city):
        key = 'csxAwMRuLWFnOm2gK6vrR30uyx7CSAjW'
        basic_ads = 'http://api.map.baidu.com/place/v2/search?query={}&region={}&city_limit=true&output=json&ak={}'
        address = basic_ads.format(keywords, city, key)
        return address

    keywords = city + '' + addr
    if addr_type == 'addr':
        address1 = get_address_bd(keywords, city)
        res1 = requests.get(address1)
        j1 = ast.literal_eval(res1.text)
        name = None
        if len(j1['result']) > 0:
            lng = j1['result']['location']['lng']
            lat = j1['result']['location']['lat']
        else:
            lng, lat = None, None
    elif addr_type == 'name':
        address1 = get_proj_bd(keywords, city)
        res1 = requests.get(address1)
        j1 = ast.literal_eval(res1.text)
        if len(j1['results']) > 0:
            name = j1['results'][0]['name']
            lng = j1['results'][0]['location']['lng']
            lat = j1['results'][0]['location']['lat']
        else:
            name, lng, lat = None, None, None
    else:
        raise ValueError("addr_typeӦΪ'addr'����ַ �� 'name'����Ŀ����")
    return [lng, lat, name]


def geocode_df(df,
               addr_col,
               addr_type: str,
               city: str = ''):
    '''
    ���ݵ�ַ�л���Ŀ�����н�����γ��

    :param df: �����Dataframe
    :param addr_col: ��ַ�У������Ƕ��������ɵ��б������
    :param addr_type: ��ַ������addr;��ַ �� name����Ŀ����
    :param city: ����
    :return:
    '''
    if isinstance(addr_col, list):
        addr_m = 'merge_address'
        df[addr_m] = ''
        for add in addr_col:
            df[addr_m] = df[addr_m].astype(str).str.cat(df[add].astype(str))
    else:
        addr_m = addr_col

    prjct = df[addr_m].drop_duplicates()  # �����ظ�����
    empty = pd.DataFrame(columns=[addr_m, 'lng', 'lat', '������Ŀ��'])
    for i in tqdm(prjct):
        lnglat = get_lnglat(i, addr_type, city)
        add_df = pd.DataFrame({addr_m: [i],
                               'lng': [lnglat[0]],
                               'lat': [lnglat[1]],
                               '������Ŀ��': [lnglat[2]]})
        empty = empty.append(add_df)
    df = df.merge(empty, how='left', on=addr_m)
    if isinstance(addr_col, list):
        df.drop(addr_m, axis=1, inplace=True)
    df = BD2WGS(df)
    if 'name' not in df.columns:
        df = reset2name(df)
    return df
