git add .
echo "Enter the commit message"
read message
git commit -m"$message"
echo "Enter the branch"
read branch
git push origin "$branch"