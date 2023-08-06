import os
import time


def relocateNow():
    try:
        source = os.getcwd()
        for path,dir1,files in os.walk(source):
            if files and path==source:
                for file in files:
                    try:
                        parts = file.split(".")
                        file_type = parts[-1].upper()
                        source_folder = os.path.join(path,file)
                        ctime = time.ctime(os.path.getmtime(source_folder)).split(" ")
                        file_time = ""+ctime[1].upper()+" "+ctime[-1]
                        target_folder = os.path.join(source,"RELOCATED")
                        if not os.path.exists(target_folder):
                            os.mkdir(target_folder)
                        target_folder = os.path.join(target_folder, file_time)
                        if not os.path.exists(target_folder):
                            os.mkdir(target_folder)
                        target_folder = os.path.join(target_folder, file_type)
                        if not os.path.exists(target_folder):
                            os.mkdir(target_folder)
                        target_folder = os.path.join(target_folder, file)
                        if not os.path.isfile(target_folder):
                            os.rename(source_folder , target_folder)
                    except:
                        print("Failed to relocate "+file)
        print("ALL FILES RELOCATED")
    except Exception as e:
        print(e)


def byMonthModified():
    try:
        source = os.getcwd()
        for path,dir1,files in os.walk(source):
            if files and path==source:
                for file in files:
                    try:
                        source_folder = os.path.join(path,file)
                        mtime = time.ctime(os.path.getmtime(source_folder)).split(" ")
                        file_time = ""+mtime[1].upper()+" "+mtime[-1]
                        target_folder = os.path.join(source,"RELOCATED")
                        if not os.path.exists(target_folder):
                            os.mkdir(target_folder)
                        target_folder = os.path.join(target_folder, file_time)
                        if not os.path.exists(target_folder):
                            os.mkdir(target_folder)
                        target_folder = os.path.join(target_folder, file)
                        if not os.path.isfile(target_folder):
                            os.rename(source_folder , target_folder)
                    except:
                        print("Failed to relocate "+file)
        print("ALL FILES RELOCATED")
    except Exception as e:
        print(e)


def byMonthCreated():
    try:
        source = os.getcwd()
        for path,dir1,files in os.walk(source):
            if files and path==source:
                for file in files:
                    try:
                        source_folder = os.path.join(path,file)
                        ctime = time.ctime(os.path.getctime(source_folder)).split(" ")
                        file_time = ""+ctime[1].upper()+" "+ctime[-1]
                        target_folder = os.path.join(source,"RELOCATED")
                        if not os.path.exists(target_folder):
                            os.mkdir(target_folder)
                        target_folder = os.path.join(target_folder, file_time)
                        if not os.path.exists(target_folder):
                            os.mkdir(target_folder)
                        target_folder = os.path.join(target_folder, file)
                        if not os.path.isfile(target_folder):
                            os.rename(source_folder , target_folder)
                    except:
                        print("Failed to relocate "+file)
        print("ALL FILES RELOCATED")
    except Exception as e:
        print(e)


def byMonthLastAccessed():
    try:
        source = os.getcwd()
        for path,dir1,files in os.walk(source):
            if files and path==source:
                for file in files:
                    try:
                        source_folder = os.path.join(path,file)
                        atime = time.ctime(os.path.getatime(source_folder)).split(" ")
                        file_time = ""+atime[1].upper()+" "+atime[-1]
                        target_folder = os.path.join(source,"RELOCATED")
                        if not os.path.exists(target_folder):
                            os.mkdir(target_folder)
                        target_folder = os.path.join(target_folder, file_time)
                        if not os.path.exists(target_folder):
                            os.mkdir(target_folder)
                        target_folder = os.path.join(target_folder, file)
                        if not os.path.isfile(target_folder):
                            os.rename(source_folder , target_folder)
                    except:
                        print("Failed to relocate "+file)
        print("ALL FILES RELOCATED")
    except Exception as e:
        print(e)


def byYearModified():
    try:
        source = os.getcwd()
        for path,dir1,files in os.walk(source):
            if files and path==source:
                for file in files:
                    try:
                        source_folder = os.path.join(path,file)
                        mtime = time.ctime(os.path.getmtime(source_folder)).split(" ")
                        file_time = ""+mtime[-1]
                        target_folder = os.path.join(source,"RELOCATED")
                        if not os.path.exists(target_folder):
                            os.mkdir(target_folder)
                        target_folder = os.path.join(target_folder, file_time)
                        if not os.path.exists(target_folder):
                            os.mkdir(target_folder)
                        target_folder = os.path.join(target_folder, file)
                        if not os.path.isfile(target_folder):
                            os.rename(source_folder , target_folder)
                    except:
                        print("Failed to relocate "+file)
        print("ALL FILES RELOCATED")
    except Exception as e:
        print(e)


