import h5py
import pandas as pd
import hdf5_getters
import os
import tables

root = '/mnt/snap/data' #EBS volume location
allfiles = []
size = 1000

for path, subdirs, files in os.walk(root):  #Getting list of files
    for name in files:
        if '.h5' in name:
            allfiles.append(os.path.join(path, name))

cols = []
for file in allfiles[:1]:  #Getting column names
    h = hdf5_getters.open_h5_file_read(file)
    for i in dir(hdf5_getters):
            item = getattr(hdf5_getters,i)
            if callable(item) and i!='open_h5_file_read':
                cols.append(i.split('get_')[1])


def file_content(file):
    h = hdf5_getters.open_h5_file_read(file)
    lsstr = []
    for i in dir(hdf5_getters):
            item = getattr(hdf5_getters,i)
            if callable(item) and i!='open_h5_file_read':
                lsstr.append(item(h))
    return lsstr

for file_idx in range(844000,len(allfiles),size):
    bucket_loc = 's3://million-song-dataset-16/data/' #S3 link address
    filename=f"output_{file_idx}.parquet"
    csvfile_ls=[]
    counter=0
    start_idx = file_idx
    end_idx = min(file_idx+size, len(allfiles))
    for file in allfiles[start_idx:end_idx]:
        counter += 1
        if counter%100 == 0:
            print(counter)
            tables.file._open_files.close_all()
        csvfile_ls.append(file_content(file))
    df=pd.DataFrame(csvfile_ls,columns=cols)
    file_path = os.path.join(bucket_loc,filename)
    df.to_parquet(file_path)
