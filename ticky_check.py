#!/usr/bin/env python3
import sys
import re
import csv
import operator

#  initialize two dictionaries
error = {}  
number_per_user = {}

error_report = 'error_message.csv'
number_per_user_report = 'user_statistics.csv'

logfile = 'syslog.log'


pattern = r'(?P<messageType>INFO|ERROR):?\s*(?P<message>.*?)\((?P<username>\w+)\)$'

with open(logfile, 'r') as file:
    for line in file.readlines():
        regex_result = re.search(pattern, line)
        if regex_result:
            message_type = regex_result.group('messageType')
            message = regex_result.group('message')
            username = regex_result.group('username')
            if message_type == 'ERROR':
                error.setdefault(message, 0)
                error[message] += 1
                number_per_user.setdefault(username, [0, 0])[1] += 1
            else:
                number_per_user.setdefault(username, [0, 0])[0] += 1

error_sorted = sorted(error.items(), key=operator.itemgetter(1), reverse=True)
number_per_user_sorted = sorted(number_per_user.items())

with open(error_report, 'w', newline='') as error_report:
    writer = csv.writer(error_report)
    writer.writerow(['Error', 'Count'])
    writer.writerows(error_sorted)

with open(number_per_user_report, 'w', newline='') as user_report:
    writer = csv.writer(user_report)
    writer.writerow(['Username', 'INFO', 'ERROR'])
    for item in number_per_user_sorted:
        onerow = [item[0], item[1][0], item[1][1]]
        writer.writerow(onerow)
