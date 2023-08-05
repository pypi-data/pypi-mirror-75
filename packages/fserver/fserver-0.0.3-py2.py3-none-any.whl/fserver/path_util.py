# -*- coding: utf-8 -*-

import os
import re
import sys

try:
    from urllib.parse import unquote
except:
    from urllib import unquote

try:
    from os import scandir
except:
    from scandir import scandir


def to_unicode_str(s):
    if sys.version_info < (3, 4) and not isinstance(s, unicode):
        if isinstance(s, str):
            try:
                s = s.decode('utf-8')
            except:
                s = s.decode('gbk')
        else:
            s = unicode(s)
    elif sys.version_info >= (3, 4) and not isinstance(s, str):
        s = str(s)
    return s


def to_local_path(path):
    """
    :param path:
    :return: the path relative to current path
    """
    path = url_path_to_local_abspath(path)
    here = url_path_to_local_abspath('.')

    min_len = len(path) if len(path) < len(here) else len(here)

    if os.name == 'nt' and path[0] != here[0]:
        return path
    else:
        sep_ind = -1
        diff_ind = -1
        for i in range(min_len):
            if here[i] != path[i]:
                diff_ind = i
                break
            if here[i] == '/':
                sep_ind = i
        if diff_ind == -1:
            # split the same parent_path
            if len(path) < len(here):  # path is substring of here
                c = here[len(path):].count('/')
                return '../' * (c + 1)
            elif len(path) > len(here):  # here is substring of path
                if path[len(here)] == '/':
                    return path[len(here) + 1:]
                else:
                    return '../' + path[len(parent_path(here)) + 1:]
            else:  # here is the same with path
                return '.'
        else:
            # sep_ind won't be -1 because the use of local_abspath
            path = path[sep_ind + 1:]
            here = here[sep_ind + 1:]
            return '../' * (here.count('/') + 1) + path


def url_path_to_local_abspath(path):
    path = path.split('?', 1)[0]
    path = path.split('#', 1)[0]
    if path == '':
        path = '.'
    return normalize_path(os.path.abspath(path))


def normalize_path(path):
    p = os.path.normpath(path)
    if os.sep == '\\':
        p = p.replace('\\', '/')
    p = p.rstrip('/')
    return to_unicode_str(p)


def parents_path(path):
    """
    :param path:
    :return: return parents_path which does not contain the end '/', that is remove the end '/'
    """
    res = set()
    path = normalize_path(path)
    while '/' in path:
        sep_ind = path.rindex('/')
        res.add(path[:sep_ind])
        path = path[:sep_ind]
    if path.startswith('./') or not path.startswith('.'):
        res.add('.')
    return res


def parent_path(path):
    """
    :param path:
    :return: return path which does not contain the end '/'
    """
    path = normalize_path(path)
    if '/' not in path:
        return '.'
    else:
        sep_ind = path.rindex('/')
        return path[:sep_ind]


def get_filename(path):
    path = normalize_path(path)
    if '/' in path:
        sep_ind = path.rindex('/')
        return path[sep_ind + 1:]
    else:
        return path


def get_suffix(path):
    if '.' in path:
        return path[path.rindex('.') + 1:]
    else:
        return ''


def is_child(child_path, parent_path):
    nc = normalize_path(child_path)
    np = normalize_path(parent_path)
    if len(nc) > len(np) and nc.startswith(np + '/'):
        return True
    return False


def ls_reg(path):
    """
    ```shell
    $ ls
    Documents Downloads Pictures Public
    ```
    :param path: EXAMPLE( 'Do*'
    :return:     EXAMPLE( set(['Documents', 'Downloads'])
    """
    res = set()
    np = normalize_path(path)
    if os.path.exists(np):
        res.add(np)
        return res
    file_name = np if '/' not in np else np[np.rindex('/') + 1:]
    pattern = re.compile(file_name.replace('\\', r'\\')
                         .replace(r'$', r'\$')
                         .replace(r'(', r'\(')
                         .replace(r')', r'\)')
                         .replace(r'+', r'\+')
                         .replace(r'.', r'\.')
                         .replace(r'[', r'\[')
                         .replace(r'?', r'\?')
                         .replace(r'^', r'\^')
                         .replace(r'{', r'\{')
                         .replace(r'|', r'\|')
                         .replace(r'*', r'.*') + '$')
    npp = parent_path(np)
    if os.path.exists(npp) and os.path.isdir(npp):
        for entry in listdir(npp):
            i = entry.name
            if pattern.match(i):
                res.add(i if file_name == np else npp + '/' + i)
    return res


def listdir(path):
    return scandir(to_unicode_str(path))


if __name__ == '__main__':
    print(os.getcwd())
    print(url_path_to_local_abspath('template/'))
    print(to_local_path(os.getcwd() + '/' + '../a/b'))  # ../a/b
    print(to_local_path(os.getcwd() + '/' + 'c/d'))  # c/d
    print(to_local_path(os.getcwd() + '/' + '.'))  # .
    print(to_local_path(os.getcwd() + '/'))  # .
    print(to_local_path(os.getcwd() + '_diff/a'))  # ../x_diff/a
    print(to_local_path(parent_path(os.getcwd()) + '/diff/template'))  # ../diff/template
