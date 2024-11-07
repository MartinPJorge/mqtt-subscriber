#!/bin/bash

# ./correct-all.sh path-to-entregas-dir

entregas=$1 # path to DIR with ONLY ZIPs of entregas

# Create CSV with corrections
echo "student,grupo,lectura,maxtemp,reqtype,subsqos,pubport,subport,nummetricas,pubacktopic,numalerts,qosalerts,total"
> notas.csv


# Put there just the files avoiding folder recursion
mkdir /tmp/clean-entregas



function add_bc {
    echo "scale=2; $1 + $2" | bc
}

### for entrega in `ls $entregas`; do
###     # UNZIP submited LAB
###     out_zip=/tmp/${entrega::-4}
###     unzip $entregas/$entrega -d $out_zip 
### 
###     # Create correction DIR
###     clean_out=/tmp/clean-entregas/${entrega::-4}
###     mkdir $clean_out
### 
###     # Copy the JSONs, PCAPNG and LOGs
###     for ext in `echo json pcapng log jpeg png`; do
###         for file in `find $out_zip -name *$ext`; do
###             # Get filename: https://stackoverflow.com/a/32372307
###             fname=`echo "$file" | sed "s/.*\///"`
###             cp $file $clean_out/$fname
###         done
###     done
### 
###     # Copy the vitals signs dataset
###     cp Human_vital_signs_R.csv $clean_out
### done



# Correct each submission, one by one
for submission in `ls /tmp/clean-entregas`; do
    X=${submission:10:2} # get group number X
    group_dir="/tmp/clean-entregas/"$submission

    total=0

    # Print name
    echo ============
    echo = GRUPO $X =
    echo ============



    # Correct the reading 
    lectura=`python3 correct_lectura.py $X $group_dir/respuestas-$X.json`
    echo -e "\tlectura: $lectura"
    total=`add_bc $total $lectura`



    # Correct multiple topics
    publishes=`python3 correct_publishes.py $X $group_dir/publishes-grupo$X.pcapng $group_dir/respuestas-$X.json`
    echo -e "\tpublishes: $publishes"
    total=`add_bc $total $publishes`



    # Correct subscribe temperature
    subs_temp=`python3 correct_temp_subs.py $X $group_dir/subs-temp-grupo$X.pcapng $group_dir/respuestas-$X.json`
    questions=( "reqtype" "subsqos" "pubport" "subport" )
    subs_temp_all=""
    i=0
    for subsi in `echo $subs_temp`; do
        echo -e "\t${questions[i]}: $subsi"
        total=`add_bc $total $subsi`
        subs_temp_all="$subs_temp_all$subsi,"
        i=$(( i + 1 ))
    done


    # Correct subscribe multiple topics
    subs_wildcard=`python3 correct_wildcard.py $X $group_dir/subs-wildcard-grupo$X.pcapng $group_dir/respuestas-$X.json`
    questions=( "nummetricas" "pubacktopic" )
    subs_wildcard_all=""
    i=0
    for subsi in `echo $subs_wildcard`; do
        echo -e "\t${questions[i]}: $subsi"
        total=`add_bc $total $subsi`
        subs_wildcard_all="$subs_wildcard_all$susbi,"
        i=$(( i + 1 ))
    done


    # Correct subscribe multiple topics
    subs_alert=`python3 correct_alert.py $X $group_dir/alerts-grupo$X.pcapng $group_dir/respuestas-$X.json`
    questions=( "nummetricas" "pubacktopic" )
    subs_alert_all=""
    i=0
    for subsi in `echo $subs_alert`; do
        echo -e "\t${questions[i]}: $subsi"
        total=`add_bc $total $subsi`
        subs_alert_all="$subs_alert_all$subsi,"
        i=$(( i + 1 ))
    done


    # Output final mark
    for student in `grep alumna $group_dir/respuestas-$X.json | cut -d'"' -f4 | sed 's/ /_/g'`; do
        echo $student,$X,$lectura,$publishes,$subs_temp_all$subs_wildcardall$subs_alert_all$total >> notas.csv
    done
done


