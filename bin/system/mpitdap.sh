#/bin/bash
if [ -z $1 ] 
then
  core=`cat /proc/cpuinfo| grep "processor"| wc -l`
  echo "Run with all cores, i.e. " $core "cores"
else
  core=$1
  echo "Run with " $core " core"
fi

mpirun -np $core $HOME/Desktop/tdap/Obj/tdap < input.fdf > result 
