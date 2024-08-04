import tkinter as tk

# global variable
t0Num = 0
t1Num = 0
s0Num = 0
s1Num = 0
raNum = 0

instArr = ["lw", "sw",
           "add", "addi", "addu", "addiu", "sub",
           "sll", "srl",
           "and", "or", "nor",
           "beq", "bne",
           "slt", "slti", "sltu",
           "j", "jal", "jr"]

regArr = ["$a0", "$a1", "$a2", "$a3",
          "$v0", "$v1",
          "$t0", "$t1", "$t2", "$t3", "$t4", "$t5", "$t6", "$t7", "$t8", "$t9",
          "$s0", "$s1", "$s2", "$s3", "$s4", "$s5", "$s6", "$s7",
          "$k0", "$k1",
          "$at", "$gp", "$sp", "$fp", "$ra", "$zero",
          "$0", "$1", "$2", "$3", "$4", "$5", "$6", "$7", "$8", "$9",
          "$10", "$11", "$12", "$13", "$14", "$15", "$16", "$17", "$18", "$19",
          "$20", "$21", "$22", "$23", "$24", "$25", "$26", "$27", "$28", "$29",
          "$30", "$31"]

labelDic = {}

dataMem = {"0": 0}  # 4位記錄一次，十進制紀錄
addressBin = "None"  # 用於顯示data memory結果

# 讀取code.txt中指令
f = open('C:/Users/Chavon/Desktop/HomeWorkProjects/example/其他/MIPS/code.txt', 'r')
allCommand = f.read()
commandArr = allCommand.split('\n')
f.close()
commandLine = 0  # 正在執行的指令行數

# 判斷是否需要Label
needLabel = False
for i in range(len(commandArr)):
    if commandArr[i][0] == ' ':
        needLabel = True
        break
# 紀錄Label
if needLabel == True:
    for i in range(len(commandArr)):
        if commandArr[i][0] == ' ':
            while commandArr[i][0] == ' ':
                commandArr[i] = commandArr[i][1:]
        else:
            labelName = ""
            while commandArr[i][0] != ' ' and commandArr[i][0] != ':':
                labelName += commandArr[i][0]
                commandArr[i] = commandArr[i][1:]
            commandArr[i] = commandArr[i][1:]  # delete ':'
            while commandArr[i][0] == ' ':
                commandArr[i] = commandArr[i][1:]
            labelDic.update({labelName: i})


def checkInst(inst):
    instExist = False
    for i in range(len(instArr)):
        if inst == instArr[i]:
            instExist = True
            break
    return instExist


def checkReg(reg):
    regExist = False
    for i in range(len(regArr)):
        if reg == regArr[i]:
            regExist = True
            break
    return regExist


def instType(inst):
    returnType = ""

    if inst == "add" or inst == "addu" or inst == "sub" or inst == "and" or inst == "or" or inst == "nor" or inst == "slt" or inst == "sltu" or inst == "sll" or inst == "srl":
        returnType = "RType"
    elif inst == "addi" or inst == "addiu" or inst == "slti":
        returnType = "IType_arithmetic"
    elif inst == "beq" or inst == "bne":
        returnType = "IType_branch"
    elif inst == "j" or inst == "jal":
        returnType = "JType"
    elif inst == "lw":      # I format
        returnType = "lw"
    elif inst == "sw":      # I format
        returnType = "sw"
    elif inst == "jr":      # R format
        returnType = "jr"

    return returnType


def RtypeBin(instR):
    returnStr = ""        # opR:[16:11] shamt:[10:6] funct:[5:0]
    opR = ""
    shamt = ""
    funct = ""
    if instR == "add":
        opR = "000000"
        shamt = "00000"
        funct = "100000"
    elif instR == "addu":
        opR = "000000"
        shamt = "00000"
        funct = "100001"
    elif instR == "sub":
        opR = "000000"
        shamt = "00000"
        funct = "100010"
    elif instR == "and":
        opR = "000000"
        shamt = "00000"
        funct = "100100"
    elif instR == "or":
        opR = "000000"
        shamt = "00000"
        funct = "100101"
    elif instR == "nor":
        opR = "000000"
        shamt = "00000"
        funct = "100111"
    elif instR == "slt":
        opR = "000000"
        shamt = "00000"
        funct = "101010"
    elif instR == "sltu":
        opR = "000000"
        shamt = "00000"
        funct = "101011"
    elif instR == "sll":
        opR = "000000"
        shamt = "SLNum"
        funct = "000000"
    elif instR == "srl":
        opR = "000000"
        shamt = "SRNum"
        funct = "000010"
    elif instR == "jr":
        opR = "000000"
        shamt = "00000"
        funct = "001000"

    returnStr = opR+","+shamt+","+funct
    return returnStr


