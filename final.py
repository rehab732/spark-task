# -*- coding: utf-8 -*-
"""final.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/112N-xJaGtb_wcZo0E7lBHRTrU2pQTROH
"""

# All import and installation
!pip install pyspark
import pyspark
sc = pyspark.SparkContext('local[*]')

!apt-get update
!apt-get install openjdk-8-jdk-headless -qq > /dev/null
!wget -q http://a...content-available-to-author-only...e.org/dist/spark/spark-2.3.1/spark-2.3.1-bin-hadoop2.7.tgz
!tar xf spark-2.3.1-bin-hadoop2.7.tgz
!pip install -q findspark
 
import os
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"
os.environ["SPARK_HOME"] = "/content/spark-2.3.1-bin-hadoop2.7"
 
!ls
 
import findspark
findspark.init()
 
import pyspark
from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate() 
spark

#Query number 1
#Retrive the first 10 records
data=sc.textFile("/content/1.out")
data.take(10)

#Q2-->max for page size

def parse(line):
  collomns=line.split(" ")
  pagesize=float(collomns[3])
  key=0
  return(key,pagesize)
data=sc.textFile("/content/1.out")
pagesize=data.map(parse)
maxx=pagesize.reduceByKey(lambda x , y: max(x,y))
maxx.saveAsTextFile('max.tx')

#Q2-->min for page size
def parse_linee(line):
  col=line.split(" ")
  pagesize=float(col[3])
  key=0
  return (key,pagesize)
data=sc.textFile("/content/1.out")
pagesize=data.map(parse_linee)
minn=pagesize.reduceByKey(lambda x , y: min(x,y))
minn.saveAsTextFile('min.tx')

#Q2-->avg for page size
def parsee(line):
  col=line.split(" ")
  page_size=float(col[3])
  return (page_size)
data=sc.textFile("/content/1.out")
page_size=data.map(parsee)
listofavg=[]
resultt=page_size.mean()
listofavg.append(resultt)
final_rdd=sc.parallelize(listofavg)
final_rdd.saveAsTextFile('avg.tx')

#Query number 3
#number of page title start with The and not en
import re
def parse_data(line):
  collomns=line.split(" ")
  return(collomns[0],collomns[1])
data=sc.textFile("/content/1.out")
page_title=data.map(parse_data)
result=page_title.filter(lambda x: (x[1].startswith('The'))&('en'!= x[0]))
pagetitlecount=result.distinct().count()
listcount=[]
listcount.insert(0,pagetitlecount)
rddd=sc.parallelize(listcount)
rddd.saveAsTextFile('ya_rab.tx')

#Query number 4
#number of unique terms in page title
import re


def parseLine(line):
 fields = line.split(" ")
 f1=fields[1]
 s = re.sub(r'[^a-zA-Z_]','', f1).upper()
 return s

def parseLine22(line):
 fields = line.split("_")
 return fields
data=sc.textFile("/content/1.out")
pagetitle=data.map(parseLine)# page title
page_titlev2=pagetitle.map(parseLine22)
r1=page_titlev2.flatMap(lambda x:x).distinct().count()
list4=[]
list4.insert(0,r1)
sc.parallelize(list4).saveAsTextFile('queryfour')#list RDD

#Query number 5
#most frequent occuring page title in the data set
def parseLine(line):
 fields = line.split(" ")
 return (fields[1])
data=sc.textFile("/content/1.out")
pagetitle=data.map(parseLine)
test=pagetitle.map(lambda x: (x,1))
test2=test.groupByKey()
test3=test2.mapValues(sum).map(lambda x:(x[1],x[0])).sortByKey(False)
sc.parallelize(test3.take(1)).saveAsTextFile('queryfive')