
lst = [250,33,56,43,45,76,83,22,99,81,76,73]

#asc order
lst.sort()
print(lst[0])

#desc order
lst.sort(reverse=True)
print(lst[-1])

#min function
print(min(lst))

#comparing every element
min = lst[0]
for i in range(len(lst)):
  if lst[i]<min:
   min=lst[i]
print(min)

#lambda
from functools import reduce
lst = [250,33,56,43,45,76,83,22,99,81,76,73]
pr=reduce(lambda x,y:x if x<y else y,lst )
print(pr)

#numpy
import numpy as np
minn = np.min(lst)
print(minn)


