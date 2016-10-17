#!/bin/sh

grep info | grep '192.168.' | grep -v 'AAAA IN' | awk '{print $1 ";" $4 ";" $5}' | sed -e 's/[//g' | sed -e 's/]//g'