def ItypeBin(instI):
    opI = ""
    if instI == "addi":
        opI = "001000"
    elif instI == "addiu":
        opI = "001001"
    elif instI == "slti":
        opI = "001010"
    elif instI == "beq":
        opI = "000100"
    elif instI == "bne":
        opI = "000101"
    elif instI == "lw":
        opI = "100011"
    elif instI == "sw":
        opI = "101011"

    return opI


def JtypeBin(instJ):
    opJ = ""
    if instJ == "j":
        opJ = "000010"
    elif instJ == "jal":
        opJ = "000011"

    return opJ


def regBin(tarReg):
    if tarReg == "$0" or tarReg == "$zero":
        return "00000"
    elif tarReg == "$1" or tarReg == "$at":
        return "00001"
    elif tarReg == "$2" or tarReg == "$v0":
        return "00010"
    elif tarReg == "$3" or tarReg == "$v1":
        return "00011"
    elif tarReg == "$4" or tarReg == "$a0":
        return "00100"
    elif tarReg == "$5" or tarReg == "$a1":
        return "00101"
    elif tarReg == "$6" or tarReg == "$a2":
        return "00110"
    elif tarReg == "$7" or tarReg == "$a3":
        return "00111"
    elif tarReg == "$8" or tarReg == "$t0":
        return "01000"
    elif tarReg == "$9" or tarReg == "$t1":
        return "01001"
    elif tarReg == "$10" or tarReg == "$t2":
        return "01010"
    elif tarReg == "$11" or tarReg == "$t3":
        return "01011"
    elif tarReg == "$12" or tarReg == "$t4":
        return "01100"
    elif tarReg == "$13" or tarReg == "$t5":
        return "01101"
    elif tarReg == "$14" or tarReg == "$t6":
        return "01110"
    elif tarReg == "$15" or tarReg == "$t7":
        return "01111"
    elif tarReg == "$16" or tarReg == "$s0":
        return "10000"
    elif tarReg == "$17" or tarReg == "$s1":
        return "10001"
    elif tarReg == "$18" or tarReg == "$s2":
        return "10010"
    elif tarReg == "$19" or tarReg == "$s3":
        return "10011"
    elif tarReg == "$20" or tarReg == "$s4":
        return "10100"
    elif tarReg == "$21" or tarReg == "$s5":
        return "10101"
    elif tarReg == "$22" or tarReg == "$s6":
        return "10110"
    elif tarReg == "$23" or tarReg == "$s7":
        return "10111"
    elif tarReg == "$24" or tarReg == "$t8":
        return "11000"
    elif tarReg == "$25" or tarReg == "$t9":
        return "11001"
    elif tarReg == "$26" or tarReg == "$k0":
        return "11010"
    elif tarReg == "$27" or tarReg == "$k1":
        return "11011"
    elif tarReg == "$28" or tarReg == "$gp":
        return "11100"
    elif tarReg == "$29" or tarReg == "$sp":
        return "11101"
    elif tarReg == "$30" or tarReg == "$fp":
        return "11110"
    elif tarReg == "$31" or tarReg == "$ra":
        return "11111"


def iBin(tarI, tarSign, intLen, isNeg):
    if isNeg:
        tarI = tarI.replace('-', '')
    tarINum = int(tarI)
    if isNeg:
        returnI = bin(tarINum-1)
        returnI = returnI.replace('1', '2')
        returnI = returnI.replace('0', '1')
        returnI = returnI.replace('2', '0')
    else:
        returnI = bin(tarINum)
    returnI = returnI.replace('b', '')
    returnText = str(returnI)
    n = len(returnText)
    if n < intLen:
        if tarSign == "Signed":
            if isNeg:
                for i in range(intLen-n):
                    returnText = '1'+returnText
            else:
                for i in range(intLen-n):
                    returnText = '0'+returnText
        else:
            for i in range(intLen-n):
                returnText = '0'+returnText

    if len(returnText) > intLen:
        returnText = returnText[1:]
    return returnText


