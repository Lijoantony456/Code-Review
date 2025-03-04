#Python program to print all odd numbers in a range

#for loop
for i in range(3,17+1):
    if i%2!=0:
        print(i,end=' ')
print()

#user input
a = int(input("enter strt num"))
b = int(input("enter end num"))
for i in range(a,b+1):
    if i%2!=0:
        print(i,end=" ")
print()

#by checking start is odd or not
str = a if a&1 else a+1
[print (x,end=" ") for x in range(str,b+1) if x%2!=0]
print()

#list function
q,w=22,43
evn_lst = range(q,w+1)[q%2!=2::2]
print(evn_lst)
for i in evn_lst:
    print(i,end=' ')
print()

#lambda
lst1=[]
z,x=32,55
for i in range(z,x+1):
    lst1.append(i)
lm = list(filter(lambda x:x%2!=0,lst1))
print(lm)

#list comprehension
lst_cm = [x for x in range(z,x+1) if x%2!=0]
print(lst_cm)

#numpy
import numpy as np
e,r=22,43
arr=np.array(range(e,r+1))
arr = arr[arr%2!=0]
print(arr)

#bitwise operator
for i in range(e,r+1):
    if i&1:
        print(i,end=" ")