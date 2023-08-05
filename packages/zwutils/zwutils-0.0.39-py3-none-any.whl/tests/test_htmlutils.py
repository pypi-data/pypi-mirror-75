# -*- coding: utf-8 -*-
import pytest
from bs4 import BeautifulSoup
from zwutils import htmlutils

def test_find_soup_parent():
    htmlstr = '''
    <table class="myclass otherclass">
    <thead></thead>
    <tbody>
        <tr><td id="a"></td></tr>
        <tr></tr>
    </tbody>
    </table>
    '''
    el = BeautifulSoup(htmlstr, features='lxml')
    el = el.find(id='a')
    r = htmlutils.find_soup_parent(el, tagnm='table')
    assert r and r.name == 'table'

    r = htmlutils.find_soup_parent(el, attrs={'class': 'myclass'})
    assert r and r.name == 'table'

    r = htmlutils.find_soup_parent(el, tagnm='table', attrs={'class': 'myclass'})
    assert r and r.name == 'table'

def test_find_soup_next_sibling():
    htmlstr = '''
    <table>
    <thead></thead>
    <tbody>
        <tr><td id="a">label</td><td>text1</td><td class="myclass otherclass">text2</td></tr>
        <tr></tr>
    </tbody>
    </table>
    '''
    el = BeautifulSoup(htmlstr, features='lxml')
    el = el.find(id='a')
    r = htmlutils.find_soup_next_sibling(el, tagnm='td')
    assert r and r.text == 'text1'

    r = htmlutils.find_soup_next_sibling(el, attrs={'class': 'myclass'})
    assert r and r.text == 'text2'

    r = htmlutils.find_soup_next_sibling(el, tagnm='td', attrs={'class': 'myclass'})
    assert r and r.text == 'text2'

def test_soup_depth_count():
    htmlstr = '''
    <table>
    <thead></thead>
    <tbody>
        <tr id="tr"><td id="td">label</td></tr>
        <tr></tr>
    </tbody>
    </table>
    '''
    soup = BeautifulSoup(htmlstr, features='lxml')
    el = soup.find(id='td')
    r = htmlutils.soup_depth_count(el)
    assert r == 3

    soup = BeautifulSoup(htmlstr, features='lxml')
    el = soup.find(id='tr')
    r = htmlutils.soup_depth_count(el, 'html')
    assert r == 3

def test_soup_calc_child():
    htmlstr = '''
    <table>
    <thead></thead>
    <tbody>
        <tr id="tr"><td id="td">label</td><td></td></tr>
        <tr></tr>
    </tbody>
    </table>
    '''
    soup = BeautifulSoup(htmlstr, features='lxml')
    r = htmlutils.soup_calc_child(soup, 'td')
    assert r[2]['child_count'] == 2 and r[2]['depth_count'] == 2


