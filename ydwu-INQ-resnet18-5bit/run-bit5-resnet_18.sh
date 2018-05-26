#!/bin/bash
trap "kill 0" INT

rm ./models/resnet-18/resnet18_part* -rf
pre_caffemodel="ResNet-18.caffemodel"
pre_part=0.7

count=1
for p in 0.5 0.25 0.125 0.0
do
    echo "$count partition and run" $p

    sed -i "s/(count_\*$pre_part)/(count_\*$p)/g" ./src/caffe/blob.cpp
    pre_part=$p

    if [ $count -eq 4 ]
    then
	sed -i "s/snapshot: 1000/snapshot: 1/g" ./examples/INQ/resnet-18/solver.prototxt
	sed -i "s/max_iter: 65000/max_iter: 1/g" ./examples/INQ/resnet-18/solver.prototxt
	break
    fi
    
    make all -j128
    nohup sh ./examples/INQ/resnet-18/train_resnet18.sh >run${count}_log.out 2>&1
    
    sed -i "s/$pre_caffemodel/resnet18_part${count}_iter_65000.caffemodel/g" ./examples/INQ/resnet-18/train_resnet18.sh
    pre_caffemodel="resnet18_part${count}_iter_65000.caffemodel"

    let "count_add_1=count+1"
    sed -i "s/part${count}/part${count_add_1}/g" ./examples/INQ/resnet-18/solver.prototxt

    let "count+=1"
done


sed -i "s/snapshot: 1/snapshot: 5000/g" ./examples/INQ/resnet-18/solver.prototxt
sed -i "s/max_iter: 1/max_iter: 65000/g" ./examples/INQ/resnet-18/solver.prototxt
sed -i "s/part4/part1/g" ./examples/INQ/resnet-18/solver.prototxt
sed -i "s/resnet18_part4_iter_15000.caffemodel/ResNet-18.caffemodel/g" ./examples/INQ/resnet-18/train_resnet18.sh
sed -i "s/(count_\*0.0)/(count_\*0.7)/g" ./src/caffe/blob.cpp
