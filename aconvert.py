'''Use ansilove to convert ansi files into pngs
Usage: python aconvert.py dir
'''
import sys
import subprocess
import os
import glob

def err(msg):
    print >> sys.stderr,msg
    sys.exit(1)

formats = [".ans", ".pcb", ".bin", ".adf", ".idf", ".tnd",'.xb']
if __name__ == '__main__':

    try:
        ansi_dir = sys.argv[1]
        os.chdir(ansi_dir)
        compatible_files = []
        for format in formats:
            compatible_files.extend(glob.glob("./*{}".format(format)))
            compatible_files.extend(glob.glob("./*{}".format(format.upper())))

        existing_pngs = glob.glob("./*.png")

        if not os.path.exists('pngs'):
            os.mkdir('pngs')

        for ansif in compatible_files:
            try:
                subprocess.call(["ansilove", ansif])
            except OSError as e:
                if e.errno == 2:
                    err("You need ansilove installed!")
                raise e

        new_pngs = set(glob.glob("./*.png")) - set(existing_pngs)
        for new_png in new_pngs:
            os.rename(new_png, "pngs/{}".format(new_png))
        print "ENJOY!"

    except IndexError:
        err("~~~~~~~ No ansi dir?!")
    except OSError as e:
        if e.errno == 2:
            err("^_^ Dir doesn't exist X_X")
        raise e




