import os
import re
import shutil
from collections import Counter

EAPT_DIR = os.path.join(os.path.expanduser("~"), '.eapt')
EAPT_PREFIX = '_eapt_'
CACHE_DIR = os.path.join(EAPT_DIR, 'lists')
APT_DIR = '/etc/apt'
PKGLIST_DIR = '/var/lib/apt/lists'

def __getHost(url):
    urlWithoutScheme = re.compile('(?:[-\w.]|(?:%[\da-fA-F]{2}))+')
    host = re.findall(urlWithoutScheme, url)[1]
    return host


def __toEaptName(url):
    host = __getHost(url)
    return EAPT_PREFIX + host


def __detectCurrentRepo(srcList):
    urlWithScheme = re.compile('https?:\/\/(?:[-\w.]|(?:%[\da-fA-F]{2}))+(?:[-\/\w.]*)')
    urls = map(lambda x: x.group(), re.finditer(urlWithScheme, srcList))

    # heuristics: select the most frequent URL as current repository URL
    currentRepo = Counter(urls).most_common()[0][0]
    return currentRepo


def __aptUpdate():
    os.system('apt update')


def __cachePkgList(url):
    name = __toEaptName(url)
    host = __getHost(url)
    cacheDir = os.path.join(CACHE_DIR, name)

    if not os.path.exists(CACHE_DIR):
        os.mkdir(CACHE_DIR)

    if not os.path.exists(cacheDir):
        os.mkdir(cacheDir)

    for file in os.listdir(PKGLIST_DIR):
        if host in file:
            shutil.move(
                os.path.join(PKGLIST_DIR, file), 
                os.path.join(cacheDir, file))


def __cacheExists(url):
    name = __toEaptName(url)
    return os.path.exists(os.path.join(CACHE_DIR, name))


def __useCachedPkgList(url):
    name = __toEaptName(url)
    host = __getHost(url)
    cacheDir = os.path.join(CACHE_DIR, name)
    
    for file in os.listdir(cacheDir):
        if host in file:
            shutil.move(
                os.path.join(cacheDir, file),
                os.path.join(PKGLIST_DIR, file))


def __newPkgList(url):
    __aptUpdate()
    __cachePkgList(url)


def __updateSrcList(content):
    with open(os.path.join(APT_DIR, 'sources.list'), 'w') as f:
        f.write(content)


def useMirror(url):
    with open(os.path.join(APT_DIR, 'sources.list'), 'r') as f:
        srcList = f.read()
    currentUrl = __detectCurrentRepo(srcList)

    if currentUrl == url:
        print('[eAPT] Already using optimal mirror')
        return

    __updateSrcList(srcList.replace(currentUrl, url))
    __cachePkgList(currentUrl)
    if __cacheExists(url):
        print('[eAPT] Using cached package list')
        __useCachedPkgList(url)
    else:
        print('[eAPT] Calling apt update')
        __newPkgList(url)
