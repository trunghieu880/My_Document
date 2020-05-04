#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the solve function below.
def solve(s):
    result = []
    for item in s.strip().split(" "):
        result.append(item.capitalize())
    return ' '.join(result)

if __name__ == '__main__':
    fptr = open('OUTPUT_PATH', 'w')
    s = input()
    result = solve(s)
    fptr.write(result + '\n')
    fptr.close()
