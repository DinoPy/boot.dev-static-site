import os
import shutil


def remove_files_from_destination_dir(destination_path):
    if os.path.exists(destination_path):
        destination_file_list = os.listdir(
            os.path.join(destination_path))
        for file in destination_file_list:
            print(file)
            if os.path.isfile(os.path.join(destination_path, file)):
                os.remove(os.path.join(destination_path, file))
            if os.path.isdir(os.path.join(destination_path, file)):
                shutil.rmtree(path=os.path.join(destination_path, file),
                              onerror=lambda x: print("error ", "x"))
    else:
        os.mkdir(destination_path)


def file_copy_handler(source_path, destination_path):
    if not os.path.exists(source_path):
        raise Exception("source path doesn't exist")
    if not os.path.exists(destination_path):
        raise Exception("destination path doesn't exist")
    source_files = os.listdir(source_path)
    for file in source_files:
        file_path = os.path.join(source_path, file)
        if os.path.isfile(file_path):
            shutil.copy(file_path, destination_path)
        if os.path.isdir(file_path):
            dest_file_path = os.path.join(destination_path, file)
            if not os.path.exists(dest_file_path):
                os.mkdir(dest_file_path)
            file_copy_handler(file_path, dest_file_path)


def copy_files():
    project_path = "/Users/costindinoiu/Documents/Dev/Projects/boot.dev/python/static_sites/"
    destination = "public"
    source = "static"
    remove_files_from_destination_dir(os.path.join(project_path, destination))
    file_copy_handler(os.path.join(project_path, source),
                      os.path.join(project_path, destination))
