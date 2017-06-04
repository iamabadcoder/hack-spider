# -*- coding:utf-8 -*-

import sys
import time
import random
import linecache
import ConfigParser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

reload(sys)
sys.setdefaultencoding('utf8')


def login(driver, home_page_url):
    try:
        driver.get(home_page_url)
        id_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "id")))
        passwd_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "pwd")))
        submit_element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "b_login")))
    except TimeoutException:
        print 'TimeoutException occur when WebDriverWait in login'
        return False
    time.sleep(5)
    id_element.send_keys(conf.get("shuimu", "name"))
    time.sleep(1)
    passwd_element.send_keys(conf.get("shuimu", "pwd"))
    time.sleep(1)
    submit_element.click()
    time.sleep(5)
    return True

def top_post(driver):
    post_url_count = len(open(file_shuimu_urls, "rU").readlines())
    post_url = linecache.getline(file_shuimu_urls, random.randint(1, post_url_count))
    driver.get(post_url)
    try:
        post_content_element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "post_content")))
        post_content_element.click()
        time.sleep(2)
        post_content_element.clear()
        post_content_element.send_keys('up me, up me')
    except TimeoutException:
        print 'TimeoutException occur when post_content'

    try:
        publish_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#post_form > div > input:nth-child(1)")))
        publish_element.click()
        time.sleep(3)
    except TimeoutException:
        print 'TimeoutException occur when top_post child'


def check_post_position(driver):
    target_post_cnt = 0
    top_three_cnt = 0
    post_list_page_url = 'http://www.newsmth.net/nForum/#!board/Career_Upgrade'
    driver.get(post_list_page_url)
    try:
        post_table_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "board-list")))
        tr_elements = post_table_element.find_elements_by_tag_name('tr')
        print len(tr_elements)
        if tr_elements is None or len(tr_elements) < 2:
            print 'tr_elements is None!!!'
        for tr_ele in tr_elements[0:15]:
            if 'lxzcyh' in tr_ele.text:
                target_post_cnt += 1
        for tr_ele in tr_elements[0:7]:
            if 'lxzcyh' in tr_ele.text:
                top_three_cnt += 1
    except TimeoutException:
        print 'TimeoutException occur when wait post_table_element'
    if target_post_cnt > 4 and top_three_cnt > 0:
        return False
    else:
        return True


if __name__ == '__main__':
    conf = ConfigParser.ConfigParser()
    conf.read('/Users/iamabadcoder/PycharmProjects/hack-spider/resources/account.conf')
    file_shuimu_urls = '/Users/iamabadcoder/PycharmProjects/hack-spider/resources/shuimu_urls.txt'

    chrome_driver = webdriver.Chrome('/Users/iamabadcoder/PycharmProjects/hack-spider/resources/chromedriver')
    chrome_driver.maximize_window()
    if not login(chrome_driver, 'http://www.newsmth.net/nForum/index'):
        print 'Login Error!!!'
    else:
        while True:
            if check_post_position(chrome_driver):
                top_post(chrome_driver)
            time.sleep(60)
