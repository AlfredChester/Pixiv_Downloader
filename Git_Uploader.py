try:
    from subprocess import Popen, PIPE
    from parse import compile
    from loguru import logger

except ImportError:
    from os import system
    __libs__ = [
        "subprocess",
        "loguru",
        "parse"
    ]
    for name in __libs__:
        try:
            system("pip install " + name)
        except Exception:
            continue

class Main:
    NormalBranch  = compile("  {}\n")
    CurrentBranch = compile("* {}\n")
    modifiedExpr  = compile("{}:   {}\n")
    def runAndGet(command:str) -> list:
        return Popen(
            command, shell = True, stdout = PIPE
        ).stdout.readlines()

    def force_decode(route_info :str) -> str:
        route_info = route_info.replace("\"","")    # Remove the '"'s on both sides
        retval = "."
        for sec in route_info.split("/"):
            sec = f"b'{sec}'"
            sec = eval(sec)
            retval += "\\" + str(sec,encoding='utf-8')
        return retval

    def checkBranch() -> list:
        # 返回(当前branch,其他branch)
        _ret = ["",[]]
        for reads in Main.runAndGet("git branch"):
            reads = reads.decode('utf-8')
            NormalParseResult  = Main.NormalBranch.parse(reads)
            SpecialParseResult = Main.CurrentBranch.parse(reads)
            if NormalParseResult != None:
                _ret[1].append(NormalParseResult[0])
            else:
                _ret[0] = SpecialParseResult[0]
        return _ret

    def findCommits() -> list:
        _ret = []
        commandOut = Main.runAndGet("git status")
        for line in commandOut:
            line = line.decode("utf-8")
            logger.info(line.replace("\n",""))
            __ParseResult = Main.modifiedExpr.parse(line)
            if __ParseResult != None:
                if not "renamed" in __ParseResult[0]:
                    _ret.append(__ParseResult[1])
                else:
                    _ret.append(__ParseResult[1].split(' ')[3])
        return _ret

    def main() -> None:
        logger.add(".\\Uploader_log\\file-{time:YYYY-MM-DD}.log", retention="1 day")
        logger.info("欢迎来到Git上传工具")
        # 首先检查当前的分支:
        CheckResult = Main.checkBranch()
        currentBranch = CheckResult[0]
        otherBranches = CheckResult[1]
        logger.info("当前分支: " + str(currentBranch))
        logger.info("其他分支: " + str(otherBranches))
        IfChange = input("是否切换到其他分支? ")
        if IfChange == 'Y' or IfChange == 'y':
            WhichToChange = input("切换到哪个分支? ")
            if WhichToChange in otherBranches:
                Main.runAndGet("git checkout " + WhichToChange)
            else:
                logger.info("NoSence!!!")
                return
        else:
            WhichToChange = currentBranch
        Main.runAndGet("git add .")
        # check which to commit
        commitResult = Main.findCommits()
        logger.info("更改过的文件: " + str(commitResult))
        for name in commitResult:
            name = name.split()[0]
            if(isinstance(name,str)):
                name = Main.force_decode(name)
                logger.info("Decoded: " + name)
            currentCommit = input(f"请输入对 {name} 的commit: ").replace('"','\\"')
            Main.runAndGet(f'git commit "{name}" -m "{currentCommit}"')
        checkIfPush = input("是否推送到GitHub? ")
        if checkIfPush != 'N' and checkIfPush != 'n':
            Main.runAndGet("git push origin " + WhichToChange)
        if IfChange == 'Y' or IfChange == 'y':
            returnToBranch = input("是否回退到原来的分支? ")
            if returnToBranch != 'N' and returnToBranch != 'n':
                Main.runAndGet("git checkout " + currentBranch)
        return

if __name__ == '__main__':
    Main.main()
    logger.info("Program exited")
    exit(0)
    