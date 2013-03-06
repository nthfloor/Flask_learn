#!/bin/bash
#Usage: ./git-land current_branch msg...

stamp=$(date +"%Y:%m:%d %H:%M:%S")
master=$(echo master)

git add -i
git commit -m "$stamp: $2"
git fetch --all -v --progress
git pull origin $1
git push origin $1

