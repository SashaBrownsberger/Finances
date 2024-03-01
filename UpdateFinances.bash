#First, make sure we're up to date with the repo
git checkout main
git fetch origin

#Now run the python script that does the updating and makes the plots
python UpdateFinances.py

#Now that we're all done, push changes to the repo
echo "Enter the comment you want to include with your GitHub push"
read user_comment
git add .
git commit -m "$user_comment"
git push -u origin main
