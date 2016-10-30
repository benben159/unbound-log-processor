#!/usr/bin/env python3
from datetime import datetime
import json
import sys
import os
from ipaddress import IPv4Address, IPv4Network
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
    #requests_daily = [] ## TODO filtering by date. need a format
    mindate, maxdate = 0, 0
    minmon, maxmon = 0, 0
    minyear, maxyear = 0, 0
    with open(sys.argv[1],'r') as log:
        for logline in log:
            logparts = logline.split()
            ipaddr = IPv4Address(logparts[3])
            ## IP address filtering default is check client IP address if it is in RFC1918 networks
            if logparts[2] == 'info:' and (ipaddr in IPv4Network('10.0.0.0/8') or ipaddr in IPv4Network('172.16.0.0/12') or ipaddr in IPv4Network('192.168.0.0/16')) and logparts[5] == 'A':
                unixts = logparts[0].replace('[','')
                unixts = unixts.replace(']','')
                reqtime = datetime.fromtimestamp(float(unixts))
                if mindate == maxdate == 0:
                    mindate = maxdate = reqtime.day
                elif reqtime.day > maxdate:
                    maxdate = reqtime.day
                if minmon == maxmon == 0:
                    minmon = maxmon = reqtime.month
                elif reqtime.month > maxmon:
                    maxmon = reqtime.month
                if minyear == maxyear == 0:
                    minyear = maxyear = reqtime.year
                elif reqtime.year > maxyear:
                    maxyear = reqtime.year
                requests.append((reqtime,logparts[3], logparts))

    print("requests are dated from {}/{}/{} to {}/{}/{}".format(minyear,minmon,mindate,maxyear,maxmon,maxdate))
    domain_hits = {}
    client_reqs = {}
    for r in requests:
        if r[1] not in client_reqs.keys():
            client_reqs[r[1]] = []
        client_reqs[r[1]].append((r[0],r[2]))
        d = domain_name(r[2])
        if d not in domain_hits.keys():
            domain_hits[d] = 1
        else:
            domain_hits[d] += 1

    client_reqs_hits = {}
    for k, v in client_reqs.items():
        if k not in client_reqs_hits.keys():
            client_reqs_hits[k] = {}
        for hit in v:
            d = domain_name(hit[1])
            if d not in client_reqs_hits[k].keys():
                client_reqs_hits[k][d] = 1
            else:
                client_reqs_hits[k][d] += 1
    outdir = sys.argv[1] + "-analyzer-out"
    try:
        os.makedirs(outdir)
        with open(os.path.join("output", outdir, "domain-hit-count.json"), "w") as d:
            d.write(json.dumps(domain_hits))
        with open(os.path.join("output", outdir, "domain-hit-count-per-client.json"), "w") as d:
            d.write(json.dumps(client_reqs_hits))
    except Exception as e:
        print("an error occurred:", str(e))
        exit(1)

