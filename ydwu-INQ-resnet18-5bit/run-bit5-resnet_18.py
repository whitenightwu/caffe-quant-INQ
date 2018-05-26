import os

#0.5 0.25 0.125 0.0

print "First partition and run"

os.system("sed -i \"s/(count_\*0.7)/(count_\*0.5)/g\" ./src/caffe/blob.cpp")
os.system("make all -j128")
os.system("nohup sh ./examples/INQ/resnet-18/train_resnet18.sh >run1.log 2>&1")

print "Second partition and run"

os.system("sed -i \"s/(count_\*0.5)/(count_\*0.25)/g\" ./src/caffe/blob.cpp")
os.system("make all -j128")

os.system("sed -i \"s/original_ResNet18.caffemodel/resnet18_part1_iter_65000.caffemodel/g\" ./examples/INQ/resnet-18/train_resnet18.sh")
os.system("sed -i \"s/part1/part2/g\" ./examples/INQ/resnet-18/solver.prototxt")
os.system("nohup sh ./examples/INQ/resnet-18/train_resnet18.sh >run2.log 2>&1")

print "Thrid partition and run"

os.system("sed -i \"s/(count_\*0.25)/(count_\*0.125)/g\" ./src/caffe/blob.cpp")
os.system("make all -j128")


os.system("sed -i \"s/resnet_part1_iter_65000.caffemodel/resnet_part2_iter_65000.caffemodel/g\" ./examples/INQ/resnet-18/train_resnet18.sh")
os.system("sed -i \"s/part2/part3/g\" ./examples/INQ/resnet-18/solver.prototxt")
os.system("nohup sh ./examples/INQ/resnet-18/train_resnet18.sh >run3.log 2>&1")


print "Last partition and run"

os.system("sed -i \"s/(count_\*0.125)/(count_\*0.)/g\" ./src/caffe/blob.cpp")
os.system("make all -j128")

os.system("sed -i \"s/resnet_part2_iter_65000.caffemodel/resnet_part3_iter_65000.caffemodel/g\" ./examples/INQ/resnet-18/train_resnet18.sh")
os.system("sed -i \"s/part3/part4/g\" ./examples/INQ/resnet-18/solver.prototxt")
os.system("sed -i \"s/snapshot: 5000/snapshot: 1/g\" ./examples/INQ/resnet-18/solver.prototxt")
os.system("sed -i \"s/max_iter: 65000/max_iter: 1/g\" ./examples/INQ/resnet-18/solver.prototxt")

os.system("nohup sh ./examples/INQ/resnet-18/train_resnet18.sh >run4.log 2>&1")

print "All quantization done and you can enjoy the power-of-two weights using check.py!"
os.system("sed -i \"s/(count_\*0.)/(count_\*0.7)/g\" ./src/caffe/blob.cpp")
os.system("make all -j128")

os.system("sed -i \"s/resnet18_part3_iter_65000.caffemodel/original_ResNet18.caffemodel/g\" ./examples/INQ/resnet-18/train_resnet18.sh")
os.system("sed -i \"s/part4/part1/g\" ./examples/INQ/resnet-18/solver.prototxt")
os.system("sed -i \"s/snapshot: 1/snapshot: 5000/g\" ./examples/INQ/resnet-18/solver.prototxt")
os.system("sed -i \"s/max_iter: 1/max_iter: 65000/g\" ./examples/INQ/resnet-18/solver.prototxt")

