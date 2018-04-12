"""
# Note: make sure to install PIL after your regular python package is installed
# Program: A set of image modification commands
# Command set:
#  1)   file command, use -f as the secnd cli argument
#       rotate a named image n times at x degrees
#       <program name> -f <file name> <(int)number of rotations> <(int)degrees per rotation>
#  2)   select command, use -sel as second cli argument, selects file from file explorer box
#       <program name> -sel <(int)number of rotations> <(int)degrees per rotation>
#  3)   directory command, use -d as the secnd cli argument
#       similar to command 1 except it looks through a directory of and
#       modifies any with a .jpg, .bmp, .png, or .gif file extension
#       <program name> -d <directory of images> <(int)number of rotations> <(int)degrees per rotation>
#  4)   pixel command, use -pix as the secnd cli argument
#       modifies some pixels in a named image at the x and y coordinates
#       <program name> -pix <-x/-y/-f> <x val/y val/file name> <-x/-y/-f>
#               <x val/y val/file name> <-x/-y/-f> <x val/y val/file name>
#  5)   contrast command, use -cont as second cli argument, creates copies of file with
#       a few different sets of color contrasts applied to it.
#       <program name> -cont
"""
# rotate images lib, must install with pip
from PIL import Image, ImageFilter
import sys # sys.argv
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os
from time import gmtime, strftime

def change_contrast_multi(f_name, steps):
    try:
        im = Image.open(f_name)
    except:
        print(f_name)
        exit(1)
    width, height = im.size
    canvas = Image.new('RGB', (width * len(steps), height))
    for n, level in enumerate(steps):
        img_filtered = change_contrast(im, level)
        canvas.paste(img_filtered, (width * n, 0))
    return canvas

def change_contrast(im, level):
    factor = (259 * (level + 255)) / (255 * (259 - level))
    def contrast(c):
        value = 128 + factor * (c - 128)
        return max(0, min(255, value))
    return im.point(contrast)

def change_contrast_of_file(f_name, level):
    im = Image.open(f_name)
    factor = (259 * (level + 255)) / (255 * (259 - level))
    def contrast(c):
        value = 128 + factor * (c - 128)
        return max(0, min(255, value))
    return im.point(contrast)


def change_pixels(f_name, x, y):
    #old_f_name = f_name
    #new_f_name = new_f_name.split("\\")
    #new_f_name = f_name + "_x_" + str(x) + "_y_" + str(y) + ".jpg"

    im = Image.open(f_name)
    pixelMap = im.load()

    img = Image.new( im.mode, im.size)
    pixelsNew = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if x in pixelMap[i,j]:
                pixelMap[i,j] = (0,0,0,255)
            else:
                pixelsNew[i,j] = pixelMap[i,j]
    img.show()

def run_file_im_rotate(f_name_base, degrees, str_time):
    old_name = f_name_base
    old_name = old_name.split("\\")
    old_name = old_name[len(old_name)-1]

    file_path = f_name_base + "_" + str_time
    new_f_name = f_name_base + "_rotated_" + str(degrees) + "_deg" + ".jpg"
    im_type = ""

    new_f_name = new_f_name.split("\\")
    f_name = new_f_name[len(new_f_name)-1] # gets the file_name only
    try:
        if not os.path.exists(file_path):
            os.makedirs(file_path)
    except:
        print("Error: could not make directory")

    try:
        im1 = Image.open(f_name_base)
        f_name = f_name[:len(f_name)-4]
    except:
        try:
            a = f_name_base + ".jpg"
            im1 = Image.open(a)
            im_type = a.format
        except:
            try:
                a = f_name_base + ".png"
                im1 = Image.open(a)
                im_type = a.format
            except:
                try:
                    a = f_name_base + ".bmp"
                    im1 = Image.open(a)
                    im_type = a.format
                except:
                    try:
                        a = f_name_base + ".gif"
                        im1 = Image.open(a)
                        im_type = a.format
                    except:
                        print("Error: incompatible file extension.\nUse the following file extensions: .bmp, .jpg, .png, .gif.")

	# rotate 60 degrees counter-clockwise
    im2 = im1.rotate(degrees)
	# brings up the modified image in a viewer, simply saves the image as
	# a bitmap to a temporary file and calls viewer associated with .bmp
	# make certain you have an image viewer associated with this file type
    # im2.show()
	# save the rotated image as d.gif to the working folder
	# you can save in several different image formats, try d.jpg or d.png
	# PIL is pretty powerful stuff and figures it out from the extension
    try:
        f_name = f_name.split(".")
        f_name = f_name[0]
        im2.save(file_path + "\\" + f_name + str_time + ".jpg")
