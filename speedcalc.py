'''
This script helps in determining exact text_speed
'''

from time import sleep
a ={'-':"ABCDEFGHIJ",'|':"1234567890"}
while True:
    for s in '|-':
        with open('feed_text_dev.txt',"w") as t:
            i = " "+a[s]+81*s+" "
            t.write(i)
        sleep(93/6.15)

