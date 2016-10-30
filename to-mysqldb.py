#!/usr/bin/env python3
from datetime import datetime
import json
import sys
import os
import pymysql
from ipaddress import IPv4Network, IPv4Address
def domain_name(s):
    split_dom = s[:-1].split('.')
    if (len(split_dom) == 1):
        return s[:-1]
    if (len(split_dom[-1]) == 2 and len(split_dom[-2]) <= 3): ## applies to CCtlds: ac.id, com.tw, org.au, co.id, or.il
        return '.'.join(split_dom[-3:])
    else:
        return '.'.join(split_dom[-2:])

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("usage: {} <log-file.csv>".format(sys.argv[0]))
        exit(1)

    requests = []
    with open(sys.argv[1], 'r') as logfile:
        for logline in logfile:
            logparts = logline.split()
            ipaddr = IPv4Address(logparts[3])
            if logparts[2] == 'info:' and (ipaddr in IPv4Network('10.0.0.0/8') or ipaddr in IPv4Network('172.16.0.0/12') or ipaddr in IPv4Network('192.168.0.0/16')) and logparts[5] == 'A':
                unixts = logparts[0].replace('[','')
                unixts = unixts.replace(']','')
                requests.append((unixts, logparts[3], logparts[4][:-1]))
    for i in requests[:20]:
        print(i)
