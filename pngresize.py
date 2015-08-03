'''Resize pngs along x-axis maintaining aspect ratio'''
import sys
import os
import glob
from PIL import Image

def err(msg):
    print >> sys.stderr,msg
    sys.exit(1)

usage = '''
python pngresize.py png_dir sizex sizey
'''

#Do not limit y-axis size, only resize y-axis to fix aspect ratio
MAX_Y = 99999

if __name__ == '__main__':
    try:
        png_dir = sys.argv[1]
        sizex = int(sys.argv[2])
        sizey = int(sys.argv[3])

        os.chdir(png_dir)
        pngs = glob.glob("*.png") + glob.glob("*.PNG")

        for png in pngs:
            print "{}:...".format(png),
            pil_png_img = Image.open(png)
            width = pil_png_img.size[0]

            if width > sizex:
                #preserves aspect ratio
                pil_img_copy = Image.Image.copy(pil_png_img)
                pil_png_img.thumbnail((sizex, MAX_Y))
                pil_png_img.save(png)
                print "\r{}:Converted".format(png),

                #if after resizing height of image is still larger than sizey, generated a thumbnail
                if pil_png_img.size[1] > sizey:
                    pil_img_copy.thumbnail((sizex, sizey))
                    pil_img_copy.save(png[:-4] + ".thumbnail.png")
                    pil_img_copy.close()
                    print " + Thumbnail Generated".format(png)
                else:
                    print
            elif pil_png_img.size[1] > sizey:
                pil_png_img.thumbnail((sizex, sizey))
                pil_png_img.save(png[:-4] + ".thumbnail.png")
                print "\r{}:Thumbnail Generated".format(png)
            else:
                print "\r{}:OK ".format(png)

            pil_png_img.close()

    except IndexError:
        err(usage)
    except OSError as e:
        if e.errno == 2:
            err("Whut... dir doesn't exist!")
        raise e