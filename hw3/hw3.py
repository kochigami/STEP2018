#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
reference: https://github.com/xharaken/step2015/blob/master/calculator_modularize_2.py
'''

'''
readNumber

pick number (digit & float) from input equation 

input:  line, index 
output: token, index

line:  char list of input equation
index: index of line to read
token: pair of tyoe and number
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

'''
readPlus/ Minus/ Times/ DIVIDED

pick symbol from input equation 

input:  line, index 
output: token, index

line:  char list of input equation
index: index of line to read
token: type of equation (PLUS, MINUS, TIMES, DIVIDED)
'''
def readLeftBracket(line, index):
    token = {'type': 'LEFTBRACKET'}
    return token, index + 1

def readRightBracket(line, index):
    token = {'type': 'RIGHTBRACKET'}
    return token, index + 1

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

'''
tokenize

read input line and pick variables

input: line
output: tokens

line:   input equation
tokens: list of numbers and symbols
ex. [{'type': 'NUMBER', 'number': 3.2}, {'type': 'PLUS'} {'type': 'NUMBER', 'number': 0.2}]
'''

def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index] == '(':
            (token, index) = readLeftBracket(line, index)
        elif line[index] == ')':
            (token, index) = readRightBracket(line, index)
        elif line[index].isdigit():
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
    '''
    (3.0+4*(2-1))/5 =>
    [{'type': 'LEFTBRACKET'}, {'type': 'NUMBER', 'number': 3.0}, {'type': 'PLUS'}, {'type': 'NUMBER', 'number': 4}, {'type': 'TIMES'}, {'type': 'LEFTBRACKET'}, {'type': 'NUMBER', 'number': 2}, {'type': 'MINUS'}, {'type': 'NUMBER', 'number': 1}, {'type': 'RIGHTBRACKET'}, {'type': 'RIGHTBRACKET'}, {'type': 'DIVIDED'}, {'type': 'NUMBER', 'number': 5}]
    '''
    return tokens

'''
evaluate_times_and_divided

find TIMES and DIVIDED and calculate part of equation

input:  tokens
output: tokens

ex. 
input  [{'type': 'NUMBER', 'number': 3.2}, {'type': 'PLUS'} {'type': 'NUMBER', 'number': 0.2} {'type': 'TIMES'} {'type': 'NUMBER', 'number': 5}]
output [{'type': 'NUMBER', 'number': 3.2}, {'type': 'PLUS'} {'type': 'NUMBER', 'number': 1.0}]
'''

def evaluate_times_and_divided(tokens):
    index = 0
    while index < len(tokens):
        if tokens[index]['type'] == 'TIMES' or tokens[index]['type'] == 'DIVIDED':
            if tokens[index - 1]['type'] == 'NUMBER' and tokens[index + 1]['type'] == 'NUMBER':
                if tokens[index]['type'] == 'TIMES':
                    token = {'type': 'NUMBER', 'number': tokens[index - 1]['number'] * tokens[index + 1]['number']}
                elif tokens[index]['type'] == 'DIVIDED':
                    token = {'type': 'NUMBER', 'number': tokens[index - 1]['number'] / float(tokens[index + 1]['number'])}                
                tokens[index] = token #1
                del tokens[index - 1] #2
                del tokens[index]     #3
                # 0: [{'type': 'NUMBER', 'number': 2}, {'type': 'PLUS'}, {'type': 'NUMBER', 'number': 1}, {'type': 'DIVIDED'}, {'type': 'NUMBER', 'number': 2}, {'type': 'TIMES'}, {'type': 'NUMBER', 'number': 2}]
                # 1: [{'type': 'NUMBER', 'number': 2}, {'type': 'PLUS'}, {'type': 'NUMBER', 'number': 1}, {'type': 'NUMBER', 'number': 0.5}, {'type': 'NUMBER', 'number': 2}, {'type': 'TIMES'}, {'type': 'NUMBER', 'number': 2}]
                # 2: [{'type': 'NUMBER', 'number': 2}, {'type': 'PLUS'}, {'type': 'NUMBER', 'number': 0.5}, {'type': 'NUMBER', 'number': 2}, {'type': 'TIMES'}, {'type': 'NUMBER', 'number': 2}]
                # 3: [{'type': 'NUMBER', 'number': 2}, {'type': 'PLUS'}, {'type': 'NUMBER', 'number': 0.5}, {'type': 'TIMES'}, {'type': 'NUMBER', 'number': 2}]
                index -= 1
        index += 1
    return tokens