def instCaculate_R(inst, destName, src1Name, src2Name):  # add rd, rs, rt
    global t0Num, t1Num, s0Num, s1Num
    # 利用變數名稱取值
    if src1Name == "$t0" or src1Name == "$8":
        src1 = t0Num
    elif src1Name == "$t1" or src1Name == "$9":
        src1 = t1Num
    elif src1Name == "$s0" or src1Name == "$16":
        src1 = s0Num
    elif src1Name == "$s1" or src1Name == "$17":
        src1 = s1Num
    if src2Name == "$t0" or src2Name == "$8":
        src2 = t0Num
    elif src2Name == "$t1" or src2Name == "$9":
        src2 = t1Num
    elif src2Name == "$s0" or src2Name == "$16":
        src2 = s0Num
    elif src2Name == "$s1" or src2Name == "$17":
        src2 = s1Num
    else:
        src2 = src2Name

    # 計算
    if inst == "add":
        dest = src1+src2
    elif inst == "addu":
        dest = src1+src2
    elif inst == "sub":
        dest = src1-src2
    elif inst == "and":
        dest = src1 & src2
    elif inst == "or":
        dest = src1 | src2
    elif inst == "nor":
        dest = ~(src1 | src2)
    elif inst == "slt":
        if src1 < src2:
            dest = 1
        else:
            dest = 0
    elif inst == "sltu":
        if src1 < src2:
            dest = 1
        else:
            dest = 0
    elif inst == "sll":
        dest = src1 << int(src2)
    elif inst == "srl":
        dest = src1 >> int(src2)

    # 賦值
    if destName == "$t0" or destName == "$8":
        t0Num = dest
    elif destName == "$t1" or destName == "$9":
        t1Num = dest
    elif destName == "$s0" or destName == "$16":
        s0Num = dest
    elif destName == "$s1" or destName == "$17":
        s1Num = dest


def instCaculate_I(inst, destName, srcName, num):  # addi rt, rs, immed
    global t0Num, t1Num, s0Num, s1Num
    # 利用變數名稱取值
    num = int(num)
    if srcName == "$t0" or srcName == "$8":
        src = t0Num
    elif srcName == "$t1" or srcName == "$9":
        src = t1Num
    elif srcName == "$s0" or srcName == "$16":
        src = s0Num
    elif srcName == "$s1" or srcName == "$17":
        src = s1Num

    # 計算
    if inst == "addi":
        dest = src+num
    elif inst == "addiu":
        dest = src+num
    elif inst == "slti":
        if src < num:
            dest = 1
        else:
            dest = 0

    # 賦值
    if destName == "$t0" or destName == "$8":
        t0Num = dest
    elif destName == "$t1" or destName == "$9":
        t1Num = dest
    elif destName == "$s0" or destName == "$16":
        s0Num = dest
    elif destName == "$s1" or destName == "$17":
        s1Num = dest


def instCaculate_BeqBne(inst, src1Name, src2Name, label):
    global t0Num, t1Num, s0Num, s1Num, commandLine, labelDic
    # 利用變數名稱取值
    if src1Name == "$t0" or src1Name == "$8":
        src1 = t0Num
    elif src1Name == "$t1" or src1Name == "$9":
        src1 = t1Num
    elif src1Name == "$s0" or src1Name == "$16":
        src1 = s0Num
    elif src1Name == "$s1" or src1Name == "$17":
        src1 = s1Num
    if src2Name == "$t0" or src2Name == "$8":
        src2 = t0Num
    elif src2Name == "$t1" or src2Name == "$9":
        src2 = t1Num
    elif src2Name == "$s0" or src2Name == "$16":
        src2 = s0Num
    elif src2Name == "$s1" or src2Name == "$17":
        src2 = s1Num

    # 計算
    if inst == "beq":
        if src1 == src2:
            commandLine = labelDic[label]-1
    elif inst == "bne":
        if src1 != src2:
            commandLine = labelDic[label]-1


