import re

operators = ("+", "-", "*", "/")


class Expression:
    def __init__(self, expression: str, compiled_re, operand_solver):
        self.__output = []
        self.__is_valid = 1
        self.__tokens = []
        self.__token_type = []
        self.__natural_flag = 0
        self.__expression_text = expression
        self.__compiled_re = compiled_re
        self.__expression_tokenizer(operand_solver)
        self.__shunting_yard()
        self.__solver()

    # the compiled re must be able to identify numeric and non-numeric operands.

    def __expression_tokenizer(self, operand_solver):
        string_index = 0
        while string_index < len(self.__expression_text):
            if self.__expression_text[string_index] in operators:
                self.__tokens.append(self.__expression_text[string_index])
                self.__token_type.append(1)
                string_index += 1
            else:
                m = self.__compiled_re.match(self.__expression_text, string_index)
                if m is not None:
                    m = m.group(0)
                    try:
                        int_m = int(m)
                        self.__tokens.append(int_m)
                        self.__token_type.append(2)
                    except ValueError:
                        if self.__is_dice(m):
                            operand_value, temp_flag = self.__dice_solver(m, operand_solver)
                            self.__tokens.append(operand_value)
                            if temp_flag != 0:
                                self.__natural_flag = temp_flag
                        else:
                            self.__tokens.append(m)
                    self.__token_type.append(3)
                    string_index += len(m)
                else:
                    self.__is_valid = 0
                    return

    def __shunting_yard(self):
        operator_stack = []
        for i in range(len(self.__tokens)):
            if self.__token_type[i] == 1:
                while len(operator_stack) > 0:
                    self.__output.append(operator_stack[-1])
                    operator_stack.pop()
                operator_stack.append(self.__tokens[i])
            else:
                self.__output.append(self.__tokens[i])
        while len(operator_stack) > 0:
            self.__output.append(operator_stack[-1])
            operator_stack.pop()

    def __solver(self):
        stack = []
        for token in self.__output:
            if token == "+":
                try:
                    op_1 = stack[-1]
                    stack.pop()
                    op_2 = stack[-1]
                    stack.pop()
                    stack.append(op_1 + op_2)
                except IndexError:
                    self.__is_valid = 0
                    return
            elif token == "-":
                try:
                    op_1 = stack[-1]
                    stack.pop()
                    op_2 = stack[-1]
                    stack.pop()
                    stack.append(op_2 - op_1)
                except IndexError:
                    self.__is_valid = 0
                    return
            else:
                stack.append(token)
        self.__output = stack[0]

    def is_valid(self):
        return self.__is_valid

    def result(self):
        return self.__output

    def is_1_or_20(self):
        return self.__natural_flag

    @staticmethod
    def __dice_solver(string, operand_solver):
        faces = 0
        ad = 0
        ad_flag = 0
        if string[0] == "d":
            dice_number = 1
            faces = int(string[1:])
        else:
            string_numbers = string.split("d")
            dice_number = int(string_numbers[0])
            numbers_len = len(string_numbers)
            if numbers_len == 3:
                faces = int(string_numbers[1])
                ad = int(string_numbers[2])
                ad_flag = 2
            elif numbers_len == 2:
                try:
                    faces = int(string_numbers[1])
                except ValueError:
                    new_numbers = string_numbers[1].split("k")
                    faces = int(new_numbers[0])
                    ad = int(new_numbers[1])
                    ad_flag = 1
        dice_tosses = operand_solver(1, faces, dice_number)
        result = 0
        if ad_flag == 0:
            result = sum(dice_tosses)
        elif ad_flag == 1:
            dice_tosses.sort()
            result = sum(dice_tosses[-ad:])
        elif ad_flag == 2:
            dice_tosses.sort()
            result = sum(dice_tosses[:ad])
        if faces == 20:
            if result == 1:
                return result, 1
            elif result == 20:
                return result, 2
        return result, 0

    @staticmethod
    def __is_dice(string):
        return bool(re.match(r"\d*d\d+k\d+|\d*d\d+d\d+|\d*d\d+", string))
