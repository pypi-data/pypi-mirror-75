import adder

# Althogh the module is imported here, only its Run method is accessible here
# Other methods such as __add is not added 
# Other parts of adder such as getting numbers from end user is not executed
# because the adder is not the main module anymore 

result = adder.Run(1,2)
print("1 + 2 = " + str(result))