import SimpleITK as sitk

def dcmToNii(file):

    reader = sitk.ReadImage(file)
    writer = sitk.WriteImage(reader, "image-0-dtn.nii")

#have not been used as of now.
def NiiToDcm(file):

    reader = sitk.ReadImage(file)
    writer = sitk.WriteImage(reader, "image-0-ntd.dcm")

def main():
    file = "image-0.dcm"
    converted_dtn = dcmToNii(file)
    print("converted the file from dicom to nifti")
    print(repr(converted_dtn))


if __name__ == "__main__":
    main()