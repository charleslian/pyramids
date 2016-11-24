for i in `ls $1`
do
if ! test -e $2'/'$i
  then echo $i
fi
done
