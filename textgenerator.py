import sys
from extrafunctions import abs_path
with open(abs_path('obstexttrial.txt'),'w') as txtfile:
    for _ in range(int(sys.argv[1])):
        txtfile.write(sys.argv[2])