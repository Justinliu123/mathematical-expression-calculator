import math
import random

BA_ASCII: int = 0b1000001
BZ_ASCII: int = 0b1011010
SA_ASCII: int = 0b1100001
SZ_ASCII: int = 0b1111010


class Function:

    def __init__(self, name: str, params: list[str], param_size: int, f: str):
        self.f = f
        self.name = name
        self.paramSize = param_size
        self.params = params

    def calculation(self, params: dict) -> float:
        # 内置函数的计算
        if self.f.startswith("math."):
            tempf = self.f
            print(tempf)
            for i in self.params:
                tempf = tempf.replace("{" + i + "}", str(params.get(i)))
            return eval(tempf)
        # 自定义函数的计算
        # 将中缀表达式转换为后缀表达式
        isFunc = False
        funcName = ""
        postfixNotation: list[str] = list()
        # 临时栈，用来处理操作符的优先级
        tempStack: list = list()
        for i in range(0, len(self.f)):
            if isFunc:
                if is_letter(self.f[i]):
                    funcName += self.f[i]
                elif self.f[i] == "(":
                    # 函数名结束
                    tempStack.append(funcName)
                    isFunc = False
                    funcName = ""
            # 处理操作数 字母
            elif (i == len(self.f) - 1 and is_letter(self.f[i])) or (
                is_letter(self.f[i]) and not is_letter(self.f[i + 1])
            ):
                postfixNotation.append(self.f[i])
            # 处理操作数 数字
            elif self.f[i].isdigit():
                number = ""
                while True:
                    if i == len(self.f) or (
                        not self.f[i].isdigit() and self.f[i] != "."
                    ):
                        break
                    number += self.f[i]
                    i += 1
                if is_number(number):
                    postfixNotation.append(number)
            # 定义函数名开始
            elif is_letter(self.f[i]) and is_letter(self.f[i + 1]):
                isFunc = True
                funcName += self.f[i]
            elif self.f[i] == ")":
                for _ in range(0, len(tempStack)):
                    operator = tempStack.pop()
                    if len(operator) > 1:
                        postfixNotation.append(operator)
                        break
                    elif operator == "(":
                        break
                    postfixNotation.append(operator)
            elif self.f[i] == "(":
                tempStack.append(self.f[i])
            # 处理操作符
            elif is_operator(self.f[i]):
                while True:
                    if len(tempStack) < 1:
                        tempStack.append(self.f[i])
                        break
                    operator = tempStack[len(tempStack) - 1]

                    # 如果栈定元素是函数或者"("则直接插入
                    if len(operator) > 1 or operator == "(":
                        tempStack.append(self.f[i])
                        break
                    if operator_priority(self.f[i], operator) > 0:
                        tempStack.append(self.f[i])
                        break
                    else:
                        postfixNotation.append(tempStack.pop())
        # 将临时栈的操作符出栈
        while len(tempStack) > 0:
            postfixNotation.append(tempStack.pop())

        # 使用后缀表达式计算, 用临时栈作为计算栈
        # print(postfixNotation)
        for i in postfixNotation:
            # 处理函数
            if len(i) > 1:
                function = STRING_FUNCTION_HASH_MAP.get(i)
                if function == None:
                    print("函数{}未定义".format(i))
                    return randomVariable()
                funcParams: dict = dict()
                paramList: list = list()
                for _ in range(0, function.paramSize):
                    paramList.append(tempStack.pop())
                paramList.reverse()
                for paramIndex in range(0, len(function.params)):
                    funcParams[function.params[paramIndex]] = paramList[paramIndex]
                tempStack.append(function.calculation(funcParams))
            elif is_letter(i):
                # 处理变量
                tempStack.append(params.get(i))
            elif is_operator(i):
                # 处理操作符
                num2 = tempStack.pop()
                num1 = tempStack.pop()
                if i == "*":
                    tempStack.append(num1 * num2)
                elif i == "/":
                    tempStack.append(num1 / num2)
                elif i == "+":
                    tempStack.append(num1 + num2)
                elif i == "-":
                    tempStack.append(num1 - num2)
                elif i == "^":
                    tempStack.append(math.pow(num1, num2))
            elif is_number(i):
                tempStack.append(float(i))
        return tempStack.pop()

    def __str__(self):
        return self.name + "(" + ",".join(i for i in self.params) + ")=" + self.f


