#!/bin/sh
# NOTE: %aI would be 100% correct ISO date
git log --date=iso -n 1 --pretty=format:"%h %ai" . > VERSION
