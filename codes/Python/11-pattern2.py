

import string
# def print_rangoli(n):
#     list1=[]
#     alphabet = list(string.ascii_letters)
#     print(alphabet)
#     for x in range(1, n+1):
#         list1.insert(x-1, alphabet[n-x])
#         print(list1)
#         list2=list1[0:x-1]
#         print(list2)
#         list2.reverse()
#         print(list2)
#         list3=list1+list2
#         s='-'.join(list3)
#         print(s)
#         print(s.center(4*n-3, '-'))
#     for x in range(1, n):
#         list1.pop(-1)
#         print(list1)
#         list3=list1[0:-1]
#         print(list3)
#         list3.reverse()
#         list3=list1+list3
#         s='-'.join(list3)
#         print(s.center(4*n-3, '-'))
#
#     # your code goes here
#
# if __name__ == '__main__':
#     n = int(input())
#     print_rangoli(n)




alpha = string.ascii_lowercase
print(alpha)
n = int(input())
L = []
for i in range(n):
    s = "-".join(alpha[i:n])
    #print(s)
    L.append((s[::-1]+s[1:]).center(4*n-3, "-"))
    #print(L)
print('\n'.join(L[:0:-1]+L))