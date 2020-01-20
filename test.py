# 根据文件时间分类
import os
import shutil

from getInfo import exifread_infos, get_location
from mainrogram import get_filelist


def timeClassification(path_input, path_output):
    for f in get_filelist(path_input, []):
        filename = f.split("//")[-1]
        date = exifread_infos(f)[0][0:6]        # 精确到月份
        file_path = path_output + date
        isExists = os.path.exists(file_path)
        if not isExists:
            os.makedirs(file_path)
            shutil.copyfile(f, os.path.join(file_path, filename))
        else:
            shutil.copyfile(f, os.path.join(file_path, filename))


def locationClassification(path_input, path_output):
    for f in get_filelist(path_input, []):
        filename = f.split("//")[-1]
        lat = exifread_infos(f)[1]
        lon = exifread_infos(f)[2]
        address = get_location(lat, lon)
        file_path = path_output + address
        isExists = os.path.exists(file_path)
        if not isExists:
            os.makedirs(file_path)
            shutil.copyfile(f, os.path.join(file_path, filename))
        else:
            shutil.copyfile(f, os.path.join(file_path, filename))


if __name__ == '__main__':
    timeClassification("IMG_20200105_145649.jpg", ".")