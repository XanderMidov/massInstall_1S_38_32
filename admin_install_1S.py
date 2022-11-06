import ctypes, sys, os, shutil, configparser, time, pathlib
from pathlib import Path

def get_version(path):
    ver = ''
    path_tuple = path.parts
    path_last_elem: str = path_tuple[-1]
    for letter in path_last_elem:
        if letter.isdigit():
            ver += letter
        elif letter == '_':
            ver += '.'
    ver = ver[1:]
    return ver

settings = configparser.ConfigParser()
settings.read('install_1S.ini', encoding='utf-8')
src = settings['MAIN']['src']
dst = settings['MAIN']['dst']
tmp = settings['MAIN']['tmp']
src_path = Path(src)
ver = get_version(src_path)
dst_path = Path(dst, ver)
tmp_path = Path(tmp, ver)
bin_path = Path(dst_path, 'bin')


if not tmp_path.exists():
    print('Копирование временных файлов...')
    shutil.copytree(src_path, tmp_path)
    print('Копирование завершено')


def install_1s():
    print('Начало установки 1С...')
    os.system(r'msiexec -i "' + str(tmp_path) + os.sep + '1CEnterprise 8.msi' + '"-quiet TRANSFORMS=adminstallrelogon.mst;1049.mst DESIGNERALLCLIENTS=1 THICKCLIENT=1 THINCLIENTFILE=1 THINCLIENT=1 WEBSERVEREXT=0 SERVER=0 CONFREPOSSERVER=0 CONVERTER77=0 SERVERCLIENT=0 LANGUAGES=RU')
    print('Установка 1С завершена')
    if bin_path.exists():
        techsys_file = Path(bin_path, 'techsys.dll')
        techsys_file.rename(Path(bin_path, 'techsys_100.dll'))
        print('Переименование завершено')
        shutil.copy(Path(tmp_path, 'techsys.dll'), bin_path)
        print('Копирование завершено')
        time.sleep(5)
        if tmp_path.exists():
            shutil.rmtree(tmp_path)
        print('Удаление временных файлов завершено')
        print('Процесс завершен')
        os.system('pause')

def uninstall_1s():
    print('Начало удаления 1С...')
    os.system(r'msiexec -uninstall "' + str(tmp_path) + os.sep + '1CEnterprise 8.msi' + '"-quiet')
    print('Удаление 1С завершено')
    time.sleep(5)
    if dst_path.exists():
        shutil.rmtree(dst_path)
        print('Директория 1С удалена')
    time.sleep(5)
    if tmp_path.exists():
        shutil.rmtree(tmp_path)
        print('Удаление временных файлов завершено')
    print('Процесс завершен')
    os.system('pause')


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if is_admin():
    if bin_path.exists():
        uninstall_1s()
    else:
        install_1s()
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
