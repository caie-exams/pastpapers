#!/bin/sh
set -e

SIZE_LIMIT=2040109466

function git_push(){
    git add $*
    git commit -m "commit in group size of $SIZE_LIMIT" -a
    git push "${remote_repo}" HEAD:${GITHUB_REF_NAME} --verbose
}


git config --local user.email "41898282+github-actions[bot]@users.noreply.github.com"
git config --local user.name "github-actions[bot]"
remote_repo="https://${GITHUB_ACTOR}:${repo-token}@github.com/${GITHUB_REPOSITORY}.git"
git config --local --add safe.directory .


file_list=$(git status -u | grep -P "^\t" | xargs wc -c | sed '$d' | awk '{$1=$1};1')
submit_list=""
submit_size=0

while [ "$file_list" != "" ];
do
    # take each line and add to another list
    
    newline=${file_list%%$'\n'*}
    submit_size=$(echo "$submit_size  + ${newline% *}" | bc -l)
    
    if [ $submit_size -ge $SIZE_LIMIT ];
        then
            git_push $submit_list

            submit_size=0
            submit_list=""
        else
            submit_list+="${newline#* } " 
            file_list=$(echo "$file_list" | sed '1d')
    fi
done


if [ "$submit_list" != "" ];
    then
        git_push .
fi

