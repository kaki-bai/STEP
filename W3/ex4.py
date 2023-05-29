#! /usr/bin/python3

# Output: token, index
#         token = {'type': 'NUMBER', 'number': number}
def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index

# Output: token, index
#         token = {'type': 'PLUS'},
def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1

def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def read_multiply(line, index):
    token = {'type': 'MULTIPLY'}
    return token, index + 1

def read_divide(line, index):
    token = {'type': 'DIVIDE'}
    return token, index + 1

def read_left_bracket(line, index):
    token = {'type': 'LEFT_BRACKET'}
    return token, index + 1

def read_right_bracket(line, index):
    token = {'type': 'RIGHT_BRACKET'}
    return token, index + 1

def read_abs(line, index):
    token = {'type': 'ABS'}
    return token, index + 3

def read_int(line, index):
    token = {'type': 'INT'}
    return token, index + 3

def read_round(line, index):
    token = {'type': 'ROUND'}
    return token, index + 5

# Input: line      eg."1+1"
# Output: tokens   eg.[{'type': 'NUMBER', 'number': 1},
#                      {'type': 'PLUS'},
#                      {'type': 'NUMBER', 'number': 1}]
def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_multiply(line, index)
        elif line[index] == '/':
            (token, index) = read_divide(line, index)
        elif line[index] == '(':
            (token, index) = read_left_bracket(line, index)
        elif line[index] == ')':
            (token, index) = read_right_bracket(line, index)
        elif line[index:index+3] == 'abs':
            (token, index) = read_abs(line, index)
        elif line[index:index+3] == 'int':
            (token, index) = read_int(line, index)
        elif line[index:index+5] == 'round':
            (token, index) = read_round(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens

def calculate_plus_minus(tokens):
    answer = 0
    index = 1
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer

def calculate_multi_divide(tokens):
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'MULTIPLY':
            tokens[index-1]['number'] *= tokens[index+1]['number']
            del tokens[index:index+2]
        elif tokens[index]['type'] == 'DIVIDE':
            tokens[index-1]['number'] /= tokens[index+1]['number']
            del tokens[index:index+2]
        else:
            index += 1

def calculate_brackets(tokens):
    # print('coming')
    while True:
        # print(f'brackets:{tokens}')
        index = 0
        index_left = -1
        index_right = -1
        while index < len(tokens):
            # print(tokens[index])
            if tokens[index]['type'] == 'LEFT_BRACKET':
                index_left = index
            elif tokens[index]['type'] == 'RIGHT_BRACKET' and index_left != -1:
                index_right = index
                break
            index += 1
        
        if index_left != -1 and index_right != -1:
            # print(index_left, index_right)
            answer_in_brackets = evaluate(tokens[index_left+1:index_right])
            # print(answer_in_brackets)
            tokens = tokens[:index_left] + [{'type': 'NUMBER', 'number': answer_in_brackets}]+ tokens[index_right+1:]
            # print(f'brackets:{tokens}')
        else:
            break
        # print(f'brackets:{tokens}')
    return tokens

def calculate_function_inside(tokens, index_left):
        index = index_left
        index_right = -1
        count_left_bracket = 0
        count_right_bracket = 0

        if tokens[index]['type'] != 'LEFT_BRACKET':
            print('Invalid syntax')
            print(tokens[index])
            exit(1)
        else:
            index += 1

        while index < len(tokens):
            # print(tokens[index])
            if tokens[index]['type'] == 'LEFT_BRACKET':
                count_left_bracket += 1
            elif tokens[index]['type'] == 'RIGHT_BRACKET':
                count_right_bracket += 1
                if count_right_bracket == count_left_bracket + 1:
                    index_right = index
                    break
            index += 1
        
            # print(index_left, index_right)
        answer_in_brackets = evaluate(tokens[index_left+1:index_right])
        # print(answer_in_brackets)
        return index_right, answer_in_brackets

def find_function_index(tokens, function_name):
        index = 0
        index_left = -1
        while index < len(tokens):
            if tokens[index]['type'] == function_name:
                index += 1
                index_left = index
                break
            index += 1
        return index_left

def function_abs(tokens):
    while True:
        # print(f'abs:{tokens}')
        index_left = find_function_index(tokens, 'ABS')
        
        if index_left == -1:
            return tokens
        else:
            index_right, answer_in_brackets = calculate_function_inside(tokens, index_left)

            if answer_in_brackets < 0:
                answer_abs = -1 * answer_in_brackets
            else:
                answer_abs = answer_in_brackets
            
            tokens = tokens[:index_left-1] + [{'type': 'NUMBER', 'number': answer_abs}]+ tokens[index_right+1:]
            return tokens

def function_int(tokens):
    while True:
        # print(f'abs:{tokens}')
        index_left = find_function_index(tokens, 'INT')
        
        if index_left == -1:
            return tokens
        else:
            index_right, answer_in_brackets = calculate_function_inside(tokens, index_left)

            answer_int = answer_in_brackets // 1
            
            tokens = tokens[:index_left-1] + [{'type': 'NUMBER', 'number': answer_int}]+ tokens[index_right+1:]
            return tokens

def function_round(tokens):
    while True:
        # print(f'abs:{tokens}')
        index_left = find_function_index(tokens, 'ROUND')
        
        if index_left == -1:
            return tokens
        else:
            index_right, answer_in_brackets = calculate_function_inside(tokens, index_left)

            if answer_in_brackets * 10 % 10 >= 5:
                answer_round = answer_in_brackets // 1 + 1
            else:
                answer_round = answer_in_brackets // 1
            
            tokens = tokens[:index_left-1] + [{'type': 'NUMBER', 'number': answer_round}]+ tokens[index_right+1:]
            return tokens

def evaluate(tokens):
    # print(f'main1:{tokens}')
    tokens = function_abs(tokens)
    tokens = function_int(tokens)
    tokens = function_round(tokens)
    tokens = calculate_brackets(tokens)
    # print(f'main2:{tokens}')
    calculate_multi_divide(tokens)
    answer = calculate_plus_minus(tokens)
    return answer


def test(line):
    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    test("1+2")
    test("1.0+2.1-3")

    test("1+2*3")
    test("1+1/2")
    test("1.0+1.0/2.0")
    test("1.0+2.0/3.0*4.0")
    test("1.0+1.0/2.0-6+7.989")
    test("(1+1)/2")
    test("(1+1)/2*(1+1)")
    test("(1+1)/2-2/(2*3)")
    test("(1+1)/(2.0*(1+3))")
    
    test("abs(1-2)")
    test("abs(1-2)+1")
    test("abs(1/2)*2")
    test("abs((1-2)*2)")
    test("abs((1.0-2.0)*(1+2))")

    test("int(1.5)")
    test("int(1.5*3)")
    test("int((1.5+2)/2)")
    test("int((1.5+2)/2)+1")
    test("int((1.5+2)/2)/(2.0+1)")
    test("int((1.5+2)/2)/abs(1-2)")
    test("int(abs(1.5-2)/2)")

    test("round(1.4)")
    test("round(1.5)")
    test("round(1.39)")
    test("round(1.51)")
    test("round(abs(1.4-2))")
    test("round(int(abs(1.4-2)))")
    test("round(int(abs(1.4-2)/2)+1)/2")
    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)