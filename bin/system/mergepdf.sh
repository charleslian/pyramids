#pdftk $1.pdf $2.pdf cat output $1+SI.pdf
gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile="${1}+SI.pdf" ${1}.pdf ${2}.pdf
