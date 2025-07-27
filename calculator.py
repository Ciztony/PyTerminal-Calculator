import sys
import fractions

operators = {"+": 1, "-": 1, "*": 2, "/": 2,"^": 3,"$":4}

def isANumber(string):
  isANumber = False
  try:
    converted = int(string)
    isANumber = True,converted
    if str(converted) != string: # Check that the integer converted is actually an integer and not rounded off, otherwise return the string as a float
      isANumber = True,float(string)
  except ValueError:
    try:
      converted = float(string)
      isANumber = True,converted
    except ValueError:
      isANumber = False,string
  return isANumber

def performTokenOperation(token,operand1,operand2):
  # Handles operation of previous two operands in stack
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
    
  if not (rawInputString[0].isnumeric() or rawInputString[0] == "(") or not (rawInputString[-1].isnumeric() or rawInputString[-1] == ")"):
    sys.exit("SYNTAX ERROR: Expression can only start and end with parentheses and/or numbers")
    
  if any(character for character in rawInputString if not character.isnumeric() and character not in ["+","-","/","*","(",")","^","."]):
    sys.exit("SYNTAX ERROR: Unknown operator found in expression")
  
  for index,character in enumerate(list(filter(lambda x: x==".",rawInputString))):
    if not rawInputString[index-1].isnumeric() or not rawInputString[index+2].isnumeric():
      sys.exit("SYNTAX ERROR: Decimal syntax invalid") # Check if there are invalid characters around the decimal point
  
  def acceptableTokenEnclosingAroundOperator(before,after):
    print(before, after)
    if before == "(" or not before.isnumeric():
      sys.exit("SYNTAX Error: Unacceptable syntax around operator")
    if after == ")" or not after.isnumeric():
      sys.exit("SYNTAX Error: Unacceptable syntax around operator")
      
  # Ensures there aren't invalid characters around operators    
  for index,character in enumerate(list(filter(lambda x:x in operators,rawInputString))):
    acceptableTokenEnclosingAroundOperator(rawInputString[index-1],rawInputString[index+2])
   
  return rawInputString

def parseInputString(rawInput):
  stack = [character for character in rawInput]
  output = []
  for character in stack:
    if character in operators:
      output.append(character)
    elif character == ".":
      output.append(output.pop() + character) # Add the decimal point to the number before the . 
    elif character.isnumeric():
      if not output:
        output.append(character)
      elif "." in output[-1] or output[-1].isnumeric(): # Add the character to the previous one if the previous element is decimal point or is a number
        previousNumber = output.pop()
        newNumber = previousNumber + character
        output.append(newNumber)
      else:
        output.append(character)
    elif character == "(":
      if output and (isANumber(output[-1])[0] or output[-1]==")"): # In the situation that the user inputs 2(5) without explicitly stating the * we use $ to signify a higher order of operation like 2(5+6) -> 2$(5+6) so that $ is carried out after the internal expression 5+6 is evaluated
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
      stack.pop() # Push all operators onto output until ( is found
    elif token in operators:
      while (stack and stack[-1] in operators
             and operators[stack[-1]] >= operators[token]):
        output.append(stack.pop()) # while top of stack has an operator higher in precedence than the character, append it to the output 
      stack.append(token)

  while stack: # Combine remaining part of the stack onto the output
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
  result = generateResult(postfix)
  if str(result).endswith(".0"):
    result = int(result)
  print(f"Result: \nAs float/integer - {result}\n{convertToFraction(result)}")

main()
