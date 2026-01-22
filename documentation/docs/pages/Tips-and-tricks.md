

## Payu cloning access-om3-configs quickly
A small bash function to help one payu clone an access-om3-config.

```bash
function eclone()
{
    if [[ ( $# -eq 0 ) || ( $1 == "--help" ) || ( $1 == "-h" ) ]] ; then
        echo "Usage:   payuexp BRANCH."
        echo "Purpose: clone an access-om3-config and path to the folder on NCI."
        echo "       "
        echo "Mandatory arguments: "
        echo "BRANCH:   branch on om3-configs we'll clone"
        echo "This:"
        echo "payuexp dev-MC_100km_jra_ryf"
        echo "       "
        echo "Becomes:"
        echo "payu clone -b expt -B dev-MC_100km_jra_ryf  https://github.com/ACCESS-NRI/access-om3-configs dev-MC_100km_jra_ryf"
        return 1
    fi
    echo "We are payu cloning branch "$1
    echo ""
    module purge;module use /g/data/vk83/modules;module load payu;module list;cd /g/data/$PROJECT/$USER/access-om3-runs
    payu clone -b expt -B $1 https://github.com/ACCESS-NRI/access-om3-configs $1
    echo ""
    cd $1
    CWD="$(pwd)"
    echo "Experiment folder is: "$CWD
    echo ""
}
```
