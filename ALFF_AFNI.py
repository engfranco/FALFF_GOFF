import sys
import commands
import os
import numpy as np
import csv



base_folder = '/Users/afranco/TEMP/FALFF_GOFF'
mask = '/usr/local/fsl/data/standard/MNI152lin_T1_2mm_brain_mask.nii.gz'
filename = 'proc_nosmooth_norm'

ROI_loc = '/Users/afranco/TEMP/FALFF_GOFF/ROIS/'
roi_names_file = '/Users/afranco/TEMP/FALFF_GOFF/SCRIPTS/FALFF_GOFF/Hipp_ROIs.txt'
output_folder = '/Users/afranco/TEMP/FALFF_GOFF/output/'
output_temp = output_folder + "temp.txt"

subj_list_file = '/Users/afranco/TEMP/FALFF_GOFF/SCRIPTS/FALFF_GOFF/subj_list_test.txt'

# Filters for F/ALFF
fbot = '0.01'
ftop = '0.1'


# reading list of ROI names
with open(roi_names_file) as f:
    ROI_names = f.read().splitlines()

# Read the list of subj names
with open(subj_list_file) as f:
    Subj_names = f.read().splitlines()

# Creating the final output matrix
#final_output = np.strarray((2, 20))
final_output = np.array(range(40), dtype='a50').reshape(20,2)
final_output[:] = 'aaaaa1'
final_output[0][0] = "HELLO"
vals = np.array(ROI_names)
print(final_output)


for ii in range(0,19):
    final_output[ii][0] = vals[ii].tostring()
    #final_output[0][ii] = 'nblahh'
    #final_output[0][ii] = vals.tostring()

print(type(vals[0].tostring()))
print(vals[0].tostring())
print(final_output)
exit()


# loop though subjects
for subj in Subj_names:

    # Go to base folder
    os.chdir(base_folder)
    # go to subject folder
    os.chdir(subj)

    # command to run
    run ="3dRSFC " + "-mask " + mask + " -band " + fbot + " " + ftop + " -prefix " + subj + " -input " + filename + ".nii.gz"
    print("command:")
    print(run)
    #os.system(run)

    # Going to extract the F/ALFF from the data
    # loop through ROIs
    for roi_name in ROI_names:
        # command to run
        roi = ROI_loc + roi_name

        # ALFF
        run = "3dROIstats  -quiet -mask " + roi + "_mask.nii.gz " + subj + "_ALFF+tlrc.HEAD > " + output_temp
        print(run)
        os.system(run)


        #SZ5011A_ALFF + tlrc.BRIK
        #SZ5011A_fALFF + tlrc.BRIK


#import numpy
#a = numpy.asarray([ [1,2,3], [4,5,6], [7,8,9] ])
#numpy.savetxt("foo.csv", a, delimiter=",")



import numpy
a = numpy.asarray([ [1,2,3], [4,5,6], [7,8,9] ])
numpy.savetxt("foo.csv", a, delimiter=",")

exit()


#!!!ROI = '/Users/afranco/TEMP/DON/Group1_thresh_zstat0010_LeftPost_mask.nii.gz'
output = '/Users/afranco/TEMP/DON/ALFF_Group1_RightPost.txt'

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