def instCaculate_LwSw(inst, destName, srcName, num):  # haven't done
    global t0Num, t1Num, s0Num, s1Num, dataMem, addressBin
    # 利用變數名稱取值
    num = int(num)
    if srcName == "$t0" or srcName == "$8":
        src = t0Num
    elif srcName == "$t1" or srcName == "$9":
        src = t1Num
    elif srcName == "$s0" or srcName == "$16":
        src = s0Num
    elif srcName == "$s1" or srcName == "$17":
        src = s1Num

    # 計算 + 賦值
    dataMemAddr = 0
    if inst == "lw":
        dataMemAddr = num+src
        dest = dataMem[dataMemAddr]
        # 賦值
        if destName == "$t0" or destName == "$8":
            t0Num = dest
        elif destName == "$t1" or destName == "9":
            t1Num = dest
        elif destName == "$s0" or destName == "$16":
            s0Num = dest
        elif destName == "$s1" or destName == "$17":
            s1Num = dest
    elif inst == "sw":
        dataMemAddr = num+src
        # 取值
        if destName == "$t0" or destName == "$8":
            dest = t0Num
        elif destName == "$t1" or destName == "$9":
            dest = t1Num
        elif destName == "$s0" or destName == "$16":
            dest = s0Num
        elif destName == "$s1" or destName == "$17":
            dest = s1Num
        dataMem.update({dataMemAddr: dest})

    # 處理data memory顯示
    destBin = iBin(dest, "Signed", 32, dest < 0)
    addressBin = "MEM["+iBin(dataMemAddr, "Unsigned",
                             32, False)+"] = "+destBin[0:8]+"\n"
    addressBin += "MEM["+iBin(dataMemAddr+1, "Unsigned",
                              32, False)+"] = "+destBin[8:16]+"\n"
    addressBin += "MEM["+iBin(dataMemAddr+2, "Unsigned",
                              32, False)+"] = "+destBin[16:24]+"\n"
    addressBin += "MEM["+iBin(dataMemAddr+3, "Unsigned",
                              32, False)+"] = "+destBin[24:32]+"\n"


def instCaculate_J(inst, label):
    global raNum, commandLine, labelDic

    if inst == "j":
        commandLine = labelDic[label]-1
    elif inst == "jal":
        raNum = commandLine
        commandLine = labelDic[label]-1


def instCaculate_Jr():
    global commandLine, raNum
    commandLine = raNum


