DENCHAR=/home/lianchao/Desktop/TDAP-2.0.0.Alpha/Util/Denchar/Src/denchar

mkdir denchar-run
cp *.PLD denchar-run
cp *.DIM denchar-run
cp *.ion denchar-run
cp *.DM denchar-run
cp *.WFSX denchar-run
cp input.fdf denchar-run

cd denchar-run
cat >>input.fdf<<!
#  *************************************************************************
#                     Input variables for Denchar
#  (besides SystemLabel, NumberOfSpecies and ChemicalSpecies, defined above)
#  *************************************************************************

Denchar.TypeOfRun      3D

Denchar.PlotCharge          T
Denchar.PlotWaveFunctions   F
!
$DENCHAR < input.fdf
