#!/usr/bin/env sh

# Update files in doc directory by copying from a working configuration branch.

set -e

branch=1deg_jra55do_ryf
files=(config.yaml nuopc.runconfig nuopc.runseq MOM_input ice_in)

cd "`git rev-parse --show-toplevel`"  # cd to git root
git checkout ${branch}
git pull
commit=$(git rev-parse --short HEAD)
git checkout main
git pull
git checkout ${branch} ${files[*]}

for file in "${files[@]}"
do
    mv ${file} doc
    git restore --staged ${file}
    echo "updated ${file}"
done

# update history in README_doc.md
echo "1. Updated $(date) from branch [${branch}](https://github.com/COSIMA/MOM6-CICE6/tree/${branch}) commit [${commit}](https://github.com/COSIMA/MOM6-CICE6/tree/${commit})" >> doc/README_doc.md