##        for i in range(len(a)): # create contrasting image
##            new_dir = f_name[:len(f_name)-4]
##            new_f_name = f_name.split("\\")
##            new_f_name = new_f_name[len(new_f_name)-1]
##            new_f_name = new_f_name[:len(new_f_name)-4]
##            print(new_f_name)
##            im = change_contrast_of_file(f_name, a[i])
##            try:
##                im.save(new_dir +  "\\" + new_f_name + "_" + str(i) + ".jpg")
##            except:
##                print("Error: Could not save new file!!!")
    except:
        try:
            im2.save(file_path + "\\" + f_name[:len(f_name)-3])
            a = file_path + "\\" + f_name[:len(f_name)-3]
##            for i in range(len(a)): # create contrasting image
##                new_dir = f_name[:len(f_name)-4]
##                new_f_name = f_name.split("\\")
##                new_f_name = new_f_name[len(new_f_name)-1]
##                new_f_name = new_f_name[:len(new_f_name)-4]
##                print(new_f_name)
##                im = change_contrast_of_file(f_name, a[i])
##                try:
##                    im.save(new_dir +  "\\" + new_f_name + "_" + str(i) + ".jpg")
##                except:
##                    print("Error: Could not save new file!!!")
        except:
            print("Error: Could not save image!")
            exit(1)

