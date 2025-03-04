#collect

from pyspark import SparkContext
sc=SparkContext(master='local',appName='jan').getOrCreate()
rdd=sc.parallelize([i for i in range(1,21)])
rdd.foreach(print)

print("*"*33)

#collect===> convert rdd to python list
#syntax==>
#      variable_name=rdd.collect()

lst=rdd.collect()
print(lst)