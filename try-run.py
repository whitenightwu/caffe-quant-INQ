#bit4-alexnet
#{0.2;0.5;0.8;0.9;0.95;1}
#blob.cpp::{0.8}

import os


print "First partition and run"

os.system("nohup sh ./examples/INQ/alexnet/train_alexnet.sh >try.log 2>&1")
