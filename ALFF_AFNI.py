import sys
import commands
import os


os.system('ls')


base_folder = '/Users/alexandre.franco/TEMP/DON'
subj = 'SZ513c'
mask = '/usr/local/fsl/data/standard/MNI152lin_T1_2mm_brain_mask.nii.gz'
filename = 'proc_nosmooth_norm'
ROI = '/Users/alexandre.franco/TEMP/DON/Group1_thresh_zstat0010_LeftPost_mask.nii.gz'
output = '/Users/alexandre.franco/TEMP/DON/ALFF_Group1_RightPost.txt'

# go to base folder
os.chdir(base_folder)
os.system('ls')
os.chdir(subj)
os.system('ls')



# run afni 3drsfc
fbot = '0.01'
ftop = '0.1'
run = "3dRSFC " + "-mask " + mask + " -band " + fbot + " " + ftop + " -prefix " + filename + " -input " + filename + ".nii.gz"
print("command:")
print(run)

#os.system(run)

# now extract the score inside the ROI
# get ALFF
run = "3dROIstats  -quiet -mask " + mask + " " + "proc_nosmooth_norm_ALFF+tlrc.HEAD > " + output
print("command:")
print(run)
os.system(run)
#3dROIstats -mask mask+orig. 'func_slim+orig[1,3,5]'



exit()
