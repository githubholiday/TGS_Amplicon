git add -A 
git commit -m "串联整个流程推送"
git push

echo "# tgs_amplicon" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin git@github.com:githubholiday/tgs_amplicon.git
git push -u origin main



