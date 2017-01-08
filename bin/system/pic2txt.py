import Image

color = 'MNHQ$OC?7>!:-..'

def to_html(func):
    html_head = '''
            <html>
              <head>
                <style type="text/css">
                  body {font-family:Monospace; font-size:5px;}
                </style>
              </head>
            <body> '''
    html_tail = '</body></html>'
    def wrapper(img):
        pic_str = func(img)
        pic_str = ''.join(l + ' <br/>' for l in pic_str.splitlines())
        return html_head + pic_str + html_tail
    return wrapper

@to_html
def make_char_img(img):
    pix = img.load()
    pic_str = ''
    import numpy as np
    width, height = np.array(img.size)
    for h in xrange(height):
        pic_str += ''
        for w in xrange(width):
            pic_str += color[int(pix[w, h]) * 14 / 255]
        pic_str += '\n'
    return pic_str

def make_txt_img(img, prefix='', postfix='\n', 
                 leftMargin = 0, rightMargin = 0,
                 bottomMargin = 0, topMargin = 0,):
    pix = img.load()
    pic_str = ''
    import numpy as np
    width, height = np.array(img.size)
    for h in xrange(topMargin, height - bottomMargin):
        pic_str += prefix
        for w in xrange(leftMargin, width - rightMargin):
            pic_str += color[int(pix[w, h]) * 14 / 255]
        pic_str += postfix
    return pic_str
    
def preprocess(img_name,numPixel=100,ratio = 0.75):
    img = Image.open(img_name)

    w, h = img.size
    m = max(img.size)
    delta = m / numPixel
    w, h = int(w / delta), int(h / delta*ratio)
    img = img.resize((w, h))
    img = img.convert('L')
    return img

def save_to_file(filename, pic_str):
    outfile = open(filename, 'w')
    outfile.write(pic_str)
    outfile.close()

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Translate a figure file to character formed figure.')
    parser.add_argument('FigureName', metavar='1', type=str,
                        help='Figure filename for translation')
    parser.add_argument('-n','--numPixel', type=int,
                        help='Number of output pixels')
                        
    parser.add_argument('-l','--leftMargin', type=int, default=0,
                        help='Number of left margin pixels')             
    parser.add_argument('-r','--rightMargin', type=int, default=0,
                        help='Number of left margin pixels')         
    parser.add_argument('-b','--bottomMargin', type=int, default=0,
                        help='Number of bottomMargin pixels')                      
    parser.add_argument('-t','--topMargin', type=int, default=0,
                        help='Number of left margin pixels')   
                        
    args = parser.parse_args()     
    #print args     
    
    filename = args.FigureName   
    img = preprocess(filename,args.numPixel)
    
    filename = filename.split('.')[0]
    prefix = ['', 'print *,\'']
    postfix= ['\n', '\'\n']
    for i, fileType in enumerate(['.txt','.f90']):
      pic_str = make_txt_img(img, prefix=prefix[i], postfix=postfix[i],
                             leftMargin = args.leftMargin,
                             rightMargin = args.rightMargin,
                             bottomMargin = args.bottomMargin,
                             topMargin = args.topMargin)
      open(filename+fileType,'w').writelines(pic_str)
    
    pic_str = make_char_img(img)
    save_to_file(filename+'.html', pic_str)

if __name__ == '__main__':
    main()
