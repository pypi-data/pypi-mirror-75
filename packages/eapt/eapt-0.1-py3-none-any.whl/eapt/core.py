import argparse
import os
import re
import shutil
import sys
from os import listdir, mkdir, path, rename, system
from time import ctime, time

from eapt import repoutil, resolver

TOP_K = 15

class eAPT:
    def __init__(self, debug=False):
        self.__baseDir = path.join(path.expanduser("~"), '.eapt')
        self.__candidateFile = path.join(self.__baseDir, 'candidates.txt')
        self.__debug = debug

        if not path.exists(self.__baseDir):
            mkdir(self.__baseDir)
        elif path.isfile(self.__candidateFile):
            with open(self.__candidateFile, 'r') as f:
                # strip to remove newline
                self._candidates = [l.strip() for l in f.readlines()]


    @property
    def candidates(self):
        return self._candidates


    def __dprint(self, *args):
        if self.__debug:
            print(*args)

    @candidates.setter
    def candidates(self, candidates):
        self._candidates = candidates

        with open(self.__candidateFile, 'w') as f:
            f.writelines([url + '\n' for url in candidates])


    def init(self):
        '''
        Fetch local mirrors from Ubuntu server.
        For now, eAPT saves all local mirror sites as candidate.
        Top-K will be selected each time they are loaded.
        '''
        print(f"Finding candidate mirror sites...")
        self.candidates = resolver.getCandidates()

        for i in range(len(self.candidates)):
            print(str(i+1) + ". " + self.candidates[i])

        self.updateCandidatePkgList()


    def updateOptimalMirror(self):
        self.__dprint('[eAPT] Finding optimal mirror...')

        ret = resolver.testLatencies(self.candidates)
        repoutil.useMirror(ret[0][0])

        self.__dprint('[eAPT] Using mirror :', ret[0][0])


    def updateCandidatePkgList(self):
        repoutil.useMirror(self.candidates[0])


    def applyMirror(self, bestMirror):
        filename = '/etc/apt/sources.list'
        listsFilesPath = '/var/lib/apt/lists'
        expression = 'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
        expression2 = '(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
        pattern = re.compile(expression)
        pattern2 = re.compile(expression2)
        urls = []

        bestMirror = re.findall(pattern, bestMirror)[0]
        
        try:
            # original file backup
            if path.isfile(filename + '.bak') == False:
                shutil.copy(filename, filename + '.bak')
        except Exception as e:
            print(e)
            print('If you can see the Permission denied error, please use sudo.')
            sys.exit(0)
        
        #urls = re.findall(pattern, buffer)
        for i, line in enumerate(open(filename)):
            for match in re.finditer(pattern, line):
                #print 'Found on line %s: %s' % (i+1, match.group())
                urls.append(match.group())

        urls = list(set(urls))
        
        # change list files and update sources.list
        with open(filename, 'r') as file :
            filedata = file.read()
        
        for url in urls:
            urlPath = re.findall(pattern2, url)[1]
            urlPathBest = re.findall(pattern2, bestMirror)[1]
            for file in listdir(listsFilesPath):
                if file.find(urlPath) != -1:
                    a = rename(path.join(listsFilesPath, file), path.join(listsFilesPath, file.replace(urlPath, urlPathBest)))
            filedata = filedata.replace(url, bestMirror)

        with open(filename, 'w') as file:
            file.write(filedata)

        #os.system("apt update")


    def callAPT(self, argv):
        # forward to apt
        self.updateOptimalMirror()
        system("apt " + ' '.join(argv))


def main():
    def __config_args():
        parser = argparse.ArgumentParser(description='Enhanced APT')

        parser.add_argument('--init', 
                            action='store_const',
                            const=True, 
                            default=False, 
                            help='initializes local mirror sites')

        parser.add_argument('--update-mirror', 
                            action='store_const',
                            const=True, 
                            default=False,
                            help='find an optimal mirror and configure APT to use it')

        parser.add_argument('-d', '--debug', 
                            action='store_const',
                            const=True, 
                            default=False,
                            help='show debug print for eAPT')

        parser.add_argument('args', nargs=argparse.REMAINDER)

        return parser
    
    parser = __config_args()
    args = parser.parse_args()
    eapt = eAPT(args.debug)

    if args.init:
        eapt.init()
    elif args.update_mirror:
        eapt.updateOptimalMirror()
    else:
        eapt.callAPT(args.args)
