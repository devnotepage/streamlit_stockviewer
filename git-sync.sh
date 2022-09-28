git add .
printf "\n"

git commit -m'update'
printf "\n"

git pull -v --progress "origin"
printf "\n"

git push -v --progress "origin" main:main
printf "\n"

read -p "Complete!"
