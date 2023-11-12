import tarfile
import os


def unzip_tarfile(dir_tar_files):
    for file in os.listdir(dir_tar_files):
        full_path = os.path.join(dir_tar_files, file)

        with tarfile.open(full_path, "r:gz") as tar:
            dir_to_save = os.path.splitext(file)[0]
            tar.extractall(path=dir_to_save)

        print(f"Unzip {file}")
