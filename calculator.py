import sys
import fractions
operators = {"+": 1, "-": 1, "*": 2, "/": 2,"^": 3,"$":4}
def isANumber(string):
  isANumber = False
  try:
    converted = int(string)
    isANumber = True,converted
    if str(converted) != string:
      isANumber = True,float(string)
  except ValueError:
    try:
      converted = float(string)
      isANumber = True,converted
    except ValueError:
      isANumber = False,string
  return isANumber

def performTokenOperation(token,operand1,operand2):
  if token == "+":
    return operand1 + operand2
  elif token == "-":
    return operand1 - operand2
  elif token == "*" or token == "$":
    return operand1 * operand2
  elif token == "/":
    if operand2 == 0:
      sys.exit(f"CALCULATION ERROR: Cannot divide {operand1} by {operand2}")
    return operand1 / operand2
  elif token == "^":
    return operand1 ** operand2

def validateRawInputString(rawInputString):
  if any(character.isalpha() for character in rawInputString):
    sys.exit("CALCULATION ERROR: Letters found in equation")
  if rawInputString.count("(") != rawInputString.count(")"):
    sys.exit("SYNTAX ERROR: Missing parentheses in expression")
  if rawInputString[0] in operators or rawInputString[-1] in operators:
    sys.exit("SYNTAX ERROR: Expression cannot start or end with operators")
  return rawInputString
    
def parseInputString(rawInput):
  stack = [character for character in rawInput]
  output = []
  for character in stack:
    if character in operators:
      output.append(character)
    elif character == ".":
      output.append(output.pop() + character)
    elif character.isnumeric():
      if not output:
        output.append(character)
      elif "." in output[-1] or output[-1].isnumeric():
        previousNumber = output.pop()
        newNumber = previousNumber + character
        output.append(newNumber)
      else:
        output.append(character)
    elif character == "(":
      if output and isANumber(output[-1])[0]:
        output.append('$')
      output.append(character)
    elif character == ")":
      output.append(character)
  return output
        
def generatePostfix(expression):
  output = []
  stack = []

  for token in expression:
    numberCheck = isANumber(token)
    if numberCheck[0]:
      output.append(str(numberCheck[1]))
    elif token == "(":
      stack.append(token)
    elif token == ")":
      while stack and stack[-1] != "(":
        output.append(stack.pop())
      stack.pop()
    elif token in operators:
      while (stack and stack[-1] in operators
             and operators[stack[-1]] >= operators[token]):
        output.append(stack.pop())
      stack.append(token)

  while stack:
    output.append(stack.pop())
  return output

def generateResult(postfix):
  stack = []
  for token in postfix:
    numberCheck = isANumber(token)
    if numberCheck[0]:
      stack.append(numberCheck[1])
    elif token in operators:
      operand2 = stack.pop()
      operand1 = stack.pop()
      stack.append(performTokenOperation(token,operand1,operand2))
  return stack[0]

def convertToFraction(result):
  fraction = fractions.Fraction(result).limit_denominator()
  if "/" not in str(fraction):
    return ""
  else:
    return f"As fraction - {fraction}"
  

def main():
  rawInput = input("Please key in your expression: ").replace(" ", "")
  expression = parseInputString(validateRawInputString(rawInput))
  print(f"\nParsed input string: {expression}\n")
  postfix = generatePostfix(expression)
  print(f"Postfix: {' '.join(postfix)}\n")
  result = isANumber(generateResult(postfix))[1]
  if isinstance(result,float):
    result = f"{result:.9f}"
  print(f"Result: \nAs float/integer - {result}\n{convertToFraction(result)}")

main()
