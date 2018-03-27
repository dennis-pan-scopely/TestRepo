#! /bin/bash
echo $USERNAME
echo $KEY
#git checkout -b dennis/test
#git push -u origin dennis/test
curl -u $USERNAME --key $KEY -d "{"title":"testTitle","head":"dennis/test1","base":"master","body":"123"}" https://api.github.com/repos/dennis-pan-scopely/TestRepo/pulls

