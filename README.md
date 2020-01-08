# Useful Git commands

## General commands

To check if there are any differences between your local branch and master
```bash
git status
```

## In order to get latest changes from github

If you want to pull latest changes from Github and you wan to abort the work you did locally
```bash
git stash
```

To check if there are any differences between your local branch and master
```bash
git pull
```

## In order to publish local changes from github

If you want to add a file for a commit 
```bash
git add [filename]
```

If you want to create a commit
```bash
git commit -m 'description of what you are commiting and why'
```

To push it to github
```bash
git push
```
# Auto Linting

To install
```bash
pip install --upgrade autopep8
```

To run auto lining locally
```bash
autopep8 [filename]
```
