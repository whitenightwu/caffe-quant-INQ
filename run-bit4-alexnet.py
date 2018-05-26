
#paper::: 
#resnet-4bit{0.3;0.5;0.8;0.9;0.95;1}
#resnet-5bit{0.5;0.75;0.875;1}
#alexnet-5bit{0.3;0.6;0.8;1}


#blob.cpp::{0.8,}
#alexnet-bit4{0.2;0.4;0.6;0.8;0.9;1}

import os

#################################
print "First partition and run"
os.system("sed -i \"s/(count_\*0.8)/(count_\*0.9)/g\" ./src/caffe/blob.cpp")
os.system("make all -j128")

#os.system("nohup sh ./examples/INQ/alexnet/train_alexnet.sh >run1.log 2>&1")

#################################
print "Second partition and run"

os.system("sed -i \"s/(count_\*0.9)/(count_\*0.8)/g\" ./src/caffe/blob.cpp")
os.system("make all -j128")

os.system("sed -i \"s/original.caffemodel/alexnet_part1_iter_63000.caffemodel/g\" ./examples/INQ/alexnet/train_alexnet.sh")
os.system("sed -i \"s/part1/part2/g\" ./examples/INQ/alexnet/solver.prototxt")

#os.system("nohup sh ./examples/INQ/alexnet/train_alexnet.sh >run2.log 2>&1")

#################################
print "Thrid partition and run"

os.system("sed -i \"s/(count_\*0.8)/(count_\*0.4)/g\" ./src/caffe/blob.cpp")
os.system("make all -j128")

os.system("sed -i \"s/alexnet_part1_iter_63000.caffemodel/alexnet_part2_iter_63000.caffemodel/g\" ./examples/INQ/alexnet/train_alexnet.sh")
os.system("sed -i \"s/part2/part3/g\" ./examples/INQ/alexnet/solver.prototxt")
#os.system("nohup sh ./examples/INQ/alexnet/train_alexnet.sh >run3.log 2>&1")

#################################
print "Forth partition and run"

os.system("sed -i \"s/(count_\*0.4)/(count_\*0.3)/g\" ./src/caffe/blob.cpp")
os.system("make all -j128")

os.system("sed -i \"s/alexnet_part2_iter_63000.caffemodel/alexnet_part3_iter_63000.caffemodel/g\" ./examples/INQ/alexnet/train_alexnet.sh")
os.system("sed -i \"s/part3/part4/g\" ./examples/INQ/alexnet/solver.prototxt")
#os.system("nohup sh ./examples/INQ/alexnet/train_alexnet.sh >run4.log 2>&1")

#################################
print "Fifth partition and run"

os.system("sed -i \"s/(count_\*0.3)/(count_\*0.2)/g\" ./src/caffe/blob.cpp")
os.system("make all -j128")

os.system("sed -i \"s/alexnet_part3_iter_63000.caffemodel/alexnet_part4_iter_63000.caffemodel/g\" ./examples/INQ/alexnet/train_alexnet.sh")
os.system("sed -i \"s/part4/part5/g\" ./examples/INQ/alexnet/solver.prototxt")
#os.system("nohup sh ./examples/INQ/alexnet/train_alexnet.sh >run5.log 2>&1")


#################################
print "Last partition and run"

os.system("sed -i \"s/(count_\*0.2)/(count_\*0.)/g\" ./src/caffe/blob.cpp")
os.system("make all -j128")
os.system("sed -i \"s/alexnet_part4_iter_63000.caffemodel/alexnet_part5_iter_63000.caffemodel/g\" ./examples/INQ/alexnet/train_alexnet.sh")
os.system("sed -i \"s/part5/part6/g\" ./examples/INQ/alexnet/solver.prototxt")
os.system("sed -i \"s/snapshot: 3000/snapshot: 1/g\" ./examples/INQ/alexnet/solver.prototxt")
os.system("sed -i \"s/max_iter: 63000/max_iter: 1/g\" ./examples/INQ/alexnet/solver.prototxt")
os.system("nohup sh ./examples/INQ/alexnet/train_alexnet.sh >run6.log 2>&1")


#################################OK
print "All quantization done and you can enjoy the power-of-two weights using check.py!"

os.system("sed -i \"s/(count_\*0.)/(count_\*0.8)/g\" ./src/caffe/blob.cpp")
os.system("make all -j128")
os.system("sed -i \"s/alexnet_part5_iter_63000.caffemodel/original.caffemodel/g\" ./examples/INQ/alexnet/train_alexnet.sh")
os.system("sed -i \"s/part6/part1/g\" ./examples/INQ/alexnet/solver.prototxt")
os.system("sed -i \"s/snapshot: 1/snapshot: 3000/g\" ./examples/INQ/alexnet/solver.prototxt")
os.system("sed -i \"s/max_iter: 1/max_iter: 63000/g\" ./examples/INQ/alexnet/solver.prototxt")
