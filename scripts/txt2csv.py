# -*- coding: utf-8 -*-
from __future__ import print_function
import csv
import os
import sys

input_filename = sys.argv[1]
output_filename, ext = os.path.splitext(input_filename)
output_filename += "_utf8.csv"

with open(sys.argv[1], newline='', encoding='utf-8') as csv_input:
    with open(output_filename, "w", newline='', encoding='utf-8') as csv_output:
        reader = csv.reader(csv_input, delimiter=',')
        writer = csv.writer(csv_output, delimiter=';')
        for row in reader:
            writer.writerow(row)

print("Ok")
