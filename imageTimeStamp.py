import os
import platform
import datetime
import glob
from PIL import Image
from PIL import ExifTags

# Appends time stamp to file name of images
# Finds groups of files according to regex
# groupFilePath is file pointer to directory
# nameRegex is regex search (i.e. '*.jpg' to get all files with extension '.jpg')
def groupAddTimeStamp(groupFilePath, nameRegex):
    fileList = glob.glob(os.path.join(groupFilePath,nameRegex));
    for filePath in fileList:
        renameFileWithTimeStamp(filePath, filePath);

# Renames groups of images with time taken stamp
# Finds groups of files according to regex
# groupFilePath is file pointer to directory
# nameRegex is regex search
# baseNameReplace is path and new base name together
# baseNameReplace is not necessarily the same path or name as original
def groupRename(groupFilePath, nameRegex, baseNameReplace):
    fileList = glob.glob(os.path.join(groupFilePath,nameRegex));
    for filePath in fileList:
        renameFileWithTimeStamp(filePath, baseNameReplace);

# renames a file (jpg) with a time stamp
# newFileBaseName includes the file extension
def renameFileWithTimeStamp(filePath, newFileBaseName):
    timeStamp = getImageTimeStamp(filePath);
    newFileName = os.path.splitext(newFileBaseName)[0] + '_' + timeStamp + os.path.splitext(newFileBaseName)[1];
    os.rename(filePath, newFileName);

# Reads time image was taken, uses PIL imports
def getImageTimeStamp(filePath):
    image = Image.open(filePath);
    # 36867 is the dictionary key for time the image was taken
    # _getexif() returns a dictionary of the exif data
    timestamp = image._getexif()[36867];
    # Convert the timestamp into a yymmdd_hhmmss time format
    timeString = timestamp[2:4]+timestamp[5:7]+timestamp[8:10]+'_'+timestamp[11:13]+timestamp[14:16]+timestamp[17:19]
    return timeString;

# Get file creation date in case file isn't jpg
# Copied from stackoverflow (link below)
def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return unixToDateTime(os.path.getctime(path_to_file))
    else:
        stat = os.stat(path_to_file)
        try:
            return unixToDateTime(stat.st_birthtime)
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return unixToDateTime(stat.st_mtime)

# uses datetime import
def unixToDateTime(time):
    return datetime.datetime.fromtimestamp(int(time)).strftime('%y-%m-%d %H:%M:%S')
