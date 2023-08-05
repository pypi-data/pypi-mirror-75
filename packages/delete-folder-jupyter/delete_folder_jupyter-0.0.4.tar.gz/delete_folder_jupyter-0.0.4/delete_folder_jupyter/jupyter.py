def delete_folder(folder_name):
    import os
    import shutil
    if (os.path.exists(os.path.join(folder_name,".git"))):
        shutil.rmtree(folder_name)
    else :
         raise ValueError("The folder {0} isn't a version control directory".format(folder_name))