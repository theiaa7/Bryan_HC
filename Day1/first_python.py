name = input("What is your name : ")
age = int(input("What is your age : "))

print(f"Hi, nice to meet you {name}, your name data type is {type(name)} and age is {type(age)}")
print("Your age is " + str(age) + " still young\n")

if age < 10:
    print(f"Your age categorized in a kid category")
elif age > 10 and age < 17:
    print(f"You are a teenager")
else:
    print("You are an adult!")

name1 = 'bryan'
name2 = "bryan"
word = "Jum'at"
word2 = 'hey is "bad"'
word3 = "You cannot pass that \"road\""

import numpy
a = numpy.array([1,2,3,4,5])
b = [1,'bro',3.13,'23232','bryan','h']
b.append("hello")

def additions(number1,number2):
    results = number1+number2
    return results

math = additions(7,9)
#math now has 16