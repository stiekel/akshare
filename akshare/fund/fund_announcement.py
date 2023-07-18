#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2023/7/18 22:40
Desc: 东方财富网站-天天基金网-基金档案-基金公告
http://fundf10.eastmoney.com/jjgg_000001.html
"""
import json
import time

import pandas as pd
import requests

from akshare.utils import demjson

def fund_announcement_personnel(symbol: str = "000791") -> pd.DataFrame:
    """
    东方财富网站-天天基金网-基金档案-基金公告-人事调整
    http://fundf10.eastmoney.com/jjgg_000001_4.html
    :param symbol: 基金代码，可以通过调用 ak.fund_name_em() 接口获取
    :type symbol: str
    :return: 东方财富网站-天天基金网-基金档案-基金公告-人事调整-公告列表
    :rtype: pandas.DataFrame
    """
    url = "http://api.fund.eastmoney.com/f10/JJGG"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Referer": f"http://fundf10.eastmoney.com/jjgg_{symbol}_4.html",
    }
    params = {
        "callback": "jQuery18306317433208358414_1689690726250",
        "fundcode": symbol,
        "pageIndex": "1",
        "pageSize": "1000",
        "type": "4",
        "_": round(time.time() * 1000),
    }
    r = requests.get(url, params=params, headers=headers)
    text_data = r.text
    data_json = demjson.decode(text_data[text_data.find("{") : -1])
    temp_df = pd.DataFrame(data_json["Data"])
    temp_df.columns = [
        "基金代码",
        "公告标题",
        "基金名称",
        "_",
        "_",
        "公告日期",
        "_",
        "报告ID",
    ]
    temp_df = temp_df[["基金代码", "公告标题", "基金名称", "公告日期", "报告ID"]]
    temp_df.sort_values(['公告日期'], inplace=True, ignore_index=True)
    temp_df['公告日期'] = pd.to_datetime(temp_df['公告日期']).dt.date
    return temp_df


if __name__ == "__main__":
    fund_announcement_personnel_df = fund_announcement_personnel(symbol="000001")
    print(fund_announcement_personnel_df)
