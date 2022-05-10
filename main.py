from ticker import Ticker
def main():
    t =Ticker('feed_text_dev.txt','feed_img_dev.png')
    t.connect()
    t.createGUI()
if __name__ == '__main__':
    main()