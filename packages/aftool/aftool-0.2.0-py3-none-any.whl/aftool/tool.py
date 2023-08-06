# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     tool
   Description :
   Author :        Asdil
   date：          2019/12/26
-------------------------------------------------
   Change Activity:
                   2019/12/26:
-------------------------------------------------
"""
__author__ = 'Asdil'
import os
import pip
import gzip
import time
import shutil
import zipfile
import psutil
import itertools
import subprocess
from tqdm import tqdm
from datetime import datetime
from inspect import signature


def path_join(path1, path2):
    """
    合并两个目录
    :param path1:  路径
    :param path2:  文件名
    :return:
    """
    assert isinstance(path1, str)
    assert isinstance(path2, str)
    if path1[-1] != os.sep:
        path1 += os.sep
    if path2[0] == os.sep:
        path2 = path2[1:]
    return path1 + path2


def get_files(path, extension=None, key=None):
    """
    获取目标目录文件
    :param path:      路径
    :param extension: 后缀
    :param key:       关键字
    :return:
    """
    if extension is not None:
        length = -len(extension)
        ret = [path_join(path, each) for each in os.listdir(
            path) if each[length:] == extension]
    elif key is not None:
        ret = [path_join(path, each)
               for each in os.listdir(path) if key in each]
    else:
        ret = [path_join(path, each) for each in os.listdir(path)]
    return ret


# 获取文件名
def get_name(path, extension=None, key=None):
    """
    获取目标目录下文件名
    :param path:      路径
    :param extension: 后缀
    :param key:       关键字
    :return:
    """
    if extension is not None:
        l = -len(extension)
        ret = [each for each in os.listdir(path) if each[l:] == extension]
    elif key is not None:
        ret = [each for each in os.listdir(path) if key in each]
    else:
        ret = [each for each in os.listdir(path)]
    return ret


def bar(data):
    """
    进度条
    :param data: 列表 字典 迭代器
    :return:
    """
    if isinstance(data, int):
        return tqdm(range(data))
    return tqdm(data)


def subprocess_check_call(cmd):
    """
    执行命令行命令
    :param cmd:  命令行命令
    :return:
    """
    subprocess.check_call(cmd, shell=True)


def subprocess_call(cmd):
    """
    执行命令行命令，不检查
    :param cmd:  命令行命令
    :return:
    """
    subprocess.call(cmd, shell=True)


def subprocess_popen(cmd):
    """
    执行命令获取返回值
    :param cmd:  命令行命令
    :return:
    """
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    out, err = p.communicate()
    return [each for each in out.decode('utf8').splitlines()]


def split_path(path):
    """
    拆分目录
    eg: '/tmp/tmp/a.txt'
        '/tmp/tmp', 'a.txt', 'a', 'txt'
    :param path: 路径
    :return:
    """
    assert isinstance(path, str)
    file_path, file_full_name = os.path.split(path)
    file_name, extension = os.path.splitext(file_full_name)
    return file_path, file_name, extension, file_full_name


def copy_file(srcfile, dstfile):
    """
    复制文件
    :param srcfile: 拷贝文件路径
    :param dstfile: 目标路径
    :return:
    """

    if not os.path.isfile(srcfile):
        print("%s not exist!" % srcfile)
        assert os.path.isfile(srcfile) is True
    else:
        _, _, _, name = split_path(srcfile)
        if dstfile[-len(name):] == name:
            fpath, fname = os.path.split(dstfile)  # 分离文件名和路径
        else:
            fpath = dstfile

        if not os.path.exists(fpath):
            os.makedirs(fpath)  # 创建路径

        dstfile = path_join(fpath, name)
        shutil.copyfile(srcfile, dstfile)  # 复制文件
        print("copy %s -> %s" % (srcfile, dstfile))


def cut_file(srcfile, dstfile):
    """
    剪切文件
    :param srcfile: 剪切文件路径
    :param dstfile: 目标路径
    :return:
    """
    if not os.path.isfile(srcfile):
        print("%s not exist!" % srcfile)
        assert os.path.isfile(srcfile) is True
    else:
        fpath, fname = os.path.split(dstfile)    # 分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)                 # 创建路径
        shutil.move(srcfile, dstfile)          # 复制文件
        print("cut %s -> %s" % (srcfile, dstfile))


def re_write_txt(file_Path, key, newstr):
    """
    替换txt文件关键字
    :param file_Path: 文件路径
    :param key:       关键字
    :param newstr:    替换词
    :return:
    """
    content = ""
    with open(file_Path, "r", encoding="utf-8") as f:
        for line in f:
            if key in line:
                line = newstr + '\n'
            content += line
    # 写入
    with open(file_Path, "w", encoding="utf-8") as f:
        f.write(content)


def inter_set(l1, l2):
    """
    列表交集
    :param l1:
    :param l2:
    :return:
    """
    assert type(l1) in [list, set]
    assert type(l2) in [list, set]
    return list(set(l1).intersection(set(l2)))


def diff_set(l1, l2):
    """
    列表差集
    :param l1:
    :param l2:
    :return:
    """
    assert type(l1) in [list, set]
    assert type(l2) in [list, set]
    return list(set(l1).difference(set(l2)))


def union_set(l1, l2):
    """
    列表并集
    :param l1:
    :param l2:
    :return:
    """
    assert type(l1) in [list, set]
    assert type(l2) in [list, set]
    return list(set(l1).union(set(l2)))


def create_dir(path):
    """
    检查文件夹是否存在，如果存在则删除重新创建
    :param path:    文件夹路径
    :param type:    文件夹不存在是否报错  True报错， False不报错,并创建文件夹
    :return:
    """
    if not os.path.exists(path):
        os.makedirs(path)
        return True
    return False


def del_dir(path):
    """
    删除目录
    :param path:  路径
    :return:
    """
    shutil.rmtree(path)


def combin_dic(*args):
    """
    合并字典
    :param args: 两个字典或多个
    :return:
    """
    ret = {}
    if len(args) == 1:
        dicts = args[0]
        assert isinstance(dicts, list)  # 断言是个列表
        for _dict in dicts:
            ret = dict(ret, **_dict)
    else:
        for _dict in args:
            assert isinstance(_dict, dict)
        for _dict in args:
            ret = dict(ret, **_dict)
    return ret


def add_dic(dica, dicb):
    """
    字典累加
    :param dica:   字典a
    :param dicb:   字典b
    :return:       字典累加
    """
    dic = {}
    for key in dica:
        if dicb.get(key):
            dic[key] = dica[key] + dicb[key]
        else:
            dic[key] = dica[key]
    for key in dicb:
        if dica.get(key):
            pass
        else:
            dic[key] = dicb[key]
    return dic


def split_list(_list, slice):
    """
    拆分列表
    :param _list:  列表
    :param slice:  拆分块的大小
    :return:       拆分后的列表
    """
    return [_list[i:i + slice] for i in range(0, len(_list), slice)]


def zip_file(file_path, output=None, rename=None, typ=3):
    """
    压缩文件
    :param file_path:  文件绝对路径
    :param output:     是否输入到其它文件夹
    :return:           True, False
    """
    # 拆分成文件路径，文件
    path, name, _, name_extension = split_path(file_path)
    if rename is None:
        rename = name

    if output is None:
        output = path
    azip = zipfile.ZipFile(path_join(output, rename + '.zip'), 'w')
    # 写入zip
    if typ == 1:
        azip.write(file_path, name_extension, compress_type=zipfile.ZIP_LZMA)

    elif typ == 2:
        azip.write(file_path, name_extension, compress_type=zipfile.ZIP_BZIP2)
    else:
        azip.write(
            file_path,
            name_extension,
            compress_type=zipfile.ZIP_DEFLATED)
    azip.close()
    print("{} -> {}".format(file_path, path_join(output, rename + '.zip')))


def unzip_file(file_path, output=None):
    """
    解压文件
    :param file_path:  zip文件完整路径
    :return:
    """
    path, name, _, name_extension = split_path(file_path)
    azip = zipfile.ZipFile(file_path)
    if output is None:
        azip.extractall(path=output)
        output = path_join(path, name)
    else:
        azip.extractall(path=output)
        output = path_join(output, name)
    azip.close()
    print("{} ->> {}".format(file_path, output))


def zip_dir(file_dir, output=None, rename=None):
    """
    压缩文件夹
    :param file_dir:  文件夹路径
    :param output:    输出路径
    :param rename:    重命名
    :return:
    """
    if rename is None:
        tmp = file_dir.strip('/')
        dirs = tmp.strip('/').split('/')
        rename = dirs[-1]
    # 压缩文件夹
    if output is None:
        output = '/' + '/'.join(dirs[:-1])
        print(path_join(output, rename))
        shutil.make_archive(path_join(output, rename), 'zip', file_dir)
    else:
        shutil.make_archive(path_join(output, rename), 'zip', file_dir)
    print("{} -> {}".format(file_dir, path_join(output, rename) + '.zip'))


def unzip_dir(file_dir, output=None, rename=None):
    """
    解压文件夹
    :param file_dir:  解压文件夹
    :return:
    """
    path, name, _, _ = split_path(file_dir)
    if output is None:
        output = path
    if rename is None:
        rename = name
    output = path_join(output, rename)

    shutil.unpack_archive(file_dir, output)
    print('{} ->> {}'.format(file_dir, output))


def gzip_file(file_path, output=None, rename=None, del_file=False):
    """
    gzip文件
    :param file_path: 文件路径
    :param output:    输出路径
    :param rename:    重命名
    :param del_file:  是否删除源文件
    :return:
    """
    assert os.path.exists(file_path)
    path, name, _, name_extension = split_path(file_path)
    if rename is None:
        rename = name
    if output is None:
        output = path
    rename += '.gz'
    out_path = path_join(output, rename)
    with open(file_path, 'rb') as f_in:
        with gzip.open(out_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    if del_file:
        os.remove(file_path)
    print('{} ->> {}'.format(file_path, out_path))


def gunzip_file(file_path, output=None, rename=None, del_file=False):
    """
    解压gz文件
    :param file_path: 文件路径
    :param output:    输出路径
    :param rename:    重命名
    :param del_file:  是否删除源文件
    :return:
    """
    assert os.path.exists(file_path)
    path, name, _, name_extension = split_path(file_path)
    if rename is None:
        rename = name
    if output is None:
        output = path
    if rename[-3:] == '.gz':
        rename = rename[:-3]
    out_path = path_join(output, rename)
    with gzip.open(file_path, 'rb') as f_in:
        data = f_in.read().decode('utf8')
        with open(out_path, 'w') as f_out:
            f_out.write(data)
    if del_file:
        os.remove(file_path)
    print('{} ->> {}'.format(file_path, out_path))


def until(y=None, m=None, d=None, H=None, M=None, S=None, logger=None):
    """
    定时任务
    :param y:  年
    :param m:  月
    :param d:  日
    :param H:  时
    :param M:  分
    :param S:  秒
    :param logger: 日志
    :return:
    """
    import time
    import datetime
    if y:
        y = int(y)
        m = int(m)
        d = int(d)
        H = int(H)
        M = int(M)
        S = int(S)
        try:
            startTime = datetime.datetime(y, m, d, H, M, S)
        except BaseException:
            if logger:
                logger.info('年月日时分秒输入错误')
            print('年月日时分秒输入错误')
            assert 1 == 2
        if startTime < datetime.datetime.now():
            logger.info('开始时间在当前时间之前')
            print('开始时间在当前时间之前')
            assert 2 == 3

        second = (startTime - datetime.datetime.now()).seconds
        minute = second // 60
        second = second % 60
        hour = minute // 60
        minute = minute % 60
        day = hour // 24
        hour = hour % 24

        print(f'将于{day}天{hour}小时{minute}分{second}秒 后运行')
        if logger:
            logger.info(f'将于{day}天{hour}小时{minute}分{second}秒 后运行')

        while datetime.datetime.now() < startTime:
            time.sleep(1)
        print('到达预定时间开始运行程序')
        if logger:
            logger.info('到达预定时间开始运行程序')
    else:
        if d or H or M or S:
            if H is None:
                H = 0
            if M is None:
                M = 0
            if S is None:
                S = 0
            seconds = 0
            time_dic = {'day': 86400,
                        'hour': 3600,
                        'min': 60}
            if d:
                seconds = (
                    time_dic['day'] *
                    int(d) +
                    time_dic['hour'] *
                    int(H) +
                    time_dic['min'] *
                    int(M) +
                    int(S))
                print(f'将于{d}天{H}小时{M}分{S}秒 后运行')
                if logger:
                    logger.info(f'将于{d}天{H}小时{M}分{S}秒 后运行')
            elif H:
                seconds = (
                    time_dic['hour'] *
                    int(H) +
                    time_dic['min'] *
                    int(M) +
                    int(S))
                print(f'将于{H}小时{M}分{S}秒 后运行')
                if logger:
                    logger.info(f'将于{H}小时{M}分{S}秒 后运行')
            elif M:
                seconds = (time_dic['min'] * int(M) + int(S))
                print(f'将于{M}分{S}秒 后运行')
                if logger:
                    logger.info(f'将于{M}分{S}秒 后运行')
            else:
                seconds = int(S)
                print(f'将于{S}秒 后运行')
                if logger:
                    logger.info(f'将于{S}秒 后运行')
            time.sleep(seconds)
            print('到达预定时间开始运行程序')
            if logger:
                logger.info('到达预定时间开始运行程序')
        else:
            print('错误！ 定时任务没有指定时间')
            if logger is not None:
                logger.info('错误！ 定时任务没有指定时间')
                assert 3 == 4


def get_process_id(name):
    """
    获取进程pid
    :param name:
    :return:
    """
    child = subprocess.Popen(["pgrep", "-f", name],
                             stdout=subprocess.PIPE, shell=False)
    response = child.communicate()[0]
    response = response.decode().strip().split('\n')
    if len(response) == 1 and len(response[0]) == 0:
        return []
    return response


def monitor_memery_cpu(pids, second=10, out_path=None, show=False):
    """
    pu使用率
    :param pids:
    :param second:
    :param out_path:
    :param show:
    :return:
    """
    proc = psutil.Process(int(pids))
    info = ['cpu rate\tmemory use']
    while True:
        try:
            cpu = psutil.cpu_percent()
            memory = proc.memory_info().rss / 1024 / 1024
        except BaseException:
            break
        if show:
            print(f'cpu 使用率: {cpu}%  memory 使用量 {round(memory, 2)}MB')
        info.append(f'{cpu}\t{memory}')
        time.sleep(second)
    if out_path is not None:
        with open(out_path, 'w') as f:
            f.write('\n'.join(info))


def read(path, sep='\n'):
    """
    按行读数据
    :param path: 路径
    :param sep:  分隔符
    :return:
    """
    with open(path, 'r') as f:
        return f.read().strip().split(sep)


def merge_commelement_list(lsts):
    """
    把公共元素的列表合并，返回合并后的结果list
    :param lsts:
    :return:
    """
    sets = [set(lst) for lst in lsts if lst]
    merged = 1
    while merged:
        merged = 0
        results = []
        while sets:
            common, rest = sets[0], sets[1:]
            sets = []
            for x in rest:
                if x.isdisjoint(common):
                    sets.append(x)
                else:
                    merged = 1
                    common |= x
            results.append(common)
        sets = results
    return sets


def runtime(func):
    """
    运行时间的装饰器
    :param : python function
    :return:
    """
    def wrapper(*args, **kwargs):
        start_now = datetime.now()
        start_time = time.time()
        ret = func(*args, **kwargs)
        end_time = time.time()
        end_now = datetime.now()
        print(f'time时间:{end_time-start_time}')
        print(
            f'datetime起始时间:{start_now} 结束时间:{end_now}, 一共用时{end_now-start_now}')
        return ret
    return wrapper


def typeassert(*ty_args, **ty_kwargs):
    def decorate(func):
        # If in optimized mode, disable type checking
        if not __debug__:
            return func

        # Map function argument names to supplied types
        sig = signature(func)
        bound_types = sig.bind_partial(*ty_args, **ty_kwargs).arguments

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_values = sig.bind(*args, **kwargs)
            # Enforce type assertions across supplied arguments
            for name, value in bound_values.arguments.items():
                if name in bound_types:
                    if not isinstance(value, bound_types[name]):
                        raise TypeError(
                            'Argument {} must be {}'.format(
                                name, bound_types[name]))
            return func(*args, **kwargs)
        return wrapper
    return decorate


def install(package):
    """install方法用于安装包

    Parameters
    ----------
    package : str
        包名
    Returns
    ----------
    """
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])


def flatten(data):
    """flatten方法用于平铺list

    Parameters
    ----------
    data : list
        列表

    Returns
    ----------
    """
    return list(itertools.chain.from_iterable(data))
