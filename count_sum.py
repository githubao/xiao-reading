#!/usr/bin/env python
# encoding: utf-8

"""
@description: 统计个数

@author: baoqiang
@time: 2019/3/17 下午12:57
"""

from collections import defaultdict
import os


def count_sum():
    dic = defaultdict(int)

    title = ''
    subtitle = ''

    with open('README.md', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()

            if line.startswith('## '):
                title = line.strip('## ')
                continue

            if line.startswith('### '):
                subtitle = line.strip('### ')
                continue

            if line.startswith('1. '):
                if not title or not subtitle:
                    print('err line: {}'.format(line))
                    continue

                key = '{}-{}'.format(title, subtitle)

                dic[key] += 1

    count = sum(dic.values())
    print_sep()
    print('total movies: {}'.format(count))
    print_sep()

    # 统计大类
    big_dic = defaultdict(int)
    for k, v in dic.items():
        key = k.split('-')[0]
        big_dic[key] += v

    for k, v in big_dic.items():
        print('{} -> {}'.format(k, v))

    # 每个小的分类按照时间排序
    print_sep()
    # sorted_dic = sorted(dic.items(), key=lambda x: x[1], reverse=True)
    sorted_dic = sorted(dic.items(), key=lambda x: x[0], reverse=False)
    for k, v in sorted_dic:
        print('{} -> {}'.format(k, v))

    print_sep()


def find_diff():
    """
    豆瓣看过与readme的不同
    :return:
    """
    home = os.environ['HOME']
    filenanme = '{}/Downloads/books.txt'.format(home)

    doubans = set()
    reads = set()

    with open(filenanme, 'r', encoding='utf-8') as f:
        name = ''

        for line in f:
            attrs = line.strip().split(' ')

            result = ' '.join(attrs[:len(attrs) - 1])

            name = result.strip().split('(')[0].split('（')[0]
            name = name.replace('中文版', '').replace('全集', '')

            if name and name not in doubans:
                doubans.add(name)
            else:
                print('dup: {}'.format(name))

    with open('README.md', 'r', encoding='utf-8') as f:
        start = False

        for line in f:
            # if '已读' in line:
            #     start = True
            # if '视频' in line:
            #     start = False

            if '读书计划' in line:
                start = True
            if '编程语言' in line:
                start = False

            if start:
                if line.startswith('1. '):
                    attrs = line.strip().replace('1. [', '').split(']')

                    if len(attrs) != 2:
                        print('err line: {}'.format(line.strip()))
                        continue

                    name = attrs[0]

                    if name not in reads:
                        reads.add(name)
                    else:
                        print('dup2: {}'.format(name))

    print('douban({}), read({})\ndiff1:\n{} \ndiff2:\n{}'.
          format(len(doubans), len(reads), '\n'.join(doubans - reads), '\n'.join(reads - doubans)))


def print_sep():
    print('#' * 20)


if __name__ == '__main__':
    count_sum()
    # find_diff()
