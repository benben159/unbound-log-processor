# Unbound DNS Request Log Processor

## Requirements

 - Python 3.4 with standard libraries

## Description

This project consist of a shell script for cleaning up raw log and
convert it into CSV file. The CSV file has enough information to be
analyzed using the Python script. The Python script's output is a JSON
formatted file: 

1. domain-hit-count.json
  this file counts the 2nd/3rd level domain (`*.facebook.com` or `*.google.co.id`) requests
1. domain-hit-count-per-client.json
  this file counts the 2nd/3rd level domain requests filtered by client


## To Do List

 - fixing shell script using only `awk`
 - next release: eliminating shell script, so the Python script can process raw logs directly
