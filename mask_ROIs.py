import sys
import commands
import os


ROI_loc = '/Users/afranco/TEMP/FALFF_GOFF/ROIS'
roi_names = '/Users/afranco/TEMP/FALFF_GOFF/SCRIPTS/FALFF_GOFF/Hipp_ROIs.txt'

# reading list of ROI names
with open(roi_names) as f:
    lines = f.read().splitlines()


# Goto where ROIs are located
os.chdir(ROI_loc)
os.system('ls')


for roi in lines:
    roi_in = (roi + '.nii.gz')
    roi_out = (roi + '_mask.nii.gz')

    run = ("3dcalc -a " + roi_in + " -expr 'step(a)' -prefix " + roi_out)
    print("command:")
    print(run)
    os.system(run)

#

