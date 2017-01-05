date=`date +%y%m%d`
filename="$1"."$date".tar.gz
tar cvzf $filename --exclude-tag-all=add_output.o $1
cp -r $filename $HOME/backup
