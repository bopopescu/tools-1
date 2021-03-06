#!/bin/bash

#############################################
# File Name: update.sh
# Author: xiaoh
# mail: xiaoh@about.me
# Created Time:  2016-03-21 13:17:40
#############################################

blog=2016-03-21-awesome-python.markdown
root=/home/xingming/gitpro

cd $root/awesome-python
git fetch upstream
git merge upstream/master

cat $root/tools/blogs/awesome-python-header.md > $root/blogs/_posts/$blog
echo '# [Awesome Python](http://www.xiaoh.me/2016/03/21/awesome-python/)' >> $root/blogs/_posts/$blog
cat $root/awesome-python/README.md | tail -n +2 >> $root/blogs/_posts/$blog

cd $root/blogs
badd _posts/$blog

git add _posts/$blog
git commit -m 'update awesome-python blog'
git push

echo 'All work done'
