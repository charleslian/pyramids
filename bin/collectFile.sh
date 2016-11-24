#!/bin/bash
echo $1 $2
for i in `find $1 -name $2`
do 
j=`echo $i| sed s/'\/'/-/g`
cp $i $j
 done