def cmdAnalyze(myCommand):
    global addressBin
    resultText.delete(1.0, 'end')
    instAns = ""
    destAns = ""
    sourceAns = ""
    immAns = ""
    machineCodeText = ""
    theDest = 'dest'
    theSource = ['s1', 's2']
    theArr = ['inst', 'dest', 's1', 's2']
    regBool = True
    formatBool = True

    # split command
    chCommand = myCommand.replace(',', ' ')
    tmpArr = chCommand.split(' ')
    regNum = len(tmpArr)
    theArr[0:regNum-1] = tmpArr
    theInst = theArr[0]
    theDest = theArr[1]

    # check inst
    instBool = checkInst(theInst)
    if instBool == False:
        resultText.insert("insert", "Instruction Error\n")
    else:
        theInstType = instType(theInst)

    # Signed or Unsigned
    if theInst == "addu" or theInst == "addiu" or theInst == "sltu":
        signType = "Unsigned"
    else:
        signType = "Signed"

    # check format - number of participant
    if theInstType == "RType" or theInstType == "IType_arithmetic" or theInstType == "IType_branch":
        if regNum != 4:
            formatBool = False
        else:
            theSource[0] = theArr[2]
            theSource[1] = theArr[3]
    elif theInstType == "lw" or theInstType == "sw":
        if regNum != 3:
            formatBool = False
        else:
            theSource[0] = theArr[2]
    elif theInstType == "JType" or theInstType == "jr":
        if regNum != 2:
            formatBool = False

    # check format - isn't number or out of the range
    isNeg = False
    if theInstType == "IType_arithmetic":
        if '-' in theSource[1]:
            if signType == "Unsigned":
                formatBool = False
            else:
                isNeg = True
                theSource[1] = theSource[1].replace('-', '')

        if theSource[1].isdigit() == False:
            formatBool = False
        elif signType == "Unsigned":      # Unsigned:0 ~ (2^n)-1
            if int(theSource[1]) >= (2**16):
                formatBool = False
        elif signType == "Signed":        # Signed:-2^(n-1) ~ 2^(n-1)-1
            if isNeg == True and int(theSource[1]) > (2**15):
                formatBool = False
            elif isNeg == False and int(theSource[1]) >= (2 ** 15):
                formatBool = False

        if isNeg:  # 還回去
            theSource[1] = '-'+theSource[1]
    # elif theInstType == "JType":
        # if theDest.isdigit() == False or int(theDest) >= (2 ** 26):
            #formatBool = False

    # check register
    if theInstType == "RType":
        regBool = checkReg(theDest)
        regBool = regBool & checkReg(theSource[0])
        if theInst == "sll" or theInst == "srl":
            if theSource[1].isdigit() == False:
                formatBool = False
            elif int(theSource[1]) >= 2**5:
                formatBool = False
        else:
            regBool = regBool & checkReg(theSource[1])
    elif theInstType == "IType_arithmetic" or theInstType == "IType_branch":
        regBool = checkReg(theDest)
        regBool = regBool & checkReg(theSource[0])
    elif theInstType == "lw" or theInstType == "sw" or theInstType == "jr":
        regBool = checkReg(theDest)

    # sw、lw : 檢查、更改source格式
    if theInst == "lw" or theInst == "sw":
        srcTmp = theSource[0]
        if "(" not in srcTmp:
            formatBool = False
        elif ")" not in srcTmp:
            formatBool = False
        else:
            srcTmp = srcTmp.replace(")", "")
            srcTmpArr = srcTmp.split("(")
            if len(srcTmpArr) != 2:         # 格式有缺失
                formatBool = False
            else:
                # not Natural number or out of the range
                if srcTmpArr[0].isdigit() == False or int(srcTmpArr[0]) >= (2**16):
                    formatBool = False
                else:
                    rmd = int(srcTmpArr[0]) % 4
                    if rmd != 0:
                        resultText.insert(
                            "insert", "Warning: Offset is not a multiple of four\n")
                if checkReg(srcTmpArr[1]) == False:   # wrong register
                    regBool = False
                else:
                    wNum = srcTmpArr[0]
                    wReg = srcTmpArr[1]

    # 顯示錯誤訊息
    if formatBool == False:
        resultText.insert("insert", "Format Error\n")
    if regBool == False:
        resultText.insert("insert", "Register Error\n")

    # 如果格式都正確 -> caculate & show the result
    if instBool and formatBool and regBool:
        instAns = ""
        sourceAns = ""
        destAns = ""

        if theInstType == "lw":
            instAns = "Instruction: "+theInst+"\n"
            destAns = "Destination: "+theDest+"\n"
            sourceAns = "Source: Mem["+wReg+" + "+wNum+"]\n"
            instCaculate_LwSw(theInst, theDest, wReg, wNum)
        elif theInstType == "sw":
            instAns = "Instruction: "+theInst+"\n"
            destAns = "Destination: Mem["+wReg+" + "+wNum+"]\n"
            sourceAns = "Source: "+theDest+", "+wReg+"\n"
            instCaculate_LwSw(theInst, theDest, wReg, wNum)
        elif theInstType == "RType":
            instAns = "Instruction: "+theInst+"\n"
            destAns = "Destination: "+theDest+"\n"
            sourceAns = "Source: "+theSource[0]+", "+theSource[1]+"\n"
            instCaculate_R(theInst, theDest, theSource[0], theSource[1])
        elif theInstType == "IType_arithmetic":
            instAns = "Instruction: "+theInst+"\n"
            destAns = "Destination: "+theDest+"\n"
            sourceAns = "Source: "+theSource[0]+"\n"
            immAns = "Immediate value: "+theSource[1]+"\n"
            instCaculate_I(theInst, theDest, theSource[0], theSource[1])
        elif theInstType == "IType_branch":
            instAns = "Instruction: "+theInst+"\n"
            destAns = "Source: "+theDest+", "+theSource[0]+"\n"
            sourceAns = "Address: "+theSource[1]+"\n"
            instCaculate_BeqBne(theInst, theDest, theSource[0], theSource[1])
        elif theInstType == "JType":
            instAns = "Instruction: "+theInst+"\n"
            destAns = "Address: "+theDest+"\n"
            instCaculate_J(theInst, theDest)
        elif theInstType == "jr":
            instAns = "Instruction: "+theInst+"\n"
            destAns = "Source: "+theDest+"\n"
            instCaculate_Jr()

        # Show binary Code
        instBinCode = ""
        if theInst == "sll" or theInst == "srl":
            binCode = RtypeBin(theInst)
            binArr = binCode.split(',')
            binRd = regBin(theDest)
            binRt = regBin(theSource[0])
            binShamt = iBin(theSource[1], signType, 5, isNeg)
            machineCodeText = "(1)Opcode = "+binArr[0]+"\n(2)rs = "+"00000(not used)" + \
                "\n(3)rt = "+binRt+"\n(4)rd = "+binRd+"\n(5)Shamt = " + \
                binShamt+"\n(6)Funct = "+binArr[2]
            instBinCode = binArr[0]+"00000"+binRt+binRd+binShamt+binArr[2]
        elif theInstType == "jr":
            binCode = RtypeBin(theInst)
            binArr = binCode.split(',')
            binRs = regBin(theDest)
            machineCodeText = "(1)Opcode = "+binArr[0]+"\n(2)rs = "+binRs + \
                "\n(3)rt = 00000\n(4)rd = 00000\n(5)Shamt = " + \
                binArr[1]+"\n(6)Funct = "+binArr[2]
            instBinCode = binArr[0]+binRs+"00000"+"00000"+binArr[1]+binArr[2]
        elif theInstType == "lw":
            binOp = ItypeBin(theInst)
            binRs = regBin(wReg)
            binRt = regBin(theDest)
            binOffset = iBin(wNum, "Unsigned", 16, isNeg)
            machineCodeText = "(1)Opcode = "+binOp+"\n(2)rs = "+binRs + \
                "\n(3)rt = "+binRt+"\n(4)Offset = "+binOffset
            instBinCode = binOp+binRs+binRt+binOffset
        elif theInstType == "sw":
            binOp = ItypeBin(theInst)
            binRs = regBin(wReg)
            binRt = regBin(theDest)
            binOffset = iBin(wNum, "Unsigned", 16, isNeg)
            machineCodeText = "(1)Opcode = "+binOp+"\n(2)rs = "+binRs + \
                "\n(3)rt = "+binRt+"\n(4)Offset = "+binOffset
            instBinCode = binOp+binRs+binRt+binOffset
        elif theInstType == "RType" and theInst != "sll" and theInst != "srl" and theInstType != "jr":
            binCode = RtypeBin(theInst)
            binArr = binCode.split(',')
            binRd = regBin(theDest)
            binRs = regBin(theSource[0])
            binRt = regBin(theSource[1])
            machineCodeText = "(1)Opcode = "+binArr[0]+"\n(2)rs = "+binRs + \
                "\n(3)rt = "+binRt+"\n(4)rd = "+binRd+"\n(5)Shamt = " + \
                binArr[1]+"\n(6)Funct = "+binArr[2]
            instBinCode = binArr[0]+binRs+binRt+binRd+binArr[1]+binArr[2]
        elif theInstType == "IType_arithmetic":
            binOp = ItypeBin(theInst)
            binRt = regBin(theDest)
            binRs = regBin(theSource[0])
            binImmd = iBin(theSource[1], signType, 16, isNeg)
            machineCodeText = "(1)Opcode = "+binOp+"\n(2)rs = "+binRs + \
                "\n(3)rt = "+binRt+"\n(4)Immediate value = "+binImmd+"\n"
            instBinCode = binOp+binRs+binRt+binImmd
        elif theInstType == "IType_branch":
            binOp = ItypeBin(theInst)
            binRt = regBin(theDest)
            binRs = regBin(theSource[0])
            binAddr = iBin(labelDic[theSource[1]], signType, 16, isNeg)
            machineCodeText = "(1)Opcode = "+binOp+"\n(2)rs = "+binRs + \
                "\n(3)rt = "+binRt+"\n(4)Address = "+binAddr+"\n"
            instBinCode = binOp+binRs+binRt+binAddr
        elif theInstType == "JType":
            binOp = JtypeBin(theInst)
            binAddr = iBin(labelDic[theDest], signType, 26, isNeg)
            machineCodeText = "(1)Opcode = "+binOp + \
                "\n(2) Address = "+binAddr+"\n"
            instBinCode = binOp+binAddr
        """
        resultText.insert("insert", instAns)
        resultText.insert("insert", destAns)
        resultText.insert("insert", sourceAns)
        resultText.insert("insert", immAns)

        resultText.insert("insert", "\nBinary Code:\n")
        resultText.insert("insert", machineCodeText)
        """
        # PC
        global commandLine
        pcBin = iBin((commandLine+1)*4, "Unsigned", 32, False)
        pcAns = 'PC: '+pcBin+'\n\n'
        resultText.insert("insert", pcAns)

        # Registert File
        regFile = "Registert File:\n"
        regFile += "$t0: "+iBin(t0Num, "Signed", 32, (t0Num < 0))+'\n'
        regFile += "$t1: "+iBin(t1Num, "Signed", 32, (t1Num < 0))+'\n'
        regFile += "$s0: "+iBin(s0Num, "Signed", 32, (s0Num < 0))+'\n'
        regFile += "$s1: "+iBin(s1Num, "Signed", 32, (s1Num < 0))+'\n'
        regFile += '\n'
        resultText.insert("insert", regFile)

        # Instruction Memory
        instMem = "Instruction Memory:\n"
        mem0 = "MEM["+iBin(4*commandLine, "Unsigned", 32,
                           False)+"] = "+instBinCode[0:8]+'\n'
        mem1 = "MEM["+iBin(4*commandLine+1, "Unsigned", 32,
                           False)+"] = "+instBinCode[8:16]+'\n'
        mem2 = "MEM["+iBin(4*commandLine+2, "Unsigned", 32,
                           False)+"] = "+instBinCode[16:24]+'\n'
        mem3 = "MEM["+iBin(4*commandLine+3, "Unsigned", 32,
                           False)+"] = "+instBinCode[24:32]+'\n'
        instMem += mem0+mem1+mem2+mem3+'\n'
        resultText.insert("insert", instMem)

        # Data Memory
        dataMem = "Data Memory: \n"
        dataMem += addressBin+'\n'
        resultText.insert("insert", dataMem)


