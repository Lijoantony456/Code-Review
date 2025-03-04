#Python program to print all
# even numbers in a range

#for loop
#lst=[]
for i in range(4,15):
    if i%2==0:
        print(i,end=' ')
#         lst.append(i)
# print(lst)
print()

#user input start and end
strt = int(input("enter start num"))
end = int(input("enter end num"))
for i in range(strt,end+1):
    if i%2==0:
        print(i,end=' ')
print()

#by checking start is even or not
srt1 = int(input())
end1 = int(input())
srt1 = srt1+1 if srt1&1 else srt1
[print (x,end=' ') for x in range(srt1,end1+1,2)]
print()

#lambda
lst=[]
a,b=5,25
for i in range(a,b+1):
    lst.append(i)
evn_num = list(filter(lambda x:x%2==0,lst))
print(evn_num)

#list comprehension
evn_lst = [x for x in range(a,b+1) if x%2==0]
print(evn_lst)

#numpy
import numpy as np
q,w=3,21
arr=np.array(range(q,w+1))
evn_arr = arr[arr%2==0]
print(evn_arr)

#bitwise operator
for i in range(q,w+1):
    if not i&1:
        print(i,end=' ')