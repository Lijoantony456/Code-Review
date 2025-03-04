#"e"


from pyspark import SparkContext
sc=SparkContext(master='local',appName='jan').getOrCreate()

rdd=sc.textFile("/home/lijo/PycharmProjects/may_spark/file1")
rdd.foreach(print)

print("*"*33)

rdd1=rdd.map(lambda x:'yes' if('e' in x) else 'no')
rdd1.foreach(print)

print("*"*33)

rdd2=rdd.map(lambda x:x.split(' '))      #converted to word by word data
rdd2.foreach(print)