'''
evaluate_plus_and_minus

find PLUS and MINUS and calculate equation

input:  tokens
output: answer

answer: number

ex. 
input [{'type': 'NUMBER', 'number': 3.2}, {'type': 'PLUS'} {'type': 'NUMBER', 'number': 1.0}]
=> 4.2
'''

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

def search_bracket(tokens):
    brackets=[]
    for index in range(len(tokens)):
        if tokens[index]['type'] == 'LEFTBRACKET':
            brackets.append([index])

    tokens_index = 0
    if len(brackets) > 0:
        brackets_index = len(brackets) -1
        while tokens_index < len(tokens) and brackets_index > -1:
            if tokens[tokens_index]['type'] == 'RIGHTBRACKET':
                brackets[brackets_index].append(tokens_index)
                brackets_index -= 1
            tokens_index += 1

    return brackets

def calculate_inside_bracket(tokens, brackets):
    tokens_cp = []
    delete_components = 0
    for i in range(len(brackets)-1, -1, -1):
        # tokens_cp = tokens[5] ~ tokens[9]
        tokens_cp = []
        for j in range(brackets[i][0] + 1, brackets[i][1] - delete_components):
            tokens_cp.append(tokens[j])

        # tokens_cp = evaluate_times_and_divided(tokens_cp)
        # tokens_cp = evaluate_plus_and_minus(tokens_cp)
        tokens_cp = evaluate_times_and_divided(tokens_cp)
        tokens_cp = evaluate_plus_and_minus(tokens_cp)
        tokens[brackets[i][0]] = {'type': 'NUMBER', 'number': tokens_cp}

        # delete components of tokens[5]-[9] and put tokens_cp
        for j in range(brackets[i][0] + 1, brackets[i][1] + 1 - delete_components):
            del tokens[brackets[i][0] + 1]
        delete_components += (brackets[i][1] + 2 - delete_components -1) - (brackets[i][0] + 1)

    return tokens

'''
test

check if my algorithm is correct

input:  line, expectedAnswer
output: print message

answer: number

ex. 
input [{'type': 'NUMBER', 'number': 3.2}, {'type': 'PLUS'} {'type': 'NUMBER', 'number': 1.0}]
=> 4.2
'''

def test(line, expectedAnswer):
    tokens = tokenize(line)
    brackets = search_bracket(tokens)
    tokens = calculate_inside_bracket(tokens, brackets)
    tokens = evaluate_times_and_divided(tokens)
    actualAnswer = evaluate_plus_and_minus(tokens)
    if abs(actualAnswer - expectedAnswer) < 1e-8:
        print "PASS! (%s = %f)" % (line, expectedAnswer)
    else:
        print "FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer)


# Add more tests to this function :)
def runTest():
    print "==== Test started! ===="
    # read number
    test("1", 1)
    test("1.0", 1.0)

    # plus
    test("2+1", 3)

    # minus
    test("2-1", 1)

    # times
    test("2*1", 2)

    # divided
    test("2/1", 2)

    # plus & minus    
    test("1.0+2.1-3", 0.1)

    # plus & times
    test("2+1*2", 4)

    # plus & divided
    test("2+1/2", 2.5)

    # plus & times & divided
    test("2+1/2*2", 3)

    # brackets
    test("(((1)))", 1)
    test("(3.0+4*(2-1))/5", 1.4)
    test("3.0+(2.1-10/100)", 5.0)

    print "==== Test finished! ====\n"

runTest()

while True:
    print '> ',
    line = raw_input()
    tokens = tokenize(line)

    # fetch pair of brackets (left, right) (ex. [[0, 10], [5, 9]])
    brackets = search_bracket(tokens)
    # loop & and calculate inside bracket
    tokens = calculate_inside_bracket(tokens, brackets)

    tokens = evaluate_times_and_divided(tokens)
    answer = evaluate_plus_and_minus(tokens)
    print "answer = %f\n" % answer
