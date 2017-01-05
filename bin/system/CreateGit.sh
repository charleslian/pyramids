gitName=`basename $PWD`
ssh lianchao@159.226.36.145 /home/lianchao/bin/buildGitServer.sh $gitName
git init
git add .
git commit -m 'initial commit'
git remote add origin lianchao@159.226.36.145:/home/lianchao/$gitName".git"
git push origin master