# 存储定义函数 {'funName': Function}
STRING_FUNCTION_HASH_MAP: dict = dict()

# 存储表达式
EXPRESSION_INDEX = 0
FUNCTION_LIST: list[Function] = list()

# 存储变量值
VARIABLE_VALUE_HASH_MAP: dict = dict()

# 操作符优先级字典，数值越大优先级越高
OPERATOR_PRIORITY_MAP = {"func": 9, "()": 9, "^": 8, "*": 7, "/": 7, "+": 6, "-": 6}


# 操作符的优先级 (func = ()) > ^ > (* = /) > (+ = -)
# operator1的优先级如果大于operator2 返回正值 ，小于 返回 负值 ，等于返回 0
def operator_priority(operator1: str, operator2: str) -> int:
    if len(operator1) > 1:
        operator1 = "func"
    if len(operator2) > 1:
        operator2 = "func"
    return OPERATOR_PRIORITY_MAP.get(operator1) - OPERATOR_PRIORITY_MAP.get(operator2)


# 判断是否是操作符
def is_operator(operator: str) -> bool:
    return (
        operator == "^"
        or operator == "*"
        or operator == "/"
        or operator == "+"
        or operator == "-"
    )


def is_function(function: str) -> bool:
    if STRING_FUNCTION_HASH_MAP.get(function) == None:
        print("函数%s没定义" % (function))
        return False
    return True


def printMain():
    print("===============主界面=================")
    print("1. 定义函数")
    # 表达式定义变量必须为单字母
    print("2. 编写表达式")
    print("3. 定义变量")
    print("4. 计算")
    print("5. 清除环境")
    print("6. 查看已定义函数")
    print("7. 查看已写入表达式")
    print("8. 查看当前变量")
    print("=====================================")


def inputIntCheck(num):
    while 1:
        inputInt = 0
        try:
            inputInt = int(input("请输入："))
        except ValueError:
            print("您输入的不是数字，请再次尝试输入！")
            continue
        if inputInt < 1 or inputInt > num:
            print("选项不在范围内！")
            continue
        return inputInt


def definedFunc():
    # 定义所有基础函数
    STRING_FUNCTION_HASH_MAP["sin"] = Function("sin", ["a"], 1, "math.sin({a})")
    STRING_FUNCTION_HASH_MAP["cos"] = Function("cos", ["a"], 1, "math.cos({a})")
    STRING_FUNCTION_HASH_MAP["tan"] = Function("tan", ["a"], 1, "math.tan({a})")
    STRING_FUNCTION_HASH_MAP["floor"] = Function("floor", ["a"], 1, "math.floor({a})")
    STRING_FUNCTION_HASH_MAP["abs"] = Function("abs", ["a"], 1, "math.abs({a})")
    STRING_FUNCTION_HASH_MAP["sqrt"] = Function("sqrt", ["a"], 1, "math.sqrt({a})")
    STRING_FUNCTION_HASH_MAP["log"] = Function(
        "log", ["a", "b"], 2, "math.log({a}, {b})"
    )


def initFunc():
    STRING_FUNCTION_HASH_MAP.clear()
    FUNCTION_LIST.clear()
    definedFunc()


def defineFunction():
    funStr = input("请输入函数：")
    funStr = funStr.replace(" ", "")
    #  获取到函数的形参部分 以及 函数的表达式部分
    arraylist: list[str] = funStr.split("=")
    if len(arraylist) != 2:
        raise Exception(
            "您的表达式不属于函数，期望的格式：【函数名】(参数1,参数2) = 数学表达式"
        )
    # 解析函数名
    functionName = None
    params = None
    # 获取参数名
    trim = arraylist[0].strip()
    trim_len = len(trim)
    last_index = trim_len - 1
    now_index = 0
    for c in trim:
        if c == "(":
            functionName = trim[0:now_index]
            continue
        if c == ")":
            if functionName is None:
                raise WindowsError("请您将函数名字写上!!!")
            params = trim[len(functionName) + 1 : last_index].split(",")
        now_index += 1
    STRING_FUNCTION_HASH_MAP[functionName] = Function(
        functionName, params, len(params), arraylist[1]
    )
    print("添加函数成功")