def byYearCreated():
    try:
        source = os.getcwd()
        for path,dir1,files in os.walk(source):
            if files and path==source:
                for file in files:
                    try:
                        source_folder = os.path.join(path,file)
                        ctime = time.ctime(os.path.getctime(source_folder)).split(" ")
                        file_time = ""+ctime[-1]
                        target_folder = os.path.join(source,"RELOCATED")
                        if not os.path.exists(target_folder):
                            os.mkdir(target_folder)
                        target_folder = os.path.join(target_folder, file_time)
                        if not os.path.exists(target_folder):
                            os.mkdir(target_folder)
                        target_folder = os.path.join(target_folder, file)
                        if not os.path.isfile(target_folder):
                            os.rename(source_folder , target_folder)
                    except:
                        print("Failed to relocate "+file)
        print("ALL FILES RELOCATED")
    except Exception as e:
        print(e)


def byYearLastAccessed():
    try:
        source = os.getcwd()
        for path,dir1,files in os.walk(source):
            if files and path==source:
                for file in files:
                    try:
                        source_folder = os.path.join(path,file)
                        atime = time.ctime(os.path.getatime(source_folder)).split(" ")
                        file_time = ""+atime[-1]
                        target_folder = os.path.join(source,"RELOCATED")
                        if not os.path.exists(target_folder):
                            os.mkdir(target_folder)
                        target_folder = os.path.join(target_folder, file_time)
                        if not os.path.exists(target_folder):
                            os.mkdir(target_folder)
                        target_folder = os.path.join(target_folder, file)
                        if not os.path.isfile(target_folder):
                            os.rename(source_folder , target_folder)
                    except:
                        print("Failed to relocate "+file)
        print("ALL FILES RELOCATED")
    except Exception as e:
        print(e)


def byExtension():
    try:
        source = os.getcwd()
        for path,dir1,files in os.walk(source):
            if files and path==source:
                for file in files:
                    try:
                        parts = file.split(".")
                        file_type = parts[-1].upper()
                        source_folder = os.path.join(path,file)
                        target_folder = os.path.join(source,"RELOCATED")
                        if not os.path.exists(target_folder):
                            os.mkdir(target_folder)
                        target_folder = os.path.join(target_folder, file_type)
                        if not os.path.exists(target_folder):
                            os.mkdir(target_folder)
                        target_folder = os.path.join(target_folder, file)
                        if not os.path.isfile(target_folder):
                            os.rename(source_folder , target_folder)
                    except:
                        print("Failed to relocate "+file)
        print("ALL FILES RELOCATED")
    except Exception as e:
        print(e)


def byFirstChar():
    try:
        source = os.getcwd()
        for path,dir1,files in os.walk(source):
            if files and path==source:
                for file in files:
                    try:
                        parts = file.split(".")
                        first_char = parts[0][0].upper()
                        source_folder = os.path.join(path,file)
                        target_folder = os.path.join(source,"RELOCATED")
                        if not os.path.exists(target_folder):
                            os.mkdir(target_folder)
                        target_folder = os.path.join(target_folder, first_char)
                        if not os.path.exists(target_folder):
                            os.mkdir(target_folder)
                        target_folder = os.path.join(target_folder, file)
                        if not os.path.isfile(target_folder):
                            os.rename(source_folder , target_folder)
                    except:
                        print("Failed to relocate "+file)
        print("ALL FILES RELOCATED")
    except Exception as e:
        print(e)


def bySize():
    try:
        source = os.getcwd()
        for path,dir1,files in os.walk(source):
            if files and path==source:
                for file in files:
                    try:
                        source_folder = os.path.join(path,file)
                        file_bytes = os.path.getsize(source_folder)
                        print(file_bytes)
                        if (file_bytes < 1024):
                            file_size="Less than 1 KB"
                        elif (file_bytes < 1048576):
                            file_size = "Less than 1 MB"
                        elif (file_bytes < 5242880):
                            file_size = "Less than 5 MB"
                        elif (file_bytes < 10485760):
                            file_size = "Less than 10 MB"
                        elif (file_bytes < 52428800):
                            file_size = "Less than 50 MB"
                        elif (file_bytes < 104857600):
                            file_size = "Less than 100 MB"
                        elif (file_bytes < 524288000):
                            file_size = "Less than 500 MB"
                        elif (file_bytes < 1073741824):
                            file_size = "Less than 1 GB"
                        elif (file_bytes < 5368709120):
                            file_size = "Less than 5 GB"
                        elif (file_bytes < 10737418240):
                            file_size = "Less than 10 GB"
                        elif (file_bytes < 53687091200):
                            file_size = "Less than 50 GB"
                        elif (file_bytes < 107374182400):
                            file_size = "Less than 100 GB"
                        else:
                            file_size="More than 100 GB"
                        target_folder = os.path.join(source,"RELOCATED")
                        if not os.path.exists(target_folder):
                            os.mkdir(target_folder)
                        target_folder = os.path.join(target_folder, file_size)
                        if not os.path.exists(target_folder):
                            os.mkdir(target_folder)
                        target_folder = os.path.join(target_folder, file)
                        if not os.path.isfile(target_folder):
                            os.rename(source_folder , target_folder)
                    except:
                        print("Failed to relocate "+file)
        print("ALL FILES RELOCATED")
    except Exception as e:
        print(e)
