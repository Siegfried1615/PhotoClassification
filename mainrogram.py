import os
from tkinter import *
from tkinter.filedialog import askdirectory


# 选择路径
from getInfo import exifread_infos, get_location


def select_Path_In():
    path_ = askdirectory()
    path_ = path_.replace("/", "\\\\")
    path_input.set(path_)


def select_Path_Out():
    path_ = askdirectory()
    path_ = path_.replace("/", "\\\\")
    path_output.set(path_)


# 获取所有图片绝对地址
def get_filelist(dir, Filelist):
    if os.path.isfile(dir):
        Filelist.append(dir)
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir = os.path.join(dir, s)
            get_filelist(newDir, Filelist)
    return Filelist


# 根据文件时间分类
def timeClassification():
    for f in get_filelist(path_input, []):
        filename = f.split("//")[-1]
        date = exifread_infos(f)[0][0:5]        # 精确到月份
        file_path = path_output + date
        isExists = os.path.exists(file_path)
        if not isExists:
            os.makedirs(file_path)
            f.save(os.path.join(file_path, filename))
        else:
            f.save(os.path.join(file_path, filename))


# 根据文件地点分类
def locationClassification():
    for f in get_filelist(path_input, []):
        filename = f.split("//")[-1]
        lat = exifread_infos(f)[1]
        lon = exifread_infos(f)[2]
        address = get_location(lat, lon)
        file_path = path_output + address
        isExists = os.path.exists(file_path)
        if not isExists:
            os.makedirs(file_path)
            f.save(os.path.join(file_path, filename))
        else:
            f.save(os.path.join(file_path, filename))


if __name__ == '__main__':
    root = Tk()
    root.title('简易照片分类 for xxy')  # 窗口标题
    root.geometry('400x200')  # 窗口尺寸
    root.iconbitmap('photo.ico')  # 窗口图标
    path_input = StringVar()
    path_output = StringVar()

    Label(root, text="目标路径:").grid(row=0, column=0)
    Entry(root, textvariable=path_input, width=35).grid(row=0, column=1)
    Button(root, text="路径选择", command=select_Path_In).grid(row=0, column=2)

    Label(root, text="输出路径:").grid(row=1, column=0)
    Entry(root, textvariable=path_output, width=35).grid(row=1, column=1)
    Button(root, text="路径选择", command=select_Path_Out).grid(row=1, column=2)

    root.mainloop()