def is_letter(char: str) -> bool:
    ascii_number = ord(char)
    # 返回该ascii码对应字符是否是字母
    return (BA_ASCII <= ascii_number <= BZ_ASCII) or (
        SA_ASCII <= ascii_number <= SZ_ASCII
    )


def is_number(s):
    try:  # 如果能运行float(s)语句，返回True（字符串s是浮点数）
        float(s)
        return True
    except ValueError:  # ValueError为Python的一种标准异常，表示"传入无效的参数"
        pass  # 如果引发了ValueError这种异常，不做任何事情（pass：不做任何事情，一般用做占位语句）
    try:
        import unicodedata  # 处理ASCii码的包

        unicodedata.numeric(s)  # 把一个表示数字的字符串转换为浮点数返回的函数
        return True
    except (TypeError, ValueError):
        pass
    return False


def randomVariable():
    return random.uniform(0.01, 10)


def expression():
    expressionStr = input("输入表达式：")
    expressionStr = expressionStr.replace(" ", "")

    params = set()
    # 解析参数
    for i in range(0, len(expressionStr)):
        # 如果是字母 判断是不是变量
        if is_letter(expressionStr[i]):
            if (i == 0) and not is_letter(expressionStr[i + 1]):
                # 判断第一个字母后面无字母
                params.add(expressionStr[i])
            elif (i == len(expressionStr) - 1) and not is_letter(expressionStr[i - 1]):
                # 判断最后一个字母前面无字母
                params.add(expressionStr[i])
            elif not is_letter(expressionStr[i + 1]) and not is_letter(
                expressionStr[i - 1]
            ):
                # 判断前后都无字母
                params.add(expressionStr[i])

    # 设置变量的默认值，如果存在值就不设置
    for i in params:
        if VARIABLE_VALUE_HASH_MAP.get(i) == None:
            VARIABLE_VALUE_HASH_MAP[i] = randomVariable()
    FUNCTION_LIST.append(
        Function("m" + str(EXPRESSION_INDEX), params, len(params), expressionStr)
    )


def allFunction():
    for i in STRING_FUNCTION_HASH_MAP.values():
        print(i)


def allExpression():
    for i in FUNCTION_LIST:
        print(i)


def defineVariable():
    print("提示：定义变量格式如：a=13")
    variableStr = input("请定义变量：")
    variableStr = variableStr.replace(" ", "")
    arraylist: list[str] = variableStr.split("=")
    if len(arraylist[0]) > 1:
        print("变量设置错误，请严格按照定义格式输入！")
        return
    VARIABLE_VALUE_HASH_MAP[arraylist[0]] = float(arraylist[1])
    print(
        "设置变量成功%s=%.2f"
        % (arraylist[0], VARIABLE_VALUE_HASH_MAP.get(arraylist[0]))
    )


def allVariable():
    print(VARIABLE_VALUE_HASH_MAP)


def calculateAll():
    for i in FUNCTION_LIST:
        # 组装每个表达式的参数值
        iParamsMap: dict = dict()
        for j in i.params:
            iParamsMap[j] = VARIABLE_VALUE_HASH_MAP.get(j)
        result = i.calculation(iParamsMap)
        print("%s=%.2f" % (i, result))


initFunc()
while 1:
    printMain()
    num = inputIntCheck(8)
    if num == 1:
        defineFunction()
    if num == 2:
        expression()
    if num == 3:
        defineVariable()
    if num == 4:
        calculateAll()
    if num == 5:
        initFunc()
    if num == 6:
        allFunction()
    if num == 7:
        allExpression()
    if num == 8:
        allVariable()
