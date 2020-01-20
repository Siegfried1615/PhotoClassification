from os import path

# 返回照片时间信息
from pip._vendor import requests


def exifread_infos(photo):
    import exifread
    filename = path.split("//")[-1]
    # 获取照片时间、经纬度信息
    # photo参数：照片文件路径
    # Open image file for reading (binary mode)
    f = open(photo, 'rb')
    # Return Exif tags
    tags = exifread.process_file(f)

    try:
        # 拍摄时间
        EXIF_Date = str(tags["EXIF DateTimeOriginal"]).replace(':', '').replace(' ', '_')
        # 纬度
        LatRef = tags["GPS GPSLatitudeRef"].printable
        Lat = tags["GPS GPSLatitude"].printable[1:-1].replace(" ", "").replace("/", ",").split(",")
        Lat = float(Lat[0]) + float(Lat[1]) / 60 + float(Lat[2]) / float(Lat[3]) / 3600
        if LatRef != "N":
            Lat = Lat * (-1)
        # 经度
        LonRef = tags["GPS GPSLongitudeRef"].printable
        Lon = tags["GPS GPSLongitude"].printable[1:-1].replace(" ", "").replace("/", ",").split(",")
        Lon = float(Lon[0]) + float(Lon[1]) / 60 + float(Lon[2]) / float(Lon[3]) / 3600
        if LonRef != "E":
            Lon = Lon * (-1)
        f.close()
    except:
        return "ERROR:请确保照片包含经纬度等EXIF信息。"
    else:
        return EXIF_Date, Lat, Lon


def get_location(lat, lon):
    url = 'http://api.map.baidu.com/reverse_geocoding/v3/?ak=ukgiP03vGBPeAo9PBn3GQooObDirU6ei&' \
          'output=json&coordtype=wgs84ll&location={},{}'.format(lat, lon)
    response = requests.get(url).json()
    status = response['status']
    if status == 0:
        address = response['result']['formatted_address']
        return address
        # print('详细地址：', self.address)
    else:
        return "API调用出错，可能已达上限。"
