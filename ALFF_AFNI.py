import os
import numpy as np
import csv
import subprocess

# NOTE:
# Missing functional data from SZ5014A and SZ5016A

base_folder = '/Users/afranco/TEMP/FALFF_GOFF'
mask = '/usr/local/fsl/data/standard/MNI152lin_T1_2mm_brain_mask.nii.gz'
filename = 'proc_nosmooth_norm'

ROI_loc = '/Users/afranco/TEMP/FALFF_GOFF/ROIS/'
roi_names_file = '/Users/afranco/TEMP/FALFF_GOFF/SCRIPTS/FALFF_GOFF/Hipp_ROIs.txt'
output_folder = '/Users/afranco/TEMP/FALFF_GOFF/output/'
output_file_ALFF = output_folder + "output_ALFF.csv"
output_file_fALFF = output_folder + "output_fALFF.csv"

subj_list_file = '/Users/afranco/TEMP/FALFF_GOFF/SCRIPTS/FALFF_GOFF/subj_list.txt'

# Filters for F/ALFF
fbot = '0.01'
ftop = '0.1'


# reading list of ROI names
with open(roi_names_file) as f:
    ROI_names = f.read().splitlines()
# Get number of rois
num_rois = len(ROI_names)

# Read the list of subj names
with open(subj_list_file) as f:
    Subj_names = f.read().splitlines()
# Get number of subjects
num_subjs = len(Subj_names)

# Creating the final output matrix
# Note adding an extra row and column to have headers
final_output_ALFF = np.array(range((num_rois+1)*(num_subjs+1)), dtype='a30').reshape((num_subjs+1), (num_rois+1))
# just a filler of the array
final_output_ALFF[:] = 'aa'
final_output_ALFF[0][0] = "subject - ROI"

# Putting ROI names on the table
name = np.array(ROI_names)
for ii in range(0, num_rois):
    final_output_ALFF[0][ii+1] = name[ii].tostring()

# Putting subject names on the table
for ii in range(0, num_subjs):
    final_output_ALFF[ii+1][0] = Subj_names[ii]

# Reusing the same template
final_output_fALFF = np.copy(final_output_ALFF)

# loop though subjects
ii_subj = 1
for subj in Subj_names:
    # Go to base folder
    os.chdir(base_folder)
    # go to subject folder
    os.chdir(subj)

    # command to run
    run = ("3dRSFC " + "-mask " + mask + " -band " + fbot + " " + ftop + " -prefix " + subj + " -input " +
           filename + ".nii.gz")
    print("command: ")
    print(run)
    os.system(run)


    # ALFF
    # Convert ALFF score to z-score
    # calculate summary stats within brain mask
    ALFF_FileName = subj + "_ALFF+tlrc.HEAD"
    run = "3dBrickStat -mean -mask " + mask + " " + ALFF_FileName
    dset_mean = subprocess.check_output(run, shell=True).rstrip('\n').lstrip('\t')
    run = "3dBrickStat -stdev -mask " + mask + " " + ALFF_FileName
    dset_stdev = subprocess.check_output(run, shell=True).rstrip('\n').lstrip('\t')

    print("The mean ALFF of values within the mask is: " + dset_mean + " for subject: " + subj)
    print("The stdev ALFF of values within the mask is: " + dset_stdev + " for subject: " + subj)

    # Now calculate the z-score
    run = "3dcalc -a " + ALFF_FileName + " -b " + mask + " -expr 'step(b)*(a - " + dset_mean + \
          ") / (" + dset_stdev + ")' -prefix " + subj + "_ALFF_Z_Score+tlrc.HEAD "
    print(run)
    os.system(run)

    # fALFF
    # Convert fALFF score to z-score
    # calculate summary stats within brain mask
    fALFF_FileName = subj + "_fALFF+tlrc.HEAD"
    run = "3dBrickStat -mean -mask " + mask + " " + fALFF_FileName
    dset_mean = subprocess.check_output(run, shell=True).rstrip('\n').lstrip('\t')
    run = "3dBrickStat -stdev -mask " + mask + " " + fALFF_FileName
    dset_stdev = subprocess.check_output(run, shell=True).rstrip('\n').lstrip('\t')

    print("The mean fALFF of values within the mask is: " + dset_mean + " for subject: " + subj)
    print("The stdev fALFF of values within the mask is: " + dset_stdev + " for subject: " + subj)

    # Now calculate the z-score
    run = "3dcalc -a " + fALFF_FileName + " -b " + mask + " -expr 'step(b)*(a - " + dset_mean + \
          ") / (" + dset_stdev + ")' -prefix " + subj + "_fALFF_Z_Score+tlrc.HEAD "
    print(run)
    os.system(run)




    # Going to extract the F/ALFF from the data
    # loop through ROIs
    ii_roi = 1
    for roi_name in ROI_names:
        # command to run
        roi = ROI_loc + roi_name

        ### ALFF
        # running 3droistats and getting the z-score
        run = "3dROIstats  -quiet -mask " + roi + "_mask.nii.gz " + subj + "_ALFF_Z_Score+tlrc.HEAD "
        print(run)
        z_score = subprocess.check_output(run, shell=True).rstrip('\n').lstrip('\t')
        print("z-score = " + z_score)
        final_output_ALFF[ii_subj][ii_roi] = z_score


        ### fALFF
        run = "3dROIstats  -quiet -mask " + roi + "_mask.nii.gz " + subj + "_fALFF+tlrc.HEAD "
        print(run)
        # running 3droistats and getting the score
        z_score = subprocess.check_output(run, shell=True).rstrip('\n').lstrip('\t')
        final_output_fALFF[ii_subj][ii_roi] = z_score


        print("ii_rois = " + str(ii_roi))
        ii_roi = ii_roi + 1

    print("ii_subj = " + str(ii_subj))
    ii_subj = ii_subj + 1

print(final_output_ALFF)
print(final_output_fALFF)
# saving output as csv
with open(output_file_ALFF, 'wb') as f:
    csv.writer(f).writerows(final_output_ALFF)
with open(output_file_fALFF, 'wb') as f:
    csv.writer(f).writerows(final_output_fALFF)

exit()
