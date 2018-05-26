#!/bin/bash
trap "kill 0" INT

rm ./models/bvlc_alexnet/alexnet_part* -rf
pre_caffemodel="original.caffemodel"
pre_part=0.7

count=1
for p in 0.9 0.8 0.7 0.5 0.3 0.1 0.0
do
    echo "$count partition and run" $p

    sed -i "s/(count_\*$pre_part)/(count_\*$p)/g" ./src/caffe/blob.cpp
    pre_part=$p

    if [ $count -eq 7 ]
    then
	sed -i "s/snapshot: 3000/snapshot: 1/g" ./examples/INQ/alexnet/solver.prototxt
	sed -i "s/max_iter: 15000/max_iter: 1/g" ./examples/INQ/alexnet/solver.prototxt
	break
    fi
    
    make all -j128
    nohup sh ./examples/INQ/alexnet/train_alexnet.sh >run${count}_log.out 2>&1
    
    sed -i "s/$pre_caffemodel/alexnet_part${count}_iter_15000.caffemodel/g" ./examples/INQ/alexnet/train_alexnet.sh
    pre_caffemodel="alexnet_part${count}_iter_15000.caffemodel"

    let "count_add_1=count+1"
    sed -i "s/part${count}/part${count_add_1}/g" ./examples/INQ/alexnet/solver.prototxt

    let "count+=1"
done


sed -i "s/snapshot: 1/snapshot: 3000/g" ./examples/INQ/alexnet/solver.prototxt
sed -i "s/max_iter: 1/max_iter: 15000/g" ./examples/INQ/alexnet/solver.prototxt
sed -i "s/part7/part1/g" ./examples/INQ/alexnet/solver.prototxt
sed -i "s/alexnet_part7_iter_15000.caffemodel/original.caffemodel/g" ./examples/INQ/alexnet/train_alexnet.sh
sed -i "s/(count_\*0.0)/(count_\*0.7)/g" ./src/caffe/blob.cpp
