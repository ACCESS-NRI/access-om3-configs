set -x
cd /home/561/cyb561/repos/access-om3-configs/documentation/docs/assets/experiments
mkdir -p MC_25km_jra_iaf-1.0-beta-5165c0f8
mkdir -p MC_25km_jra_iaf-1.0-beta-gm1-d968c801
mkdir -p MC_25km_jra_iaf-1.0-beta-gm2-5dc49da6
mkdir -p MC_25km_jra_iaf-1.0-beta-gm3-da330542
mkdir -p MC_25km_jra_iaf-1.0-beta-gm4-9fd08880
mkdir -p MC_25km_jra_iaf-1.0-beta-gm5-9b5dbfa9

src=/g/data/tm70/cyb561/access-om3-paper-1/notebooks/
dest=/home/561/cyb561/repos/access-om3-configs/documentation/docs/assets/experiments/


cp ${src}mkfigs_output_MC_25km_jra_iaf-1.0-beta-5165c0f8/mkmd/*.png      ${dest}MC_25km_jra_iaf-1.0-beta-5165c0f8
cp ${src}mkfigs_output_MC_25km_jra_iaf-1.0-beta-gm1-d968c801/mkmd/*.png  ${dest}MC_25km_jra_iaf-1.0-beta-gm1-d968c801
cp ${src}mkfigs_output_MC_25km_jra_iaf-1.0-beta-gm2-5dc49da6/mkmd/*.png  ${dest}MC_25km_jra_iaf-1.0-beta-gm2-5dc49da6
cp ${src}mkfigs_output_MC_25km_jra_iaf-1.0-beta-gm3-da330542/mkmd/*.png  ${dest}MC_25km_jra_iaf-1.0-beta-gm3-da330542
cp ${src}mkfigs_output_MC_25km_jra_iaf-1.0-beta-gm4-9fd08880/mkmd/*.png  ${dest}MC_25km_jra_iaf-1.0-beta-gm4-9fd08880
cp ${src}mkfigs_output_MC_25km_jra_iaf-1.0-beta-gm5-9b5dbfa9/mkmd/*.png  ${dest}MC_25km_jra_iaf-1.0-beta-gm5-9b5dbfa9

cd /home/561/cyb561/repos/access-om3-configs/documentation/docs/pages/experiments
mkdir -p MC_25km_jra_iaf-1.0-beta-5165c0f8
mkdir -p MC_25km_jra_iaf-1.0-beta-gm1-d968c801
mkdir -p MC_25km_jra_iaf-1.0-beta-gm2-5dc49da6
mkdir -p MC_25km_jra_iaf-1.0-beta-gm3-da330542
mkdir -p MC_25km_jra_iaf-1.0-beta-gm4-9fd08880
mkdir -p MC_25km_jra_iaf-1.0-beta-gm5-9b5dbfa9


dest=/home/561/cyb561/repos/access-om3-configs/documentation/docs/pages/experiments/
cp ${src}mkfigs_output_MC_25km_jra_iaf-1.0-beta-5165c0f8/mkmd/*.md ${dest}MC_25km_jra_iaf-1.0-beta-5165c0f8/
cp ${src}mkfigs_output_MC_25km_jra_iaf-1.0-beta-gm1-d968c801/mkmd/*.md  ${dest}MC_25km_jra_iaf-1.0-beta-gm1-d968c801/
cp ${src}mkfigs_output_MC_25km_jra_iaf-1.0-beta-gm2-5dc49da6/mkmd/*.md  ${dest}MC_25km_jra_iaf-1.0-beta-gm2-5dc49da6/
cp ${src}mkfigs_output_MC_25km_jra_iaf-1.0-beta-gm3-da330542/mkmd/*.md  ${dest}MC_25km_jra_iaf-1.0-beta-gm3-da330542/
cp ${src}mkfigs_output_MC_25km_jra_iaf-1.0-beta-gm4-9fd08880/mkmd/*.md  ${dest}MC_25km_jra_iaf-1.0-beta-gm4-9fd08880/
cp ${src}mkfigs_output_MC_25km_jra_iaf-1.0-beta-gm5-9b5dbfa9/mkmd/*.md  ${dest}MC_25km_jra_iaf-1.0-beta-gm5-9b5dbfa9/