def buttonEvent():
    global commandLine, commandArr

    if commandLine < len(commandArr):
        exeCommand.delete('1.0', 'end')
        exeCommand.insert("insert", commandArr[commandLine])
        cmdAnalyze(commandArr[commandLine])
        commandLine += 1
    elif commandLine == len(commandArr):
        exeCommand.delete('1.0', 'end')
        exeCommand.insert("insert", "END")
        commandLine += 1


# GUI window
win = tk.Tk()
win.title('MIPS')
win.geometry('600x420')  # 視窗大小 寬x高
win.resizable(True, True)
win.configure(bg='#87C1F7')
while 1:
    myLabel = tk.Label(win, text="MIPS command :",
                       font=('Arial', 11), bg='#87C1F7', width=50, height=2)
    myLabel.grid(row=0, column=0)
    myButton = tk.Button(win, text="Next",
                         command=buttonEvent, bg='#E9F3AF')
    myButton.grid(row=1, column=1)
    exeCommand = tk.Text(win, bg='#E2E9B9', width=30, height=1)
    exeCommand.grid(row=1, column=0)

    # result
    decoLabel = tk.Label(win, text="", bg='#87C1F7')
    decoLabel.grid(row=2, column=0)
    resultText = tk.Text(win, bg='#87C1F7', width=60, height=21)
    resultText.grid(row=3, column=0)

    win.mainloop()  # 常駐
