#union
#intersection

from pyspark import SparkContext
sc=SparkContext(master='local',appName='jan').getOrCreate()
rdd=sc.parallelize(i for i in range(1,31))
rdd1=sc.parallelize(i for i in range(10,51))
rdd.foreach(print)

print("*"*33)

rdd1.foreach(print)

print("*"*33)

#union
#combined result when joining two dataset
#duplicate values are included

#syntax
#newrdd=oldrdd1.union(oldrdd2)

rdd2=rdd.union(rdd1)
rdd2.foreach(print)

print("*"*33)

rdd3=rdd2.distinct()
rdd3.foreach(print)

print("*"*33)

#intersection
#collect common elements from two dataset(rdd)

rdd4=rdd.intersection(rdd1)
rdd4.foreach(print)