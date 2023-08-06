''' ##### '''
# Originally created by : KUNWAR YUVRAJ
''' ##### '''

def isEmpty(stack):
	return stack == []

def push(stack, item):
	return stack.append(item)

def pop(stack):
	return stack.pop()

def peek(stack):
	return stack[-1]

precedence = {'+':1, '-':1, '*':2, '/':2, '^':3}

def hasLessOrEqualPriority(operator1, operator2):
	try:
		if (operator1 or operator2) not in precedence:
			return False
		return precedence[operator1] <= precedence[operator2]
	except KeyError:
		return False

def isOperator(item):
	operators = ['+', '-', '/', '*', '^']
	return item in operators

def isOperand(item):
	return item.isalpha() or item.isdigit()

def isLeftParanthesis(item):
	return item == '('

def isRightParanthesis(item):
	return item == ')'

"""### INFIX SESSION STARTS ###"""

def infix_to_postfix(infix):
	infix = infix.replace(" ","")
	stack = []
	postfix = ""

	for item in infix:
		if isOperand(item):
			postfix += item
		
		elif isLeftParanthesis(item):
			push(stack, item)

		elif isRightParanthesis(item):
			while( (not isEmpty(stack)) and peek(stack) != '('):
				operator = pop(stack)
				postfix += operator

			if (not isEmpty(stack) and peek(stack) != '('):
				return -1
			else: 
				pop(stack) 
		else:
			while (not isEmpty(stack)) and hasLessOrEqualPriority(item, peek(stack)):
				postfix += pop(stack)
			push(stack,item)

	while not isEmpty(stack):
		postfix += pop(stack)
	return postfix

def infix_to_prefix(infix):
	try:
		reverse_infix = ""

		for item in infix[::-1]:
			if item == '(':
				reverse_infix += ')'
			elif item == ')':
				reverse_infix += '('
			else:
				reverse_infix += item

		reverse_postfix = infix_to_postfix(reverse_infix)

		return reverse_postfix[::-1]
	except:
		print("\nIf you are entering variables, then DON'T LEAVE ANY SPACE !!\n")

### INFIX SESSION ENDS ###
### ========================================= ###

### POSTFIX SESSION STARTS ###

# POSTFIX TO INFIX
def postfix_to_infix(postfix) : 
	try:
	    stack = []  
	    for item in postfix:   
	        if (isOperand(item)) :          
	            stack.insert(0, item)  
	        else:           
	            op1 = stack[0]  
	            stack.pop(0)  
	            op2 = stack[0]  
	            stack.pop(0)  
	            stack.insert(0, "(" + op2 + item + op1 + ")")  	            
	    return stack[0] 

	except :
		print("Enter valid postfix ")

# POSTFIX TO PREFIX
def postfix_to_prefix(postfix) :
	infix = postfix_to_infix(postfix)
	return infix_to_prefix(infix)

"""### POSTFIX SESSION ENDS ### """

"""### ========================================= ###"""

"""### PREFIX SESSION STARTS ### """

#PREFIX TO INFIX
def prefix_to_infix(prefix):
	OPERATORS = set(['+', '-', '*', '/', '(', ')'])
	PRIORITY = {'+':1, '-':1, '*':2, '/':2}
	stack = []
	prev_op = None
	for ch in reversed(prefix):
	    if not ch in OPERATORS:
	        stack.append(ch)
	    else:
	        a = stack.pop()
	        b = stack.pop()
	        if prev_op and PRIORITY[prev_op] < PRIORITY[ch]:
	            exp = '('+a+ch+b+')'
	        else:
	            exp = a+ch+b
	        stack.append(exp)
	        prev_op = ch
	return stack[-1]

#PREFIX TO POSTFIX
def prefix_to_postfix(prefix):
	infix = prefix_to_infix(prefix)
	return infix_to_postfix(infix)

"""### PREFIX SESSION ENDS ### """

"""### MAIN CONVERSION STARTS ###"""
def infix_converter(infix):
	print('Postfix :',infix_to_postfix(infix),'\nPrefix :',infix_to_prefix(infix))
	print()

def postfix_converter(postfix):
	print('Infix :',postfix_to_infix(postfix),'\nPrefix :',postfix_to_prefix(postfix))
	print()

def prefix_converter(prefix):
	print('Infix :',prefix_to_infix(prefix),'\nPostfix :',prefix_to_postfix(prefix))
	print()

"""### MAIN CONVERSION ENDS ###"""

def my_name():
    """
    This function shows heading of the program ,i.e, my name
    This supports main function
    """
    print("\nNOTATION CONVERTER BY :")

    print('''
░█─▄▀ ░█─░█ ░█▄─░█ ░█──░█ ─█▀▀█ ░█▀▀█ 　 ░█──░█ ░█─░█ ░█──░█ ░█▀▀█ ─█▀▀█ ───░█ 
░█▀▄─ ░█─░█ ░█░█░█ ░█░█░█ ░█▄▄█ ░█▄▄▀ 　 ░█▄▄▄█ ░█─░█ ─░█░█─ ░█▄▄▀ ░█▄▄█ ─▄─░█ 
░█─░█ ─▀▄▄▀ ░█──▀█ ░█▄▀▄█ ░█─░█ ░█─░█ 　 ──░█── ─▀▄▄▀ ──▀▄▀─ ░█─░█ ░█─░█ ░█▄▄█
''')

infix = "A+B*C/D"

def run():
	my_name()
	ques = ['infix', 'postfix', 'prefix']
	while True:
		print()
		print('#'*60)
		print('='*55,'\n')

		for i in ques:
		    print("Enter",ques.index(i)+1,"to convert",i,"expression")

		print("Enter ANY other key to exit !!!")
		print()

		choice = input("Enter your choice : ")
		print('='*55)
		print('#'*60)
		print()

		if choice == '1':
			infix = input("Enter infix : ")
			print()
			infix_converter(infix)
		elif choice == '2':
			postfix = input("Enter postfix : ")
			print()
			postfix_converter(postfix)
		elif choice == '3':
			prefix = input("Enter prefix : ")
			print()
			prefix_converter(prefix)
		else:
			break
if __name__ == "__main__":
	run()
