y = int(input())
lis = list(map(int,input().strip().split()))[:y]
q = max(lis)
while max(lis) == q:
    lis.remove(max(lis))
print(max(lis))