#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日市场数据获取脚本
自动抓取A股大盘数据、资金流向、热点板块
生成每日复盘报告

使用方法:
    python daily_report.py
"""

import requests
import json
import datetime
import os
import re

# 配置
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "strategy")
TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "templates", "daily-market-template.md")

# 东方财富API接口
EASTMONEY_API = {
    "index": "https://push2.eastmoney.com/api/qt/ulist.np/get",
    "funds": "https://push2.eastmoney.com/api/qt/ulist.np/get",
    "sector": "https://push2.eastmoney.com/api/qt/clist/get"
}

def get_date_str():
    """获取日期字符串"""
    return datetime.datetime.now().strftime("%Y-%m-%d")

def get_index_data():
    """获取大盘指数数据"""
    try:
        # 上证指数、深证成指、创业板指、沪深300、科创50
        codes = "1.000001,0.399001,0.399006,1.000300,1.000688"
        url = f"https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&invt=2&fields=f2,f3,f4,f5,f12,f14&secids={codes}"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        index_map = {
            "000001": "上证指数",
            "399001": "深证成指", 
            "399006": "创业板指",
            "000300": "沪深300",
            "000688": "科创50"
        }
        
        result = []
        if data.get("data") and data["data"].get("diff"):
            for item in data["data"]["diff"]:
                code = item.get("f12", "")
                name = index_map.get(code, code)
                result.append({
                    "name": name,
                    "close": item.get("f2", "--"),
                    "change": item.get("f4", "--"),
                    "pct": item.get("f3", "--"),
                    "volume": item.get("f5", "--")
                })
        return result
    except Exception as e:
        print(f"获取指数数据失败: {e}")
        return []

def get_sector_data():
    """获取板块涨幅数据"""
    try:
        url = "https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=20&po=1&np=1&fltt=2&invt=2&fid=f3&fs=m:90+t:2+f:!50&fields=f2,f3,f4,f12,f14,f20,f21"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        result = []
        if data.get("data") and data["data"].get("diff"):
            for item in data["data"]["diff"][:10]:
                result.append({
                    "name": item.get("f14", ""),
                    "change": item.get("f3", "--"),
                    "lead": "",  # 领涨股需要额外获取
                    "catalyst": ""
                })
        return result
    except Exception as e:
        print(f"获取板块数据失败: {e}")
        return []

def generate_report():
    """生成每日复盘报告"""
    date_str = get_date_str()
    
    # 读取模板
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # 替换日期
    report = template.replace("{{日期}}", date_str)
    report = report.replace("{{YYYY-MM-DD HH:MM}}", datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    
    # 获取数据
    index_data = get_index_data()
    sector_data = get_sector_data()
    
    # 填充指数数据
    for item in index_data:
        # 在表格中查找对应行并填充
        pattern = f"| {item['name']} | | | | |"
        replacement = f"| {item['name']} | {item['close']} | {item['change']} | {item['pct']}% | {item['volume']} |"
        report = report.replace(pattern, replacement)
    
    # 填充板块数据
    for i, item in enumerate(sector_data[:3], 1):
        pattern = f"| {i} | | | | |"
        replacement = f"| {i} | {item['name']} | {item['change']}% | {item['lead']} | {item['catalyst']} |"
        report = report.replace(pattern, replacement, 1)
    
    # 保存报告
    filename = f"daily-report-{date_str}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"报告已生成: {filepath}")
    return filepath

if __name__ == "__main__":
    print(f"开始生成 {get_date_str()} 的每日复盘报告...")
    generate_report()
