
from html2image import Html2Image
from extrafunctions import *
class Strip:
    def __init__(self,width,height,savefile='strip.png',html_file=None,css_file=None) -> None:
        self.width = width
        self.height = height
        self.savefile = savefile
        self.html = self.getDefaultHTML() if html_file == None else fileToString(html_file)
        self.css = self.getDefaultCSS() if css_file == None else fileToString(css_file)
        
        self.createGraphics()
            
    
    def createGraphics(self):
        image = Html2Image(size=(self.width,self.height))
        image.screenshot(html_str=self.html,css_str=self.css,save_as=self.savefile)
    def getDefaultHTML(self):
        default_html = """
        <div class="rectangle"></div>
        """
        return(default_html)

    def getDefaultCSS(self):
        default_css = """
        html,body{
            padding: 0;
            margin: 0;
        }

        .rectangle{
            position: absolute;
            width: WIDTHpx;
            height: HEIGHTpx;
            background: radial-gradient(50% 50% at 50% 50%, #5E0080 28.65%, #000000 100%);
            opacity: 0.8;
            box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
        }
        """
        default_css = default_css.replace('WIDTH',str(self.width))
        default_css = default_css.replace('HEIGHT',str(self.height))
        
        return(default_css)
class Circle:
    def __init__(self,width,height,savefile='circle.png',html_file=None,css_file=None) -> None:
        self.width = width
        self.height = height
        self.savefile = savefile
        self.html = self.getDefaultHTML() if html_file == None else fileToString(html_file)
        self.css = self.getDefaultCSS() if css_file == None else fileToString(css_file)
        
        self.createGraphics()
            
    
    def createGraphics(self):
        image = Html2Image(size=(self.width,self.height))
        image.screenshot(html_str=self.html,css_str=self.css,save_as=self.savefile)
    def getDefaultHTML(self):
        default_html = """
        <div class="circle"></div>
        """
        return(default_html)

    def getDefaultCSS(self):
        default_css = """
        html,body{
            padding: 0;
            margin: 0;
        }

        .circle{
            position: absolute;
            width: WIDTHpx;
            height: HEIGHTpx;
            border-radius: 100%;

            background: #FFFFFF;
            box-shadow: inset -4px 4px 4px 1px rgba(0, 0, 0, 0.8);

        }
        """
        default_css = default_css.replace('WIDTH',str(self.width))
        default_css = default_css.replace('HEIGHT',str(self.height))
        
        return(default_css)
def main():
    c =Circle(50,50)
    s = Strip(1208,30)

if __name__ == '__main__':
    main()
