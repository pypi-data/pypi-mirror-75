# accessible function in other modules
def Run(firstNumber,secondNumber):
    return __add(firstNumber,secondNumber)

def __add(firstNumber,secondNumber):
    result = firstNumber + secondNumber
    return result  

# this part is executed only when adder is the main module
if __name__ == "__main__":
    #gets the first user from user
    print("Please enter the first number")
    firstNumber = int(input())

    #gets the second number from user
    print("Please enter the second number")
    secondNumber = int(input())

    result = __add(firstNumber,secondNumber)
    print("The result is:")
    print(result)



  