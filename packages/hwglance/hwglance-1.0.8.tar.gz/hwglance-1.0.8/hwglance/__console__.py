# -*- coding: utf-8 -*-
from hwglance import HWmon
import sys, getopt

fnt = HWmon.pClr

def main():
    argv = sys.argv[1:]
    refresh = 0.5
    doWave = True
    changeColor = True
    useServices = True
    helpmsg = f"""
{fnt.BM}
{fnt.b}hwmon {fnt.G}-r 0.5 -w True/False -c True/False -s True/False{fnt.BM}
{fnt.wh}-r --refresh     {fnt.G}INT or FLOAT       {fnt.wh}# Refresh time{fnt.E}{fnt.BM}
{fnt.wh}-w --wave        {fnt.G}BOOLEAN            {fnt.wh}# Enable or disable wave moving at the bottom{fnt.E}{fnt.BM}
{fnt.wh}-c --coloring    {fnt.G}BOOLEAN            {fnt.wh}# Enable or disable coloring cycle{fnt.E}{fnt.BM}
{fnt.wh}-s --services    {fnt.G}BOOLEAN            {fnt.wh}# Enable or disable IP Services{fnt.E}
"""
    try:
       opts, args = getopt.getopt(argv,"hr:w:c:s",["refresh=","wave=","coloring=", "services="])
    except getopt.GetoptError:
       print(helpmsg)
       sys.exit(2)
    for opt, arg in opts:
        if len(args) == 1:
            message = args[0]
        if opt == '-h':
            print(helpmsg)
            sys.exit(420)
        elif opt in ("-r", "--refresh"):
            refresh = arg
        elif opt in ("-w", "--wave"):
            doWave = arg
        elif opt in ("-c", "--coloring"):
            changeColor = arg
        elif opt in ("-s", "--services"):
            useServices = arg
         

    HWmon(refresh=refresh, doWave=doWave, changeColor=changeColor, useServices=useServices)

if __name__ == "__main__":
   main()