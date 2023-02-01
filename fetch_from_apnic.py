#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import urllib.request, urllib.parse, urllib.error
import os
import math

apnic_file_url = 'http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest'
file_save_name = 'data_apnic-latest.txt'
all_file_name = 'data_all.txt'
country_to_extract = 'all'

def show_progress(a, b, c):
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    print('Progress: %.2f%%' % per)


if __name__ == '__main__':
    urllib.request.urlretrieve(url=apnic_file_url, filename=file_save_name, reporthook=show_progress)
    record_dict_list = []
    with open(file_save_name) as saved_file:
        valid_record_num = 0
        for line in saved_file.readlines():
            line_pattern = 'apnic\|(?P<country>\w{2})\|(?P<ip_version>ipv[4,6])\|(?P<net_address>[\d.:]+)\|(?P<net_size>\d+)\|\d+\|(assigned|allocated)'
            match_group = re.match(line_pattern, line)
            if match_group:
                valid_record_num += 1
                record_dict_list.append(match_group.groupdict())
    print('Total records count: %d' % valid_record_num)

    countries = set()
    for record in record_dict_list:
        countries.add(record['country'])
    print("=====>>>>>> ALL Contry Codes:")
    print("%s " % sorted(countries))

    # ipv6,CN,192.168.1.1/32
    with open(all_file_name, 'w') as output_csv:
        for record in record_dict_list:
            output_csv.write(record['ip_version'] + ',')
            output_csv.write(record['country'] + ',')
            output_csv.write(record['net_address'] + '/' + str( 32 - int(math.log(int(record['net_size']), 2))) + '\n')

