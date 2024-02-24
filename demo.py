# coding = utf-8
# -*- coding:utf-8 -*-
import os
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from currency_dic import Dic

# chrome driver path
CHROME_PATH = 'D:\\python_project\\exchange_rate\\chromedriver'
os.environ['PATH'] += os.environ['PATH'] + ';' + CHROME_PATH
# print(os.environ['PATH'])

if __name__ == '__main__':
    # 解析命令行参数
    assert len(sys.argv) == 3, '参数不足'
    date = sys.argv[1]
    assert len(date) == 8, '日期格式错误'
    date = date[:4] + '-' + date[4:6] + '-' + date[6:8]
    currency_type = sys.argv[2]
    currency_type = Dic.get(currency_type)
    assert currency_type is not None, '货币代号错误'

    # 构建driver
    driver = webdriver.Chrome()
    driver.get('https://www.boc.cn/sourcedb/whpj/')
    # print(driver.title)

    # 设置开始时间
    input_start = driver.find_element(
        By.CSS_SELECTOR,
        '#historysearchform > div > table > tbody > tr > td:nth-child(2) > div > input'
    )
    input_start.clear()
    input_start.send_keys(date)

    # 设置结束时间
    input_end = driver.find_element(
        By.CSS_SELECTOR,
        '#historysearchform > div > table > tbody > tr > td:nth-child(4) > div > input'
    )
    input_end.clear()
    input_end.send_keys(date)

    # 设置牌价
    select = Select(driver.find_element(
        By.CSS_SELECTOR,
        '#pjname'
    ))
    select.select_by_value(currency_type)

    # 点击查询
    input_select = driver.find_element(
        By.CSS_SELECTOR,
        '#historysearchform > div > table > tbody > tr > td:nth-child(7) > input'
    )
    input_select.click()

    # 获取总页数
    page = driver.find_element(
        By.CSS_SELECTOR,
        '#list_navigator > ol > li:nth-child(1)'
    )
    page_count = int(page.text[1: -1])
    # print(page.text)

    # 保存查询内容
    with open('./result.txt', 'w', encoding='utf-8') as f:
        for i in range(page_count):
            table = driver.find_element(
                By.CSS_SELECTOR,
                'body > div > div.BOC_main.publish > table > tbody'
            )

            # 获取表格内容
            text = table.get_attribute('innerText').strip()
            start_idx = text.find('\n') + 1
            if i == 0:
                # 打印其中一个结果
                if text == '':
                    print('无结果')
                else:
                    end_idx = text.find('\n', start_idx)
                    ret = text[start_idx: end_idx].split('\t')[3]
                    print('无结果' if ret == '' else ret)
            else:
                text = text[start_idx:].strip()
            if text != '':
                f.write(text)
                f.write('\n')

            # 翻页
            if i < page_count - 1:
                page_next = driver.find_element(
                    By.CSS_SELECTOR,
                    '#list_navigator > ol > li.turn_next'
                )
                page_next.click()

    driver.close()
