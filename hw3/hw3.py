#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
reference: https://github.com/xharaken/step2015/blob/master/calculator_modularize_2.py
'''

def readNumber(line, index):
    number = 0
    flag = 0
    keta = 1
    while index < len(line) and (line[index].isdigit() or line[index] == '.'):
        if line[index] == '.':
            flag = 1
        else:
            number = number * 10 + int(line[index])
            if flag == 1:
                keta *= 0.1
        index += 1
    token = {'type': 'NUMBER', 'number': number * keta}
    return token, index


def readPlus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1

def readMinus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def readTimes(line, index):
    token = {'type': 'TIMES'}
    return token, index + 1

def readDivided(line, index):
    token = {'type': 'DIVIDED'}
    return token, index + 1

def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = readNumber(line, index)
        elif line[index] == '+':
            (token, index) = readPlus(line, index)
        elif line[index] == '-':
            (token, index) = readMinus(line, index)
        elif line[index] == '*':
            (token, index) = readTimes(line, index)
        elif line[index] == '/':
            (token, index) = readDivided(line, index)
        else:
            print 'Invalid character found: ' + line[index]
            exit(1)
        tokens.append(token)
    return tokens

def evaluate_times_and_divided(tokens):
    index = 0
    while index < len(tokens):
        if tokens[index]['type'] == 'TIMES' or tokens[index]['type'] == 'DIVIDED':
            if tokens[index - 1]['type'] == 'NUMBER' and tokens[index + 1]['type'] == 'NUMBER':
                if tokens[index]['type'] == 'TIMES':
                    token = {'type': 'NUMBER', 'number': tokens[index - 1]['number'] * tokens[index + 1]['number']}
                elif tokens[index]['type'] == 'DIVIDED':
                    token = {'type': 'NUMBER', 'number': tokens[index - 1]['number'] / float(tokens[index + 1]['number'])}                
                tokens[index] = token
                del tokens[index - 1]
                del tokens[index]
                index -= 1
        index += 1
    return tokens

def evaluate_plus_and_minus(tokens):
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print 'Invalid syntax'
        index += 1
    return answer


def test(line, expectedAnswer):
    tokens = tokenize(line)
    tokens = evaluate_times_and_divided(tokens)
    actualAnswer = evaluate_plus_and_minus(tokens)
    if abs(actualAnswer - expectedAnswer) < 1e-8:
        print "PASS! (%s = %f)" % (line, expectedAnswer)
    else:
        print "FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer)


# Add more tests to this function :)
def runTest():
    print "==== Test started! ===="
    test("1+2", 3)
    test("1.0+2.1-3", 0.1)
    print "==== Test finished! ====\n"

runTest()

while True:
    print '> ',
    line = raw_input()
    tokens = tokenize(line)
    tokens = evaluate_times_and_divided(tokens)
    answer = evaluate_plus_and_minus(tokens)
    print "answer = %f\n" % answer
