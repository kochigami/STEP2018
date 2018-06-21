#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
from collections import OrderedDict

LINKS_FILE_PATH="./wikipedia/links.txt"
PAGES_FILE_PATH="./wikipedia/pages.txt"
DATA_SIZE = 1483277

# def read_file(file_path):
#     file_data = open(file_path, "r")
#     #lines = file_data.readlines()        
    
    
#     file_data.close()
#     return lines

def make_dictionary(file_path):
    file_data = open(file_path, "r")
    dictionary = OrderedDict()
    for line in file_data:
        dictionary[(line.split())[1]] = int((line.split())[0])
    file_data.close()
    print "make dictionary finished"
    return dictionary

def make_adjacent_simple():
    adjacent = [[1, 2],
                [3, 4],
                [5, 6],
                [7, 8],
                [],
                [9],
                [],
                [],
                [],
                []]
    return adjacent

def make_adjacent(file_path):
    file_data = open(file_path, "r")
    
    adjacent = [[]] * DATA_SIZE
    for line in file_data:
        adjacent[int((line.split())[0])].append(int((line.split())[1]))

    file_data.close()
    return adjacent
    
def convert_word_to_number(dictionary, word):
    number = -1
    for i in dictionary.keys():
        if i == word:
            number = dictionary[i]
    return number

def dequeue(x):
    ret = x[0]
    x[0:] = x[1:]
    return ret

def enqueue(x, a):
    x[len(x):] = [a]

def search(adjacent, start, goal):
    dictionary = make_dictionary(PAGES_FILE_PATH)
    # print str(dictionary).decode('string-escape')
    # ex. ('奨学生', 216508)

    # convert word to number
    from_number = convert_word_to_number(dictionary, start)
    print from_number
    to_number = convert_word_to_number(dictionary, goal)
    print to_number
    if from_number == -1 or to_number == -1:
        print "word not found"
        sys.exit()
    
    q = [[from_number]]

    while len(q) > 0:
        '''
        ex. from: 0, to: 6
        print q
        
        [[0]]
        [[0, 1], [0, 2]]
        [[0, 2], [0, 1, 3], [0, 1, 4]]
        [[0, 1, 3], [0, 1, 4], [0, 2, 5], [0, 2, 6]]
        [[0, 1, 4], [0, 2, 5], [0, 2, 6], [0, 1, 3, 7], [0, 1, 3, 8]]
        [[0, 2, 5], [0, 2, 6], [0, 1, 3, 7], [0, 1, 3, 8]]
        [[0, 2, 6], [0, 1, 3, 7], [0, 1, 3, 8], [0, 2, 5, 9]]
        
        => [0, 2, 6]
        '''

        '''
        ex. q: [[0, 1], [0, 2]] 
        =>  path: [0, 1]
        =>  q: [[0, 2]]
        '''
        path = dequeue(q)
        '''
        ex. [0, 1] => 1
        '''
        last_component = path[len(path) - 1]
        if last_component == to_number:
            return path
        else:
            '''
            ex. adjacent[1] => 3, 4
            => q: [[0, 2], [0, 1, 3], [0, 1, 4]]
            '''
            for x in adjacent[last_component]:
                new_path = path[:] + [x]
                enqueue(q, new_path)

if __name__ == '__main__':
    start = time.time()

    # TODO: input word at the same time (from, to)
    from_word = raw_input("Enter words (from): ")
    to_word = raw_input("Enter words (to): ")
    
    # print search(make_adjacent_simple(), 2, 6)
    search(make_adjacent(LINKS_FILE_PATH), from_word, to_word)
    process_time = time.time() - start
    print "elapsed time: {} [s]".format(process_time) 
