import time 
import os
class Format:
    spacesAfterSemi = 2
    labelSize = 12
    dirInsSize = 9
    operandSize = 7
    operandPreSpacing = 2
    commentStartPos = 43


    
    def __init__(self,asmPath):
        self.asmPath = asmPath
        curTime = time.strftime('%X')
        print(f"[{curTime}]  Formatting file \"{self.asmPath}\"............",end="")
        self.format(self.asmPath)
        self.formattedLines = []
 

    def format(self,fileName):
        linesToDelete = []
        with open(fileName, 'r') as file:
            self.lines = file.read().splitlines()#.replace('\n', '')

            #replace tabs with spaces
            for i,currLine in enumerate(self.lines):
                self.lines[i] = currLine.replace('\t',' ')

            #remove leading spaces
            for i,currLine in enumerate(self.lines):
                self.lines[i] = self.removeLeadingSpaces(currLine)
            #reduce consecutive empty lines to a single empty line
            for i,currLine in enumerate(self.lines):
                try:
                    if len(currLine) ==0 and len(self.lines[i+1]) == 0:
                        linesToDelete.append(i)
                except:
                    pass
            for i in reversed( linesToDelete):
                del(self.lines[i])
        os.remove(fileName) 
        with open(fileName,'w') as output:
            for currLine in self.lines:
                output.write(f"{self.formatLine(currLine)}\n")
        print("Success")

    def formatLine(self,curLine:str):
        hasLabel = 0
        hasDirIns = 0
        dirIns = ""
        label = ""
        operands = []
        comment = ""
        returnString = ""
        targetLength = 0
        #Do nothing to empty lines
        if len(curLine) == 0:
            return curLine

        #comment only lines
        if curLine[0] == ';':
            #removes the semicolon
            return self.formatComment(curLine[1:])

        #grab regardless if there is one or not 
        temp = self.startToDelimeter(curLine,{';',':'})
        label = removeSpaces(temp[0])
        if label[-1] == ':':
            hasLabel = 1
            curLine = temp[1]
            if len(curLine) ==0:
                return label

        curLine = self.removeLeadingSpaces(curLine) 
        #grab everthing before a comment
        temp = self.startToDelimeter(curLine,{';'})
        if len(temp[1]) != 0:
            comment = self.formatComment(temp[1])
            curLine = temp[0][:-1]
            curLine = self.removePaddingSpaces(curLine)
        
        temp = self.startToDelimeter(curLine,{' '})
        if len(temp[0]) != 0:
            curLine = temp[1]
            hasDirIns =1
            dirIns = self.removePaddingSpaces(temp[0])
            dirIns = dirIns.upper()
        else:
            return curLine        
        #curLine is now operands only
        curLine = removeSpaces(curLine)
        temp = curLine.split(',')
        for i,op in enumerate(temp):
            if len(op) != 0:
                operands.append(removeSpaces(op))



        if hasLabel:
            returnString +=(label.ljust(self.labelSize) + dirIns.ljust(self.dirInsSize)) 
        else:
            returnString += (' '*self.labelSize +dirIns.ljust(self.dirInsSize))


        if len(operands) !=0 :
            firstOperand = operands.pop(0)
            returnString += firstOperand.ljust(self.operandSize)
            
        if len(operands) !=0 :
            lastOperand = ','+' '*self.operandPreSpacing +operands.pop().ljust(self.operandSize)
            if len(operands) !=0:
                for op in operands:
                    returnString+=','+' '*self.operandPreSpacing+op.ljust(self.operandSize)
            returnString+=lastOperand
        if len(comment)!= 0:
            returnString = returnString.ljust(self.commentStartPos) +' ' +comment
        if len(returnString)!=0:
            return returnString

        
        return curLine

    def removeLeadingSpaces(self,string:str):
        for curChar in string:
            if curChar !=' ':
                break
            else:
                string = string[1:]
        return string

    def formatComment(self,comment:str):
        #remove spaces at start, and at the end
        comment = self.removePaddingSpaces(comment)
        return ';'+' '*self.spacesAfterSemi+comment

    def startToDelimeter(self,string:str,delims:set): #returns tuple(str,str), where tuple[0] is the substring before delimeter, and tuple[1] is the remaining chars 
        substring = "" 
        for curChar in string:
            if curChar in delims:
                substring+=curChar
                string = string[1:]
                break
            else:
                substring+=curChar
                string = string[1:]
        return (substring,string)
    def removeTrailingSpaces(self,string:str):
        string = string[::-1]
        string = self.removeLeadingSpaces(string)
        return string [::-1]
    def removePaddingSpaces(self,string:str):
        string = self.removeLeadingSpaces(string)
        string = self.removeTrailingSpaces(string)
        return string
def removeSpaces(string:str):
    return string.replace(' ','')