def main():
    if(len(sys.argv) != 5 and
       len(sys.argv) != 4 and
       len(sys.argv) != 8 and
       len(sys.argv) != 3):
        print("Usage: <program name> -f <file name> <(int)number of rotations> <(int)degrees per rotation>")
        print("OR")
        print("Usage: <program name> -d <directory of images> <(int)number of rotations> <(int)degrees per rotation>")
        print("OR")
        print("Usage: <program name> -sel <(int)number of rotations> <(int)degrees per rotation>")
        print("OR")
        print("Usage: <program name> -cont <file name>")
        err_msg = "Usage: <program name> -pix <-x/-y/-f> <x val/y val/file name> <-x/-y/-f> "
        err_msg += "<x val/y val/file name> <-x/-y/-f> <x val/y val/file name>"
        print(err_msg)
        exit(1)

    str_time = strftime("%Y_%m_%d_%H_%M_%S", gmtime()) # get timestamp for the directoires

    if(sys.argv[1] == '-f'): # for running on a single file
        f_name = sys.argv[2]
        num_rotations = int(sys.argv[3])
        deg_per_rotation = int(sys.argv[4])
        if(deg_per_rotation * num_rotations > 360):
            deg_per_rotation = 360 / num_rotations # in case you ploebs can't do math
        try:
            for i in range(num_rotations):
                run_file_im_rotate(f_name, i * deg_per_rotation, str_time)
        except:
            print("Error: You broke me.")
            exit(1)
    elif(sys.argv[1] == '-d'): # runs on every image in the specified directory
        directory = sys.argv[2]
        try:
            for file in os.listdir(directory):
                if( (file.endswith(".jpg")) or
                    (file.endswith(".png")) or
                    (file.endswith(".gif")) or
                    (file.endswith(".bmp"))):
                    file = os.path.join(directory, file)
                    file = file[:len(file)-4]
                    try:
                        f_name = file
                        num_rotations = int(sys.argv[3])
                        deg_per_rotation = int(sys.argv[4])
                        if(deg_per_rotation * num_rotations > 360):
                            deg_per_rotation = 360 / num_rotations # in case you ploebs can't do math

                        try:
                            for i in range(num_rotations):
                                run_file_im_rotate(f_name, i * deg_per_rotation, str_time)
                        except:
                            print("Error: You broke me.")
                    except:
                        print("Error: You broke me.")
        except:
            print("Error: invalid directory name")
    elif(sys.argv[1] == '-sel'): # allows one to select a file to modify from file explorer
        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        f_name = filename[:len(filename)-4]
        new_f_name = f_name.split("/")
        f_name = str()
        for i in range(len(new_f_name)):
            f_name += str(new_f_name[i])
            f_name += ("\\")
        f_name = f_name[:len(f_name)-1]

        num_rotations = int(sys.argv[2])
        deg_per_rotation = int(sys.argv[3])
        if(deg_per_rotation * num_rotations > 360):
            deg_per_rotation = 360 / num_rotations # in case you ploebs can't do math
        try:
            for i in range(num_rotations):
                run_file_im_rotate(f_name, i * deg_per_rotation, str_time)
        except:
            print("Error: You broke me.")
    elif(sys.argv[1] == '-pix'): # modifies pixels in a specific image
        if(len(sys.argv) == 8):
            x = -1
            y = -1
            i = 0
            while i < len(sys.argv):
                if(i > 1):
                    if(sys.argv[i] == '-f'):
                        f_name = sys.argv[i+1]
                        i += 1
                    elif(sys.argv[i] == '-x'):
                        x = int(sys.argv[i+1])
                        i += 1
                    elif(sys.argv[i] == '-y'):
                        y = int(sys.argv[i+1])
                        i += 1
                    else:
                        print("IDK what to do with this nonsense!!!")
                i += 1 # always increment
            try:
                change_pixels(f_name, x, y)
            except:
                print("Error: Could not execute pixel change!")
                exit(1)
        else:
            err_msg = "Usage: <program name> -pix <-x/-y/-f> <x val/y val/file name> <-x/-y/-f> "
            err_msg += "<x val/y val/file name> <-x/-y/-f> <x val/y val/file name>"
            print(err_msg)
            exit(1)
    elif(sys.argv[1] == '-cont'): # provides several different contrasts of a specified image
        f_name = sys.argv[2]
        a = [-400, -300, -200, -100, 100, 200, 300, 400]

        new_dir = f_name[:len(f_name)-4]
        new_f_name = f_name.split("\\")
        new_f_name = new_f_name[len(new_f_name)-1]
        new_f_name = new_f_name[:len(new_f_name)-4]
        print(new_f_name)
        try:
            if not os.path.exists(new_dir):
                os.makedirs(new_dir)
        except:
            print("Error: could not make directory")
        for i in range(len(a)):
            im = change_contrast_of_file(f_name, a[i])
            try:
                im.save(new_dir +  "\\" + new_f_name + str(i) + ".jpg")
            except:
                print("Error: Could not save new file!!!")
    else:
        print("Usage: <program name> -f <file name> <(int)number of rotations> <(int)degrees per rotation>")
        print("OR")
        print("Usage: <program name> -d <directory of images> <(int)number of rotations> <(int)degrees per rotation>")
        print("OR")
        print("Usage: <program name> -sel <(int)number of rotations> <(int)degrees per rotation>")
        print("OR")
        print("Usage: <program name> -cont <file name>")
        err_msg = "Usage: <program name> -pix <-x/-y/-f> <x val/y val/file name> <-x/-y/-f> "
        err_msg += "<x val/y val/file name> <-x/-y/-f> <x val/y val/file name>"
        print(err_msg)
        exit(1)
    print()
    print("Success!!!!")

if __name__ == '__main__':
    main()
