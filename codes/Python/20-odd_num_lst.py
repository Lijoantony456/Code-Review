#Python program to print odd numbers in a List

lst = [2,3,34,45,567,6,32,33,4,56,7,5,3,2,1]

#for loop
for i in lst:
    if i%2==1:
        print(i,end=" ")

#while loop

n=0
while n<len(lst):
    if lst[n]%2==1:
        print(lst[n],end=" ")
    n+=1

#list comprehension

odd = [x for x in lst if x%2==1]
print(odd)

#lambda
odd_n = list(filter(lambda x:x%2!=0,lst))
print(odd_n)

#numpy
import numpy as np
arrr = np.array(lst)
np_odd= arrr[arrr%2==1]
print(np_odd)

#numpy(where)
odd_wh= arrr[np.where(arrr%2!=0)]
print(list(odd_wh))