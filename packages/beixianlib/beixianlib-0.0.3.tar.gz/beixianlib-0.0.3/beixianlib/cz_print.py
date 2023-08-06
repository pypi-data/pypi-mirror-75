from time import *
import sys


def cz_print(text, cz):
    sys.stdout.write("\r " + "" * 60 + "\r")
    sys.stdout.flush()
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        sleep(cz)