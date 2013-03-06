#!/bin/bash
#Usage: git-land test_branch ...

stamp=$(date +"%Y:%m:%d %H:%M:%S")
master=$(echo master)

git add -i
git commit -m "$stamp: Merge and land latest changes"
git checkout $master
git fetch --all -v --progress
git pull origin $master
git merge $1
git push origin $master
git checkout $1

#set -x
#git fetch --all
#for branch in "$@"; do
#    git checkout "$branch"      || exit 1
#    git rebase "origin/$branch" || exit 1
#done
