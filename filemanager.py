import glob
import os
import sys
import time
import threading
from easygui import msgbox
from format import Format
def fixPath(rootSearchPath:str):
    for cur in rootSearchPath:
        if cur == '\\':
            cur='/'


def fileNameFromPath(path:str):
    path = path[::-1]
    ret = ""
    for curChar in path:
        if curChar == '\\':
            break
        else:
            ret+=curChar
    return ret[::-1]


def folderNameFromPath(path:str):
    trunacate = '\\'+fileNameFromPath(path)
    path = path.replace(trunacate,'')
    return fileNameFromPath(path)

def makeAbsWindowsPath(path:str):
    cwd = os.getcwd()
    return cwd + "\\" + path.replace('/','\\')


class FileManager:
    watchPeriodSeconds = 0.1
    backupCount = 30
    asmPathList = []
    rootSearchPath = []
    asmModifiedTime = []
    def __init__(self,rootSearchPath):
        self.rootSearchPath = rootSearchPath
        self.getPaths()
        self.asmModifiedTime = self.getModifiedTimeList()
        os.makedirs('./MCS-Format Backup', exist_ok=True)
        self.cout()
        self.backupFiles()
        self.formatFiles()


        firstRunFlag =1 
        while 1:
            newTimes = self.getModifiedTimeList()
            if firstRunFlag == 1:
                self.asmModifiedTime = newTimes
                firstRunFlag = 0 
                
            self.getPaths()
            #if mismatch detected (e.g user adds/deletes file) format all
            if len(newTimes) != len(self.asmModifiedTime):
                self.cout()
                self.formatFiles()
            else:
                for i,(oldTime,newTime) in enumerate(zip(self.asmModifiedTime,newTimes)):
                    if(oldTime!=newTime):
                        self.backupFile(self.asmPathList[i],self.generateBackupPath(self.asmPathList[i]))
                        Format(self.asmPathList[i])
            self.asmModifiedTime = self.getModifiedTimeList() 
            time.sleep(self.watchPeriodSeconds)

    def cout(self):
        msg = f"MCS-Format is watching \"{self.rootSearchPath}\"\nand it's subfolders for changes to .asm files.\n{len(self.asmPathList)} Files found."
        print(msg)
        print(f"Backups will be saved to ./MCS-Format Backup/**/*.asm")


    def getPaths(self):
    
        fixPath(self.rootSearchPath)
        self.asmPathList = glob.glob(self.rootSearchPath + '/**/*.asm', recursive=True)

    def getModifiedTimeList(self):
        ret = []
        for path in self.asmPathList:
            try:
               ret.append(os.stat(path).st_mtime)
            except:
                ret.append(0)
                print(f"WARN: cannot update file time for {path}")
        return ret


    def formatFiles(self):
        self.backupFiles()
        for path in self.asmPathList:
            Format(path)

    def generateBackupPath(self,path):
        backupTime = time.time()
        folderName = folderNameFromPath(path)
        fileName = fileNameFromPath(path)
        os.makedirs(f'./MCS-Format Backup/{folderName}/{fileName.replace(".asm","")}',exist_ok=True)
        bkupFileName = fileName.replace('.asm',f'{backupTime}.asm')
        bkupFileName = f'MCS-Format Backup/{folderName}/{fileName.replace("asm","")}/{bkupFileName}'
        bkupFileName = makeAbsWindowsPath(bkupFileName)
        return bkupFileName

    def generateBackupPaths(self):
        backupTime = time.time()
        backupPathList = []
        for path in self.asmPathList:
            bkupFileName = self.generateBackupPath(path)
            backupPathList.append(bkupFileName)
        return backupPathList

    def backupFile(self,asmFilePath,backUpPath):
            command = f'copy "{asmFilePath}" "{backUpPath}">nul'
            os.system(command)
            backUpPath = backUpPath[::-1]
            for i,curChar in enumerate(backUpPath):
                if curChar != '\\':
                    backUpPath = backUpPath[1:]
                else:
                    backUpPath = backUpPath[1:]
                    backUpPath = backUpPath[::-1]
                    break
                    
            backUpFilesList = glob.glob(backUpPath+"/*.asm")
            if len(backUpFilesList) > self.backupCount:
                backUpFilesList.sort()
                stopIndex = len(backUpFilesList) - self.backupCount
                backUpFilesRemoveList = backUpFilesList[:stopIndex]
                for path in backUpFilesRemoveList:
                    os.remove(path)

    def backupFiles(self):
        backupPathList = self.generateBackupPaths()
        for path,backUpPath in zip(self.asmPathList,backupPathList):
            self.backupFile(path,backUpPath)