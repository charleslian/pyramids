for i in `ls $1`
do
diffCont=`diff -q -i $1'/'$i $2'/'$i 2> /dev/null`
#echo $diffCont
if [[ $diffCont != "" ]]; then 
 #echo $diffCont
 echo $i
fi
done
