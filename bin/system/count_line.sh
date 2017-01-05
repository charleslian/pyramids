NEW=`wc -l /home/lianchao/Desktop/TDAP/Src/* 2> /dev/null |tail -1 |cut -c 1-7`
OLD=`wc -l /home/lianchao/Downloads/SoftWares/siesta-3.2-pl-5/Src/* 2> /dev/null  |tail -1 |cut -c 1-7`
let "ADDED=$NEW-$OLD"
echo -e "SIESTA:\033[49;36;1m" $OLD "\033[0m TDAP:\033[49;36;1m" $NEW "\033[0m ADDED:\033[49;36;1m" $ADDED "\033[0m"
