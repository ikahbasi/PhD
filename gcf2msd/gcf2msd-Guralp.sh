ini=/home/ekarkooti/ikahbasi-PhD/TMP/Kaki_gcf2msd.ini
root=/media/ekarkooti/ext4/Kahbasi-PhD/Kaki/raw-gcf-data
for dir in $(find $root -type d)
do
    for input in $(ls ${dir}/*.gcf)
    do
        
        outdir="${input/raw-gcf-data/MSEED}"
        outdir=$(dirname $outdir)
        #echo $outdir
        /home/ekarkooti/Apps/gcf2msd_guralp/gcf2msd ${input} -o:$outdir -i:$ini
    done
done
