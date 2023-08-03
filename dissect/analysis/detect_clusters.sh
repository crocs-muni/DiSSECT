#!/bin/bash

compute_traits() {
    compute_bitlengths
    TRAITS_INIT=("${TRAITS[@]}")
    for TRAIT in "${TRAITS_INIT[@]}"
    do
        TRAITS=( $TRAIT )
        compute_bitlengths
    done
}

compute_bitlengths() {
    BITLEN="256"
    run_outliers
    BITLEN="224"
    run_outliers
    BITLEN="192"
    run_outliers
    BITLEN="160"
    run_outliers
}

run_outliers() {
    if [ "${#TRAITS[@]}" = "1" ]
    then
        FNAME="${NAME}_${BITLEN}_${TRAITS[0]}"
    else
        FNAME="${NAME}_${BITLEN}"
    fi
    echo "Computing ${FNAME}"

    for TRAIT in "${TRAITS[@]}"
    do
        if [ -z "${CATEGORY}" ]
        then
            sage --python feature_builder.py --trait $TRAIT --bits $BITLEN --source 'https://dissect.crocs.fi.muni.cz/' --output out.csv --input out.csv --keep-category
        else
            sage --python feature_builder.py --trait $TRAIT --bits $BITLEN --category ${CATEGORY} --source 'https://dissect.crocs.fi.muni.cz/' --output out.csv --input out.csv --keep-category
        fi
    done
    sage --python feature_clusters.py out.csv clusters.csv
    mv out.csv cluster_results/${FNAME}.csv
    mv clusters.csv cluster_results/${FNAME}_clusters.csv
}

NAME="brainpool"
TRAITS=( "a02" "a03" "a05" "a06" "a07" "a08" "a12" "a22" "a23" "a24" "a25" "a28" "a29" "i13" "i15" )
CATEGORY="random brainpool_sim"
compute_traits
