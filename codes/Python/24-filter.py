#sample4.txt

#id,name,

#1. age above 22 fname,lname,age,loc
#2. chennai work fname,lname,age,prof,loc
#3.age above 22 and loc chennai fname,lname,age,prof,loc
#4.age 2 increment fname,lname,age,prof

from pyspark import SparkContext
sc=SparkContext(master='local',appName='jan').getOrCreate()
rdd=sc.textFile("/home/lijo/Downloads/sample4.txt")
rdd.foreach(print)

print("**"*22)

rdd1=rdd.map(lambda x:x.split(","))
rdd1.foreach(print)

print("**"*22)
#1.
rdd2=rdd1.filter(lambda x:x[3]>'22').map(lambda x:[x[1],x[2],x[3],x[5]])
rdd2.foreach(print)

print("**"*22)
#2.
rdd3=rdd1.filter(lambda x:x[5]=='chennai').map(lambda x:[x[1],x[2],x[3],x[5]])
rdd3.foreach(print)

print("**"*22)
#3.
rdd4=rdd1.filter(lambda x:x[3]>'22' and x[5]=='chennai').map(lambda x:[x[1],x[2],x[3],x[5]])
rdd4.foreach(print)

print("**"*22)
#4.
rdd5=rdd1.map(lambda x:(int(x[3])+2))
rdd5.foreach(print)