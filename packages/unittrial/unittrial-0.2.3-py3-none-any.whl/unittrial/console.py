import re, sys
from os import system


class Console:
    _primed = False
    indention = 0
    indention_char = '   '

    ansiRegex = re.compile(r"\x1b\[\d+(m|;\d+m)")

    Black = '\x1b[30m'
    Red = '\x1b[31m'
    Green = '\x1b[32m'
    Yellow = '\x1b[33m'
    Blue = '\x1b[34m'
    Magenta = '\x1b[35m'
    Cyan = '\x1b[36m'
    White = '\x1b[37m'
    Reset = '\x1b[0m'

    BrightBlack = '\x1b[30;1m'
    BrightRed = '\x1b[31;1m'
    BrightGreen = '\x1b[32;1m'
    BrightYellow = '\x1b[33;1m'
    BrightBlue = '\x1b[34;1m'
    BrightMagenta = '\x1b[35;1m'
    BrightCyan = '\x1b[36;1m'
    BrightWhite = '\x1b[37;1m'

    BackgroundBlack = '\x1b[40m'
    BackgroundRed = '\x1b[41m'
    BackgroundGreen = '\x1b[42m'
    BackgroundYellow = '\x1b[43m'
    BackgroundBlue = '\x1b[44m'
    BackgroundMagenta = '\x1b[45m'
    BackgroundCyan = '\x1b[46m'
    BackgroundWhite = '\x1b[47m'

    @staticmethod
    def clear():
        system('cls')

    @staticmethod
    def writeError(msg):
        Console.write(f"{Console.BrightRed}{msg}")

    @staticmethod
    def formatStatus(msg: str, status: str, width=80):
        msgCopy = Console.ansiRegex.sub("", msg.strip())
        statusCopy = Console.ansiRegex.sub("", status.strip())
        indention = Console.indention_char * Console.indention
        return Console.BrightWhite + msg + (" " * (width - (len(msgCopy) + len(statusCopy) + len(indention)))) + f"{Console.BrightWhite}[{status}{Console.BrightWhite}]"

    @staticmethod
    def update(msg):
        sys.stdout.write('\r' + (Console.indention_char * Console.indention) + msg + Console.Reset)

    @staticmethod
    def updateStatus(msg: str, status, width=75):
        Console.update(Console.formatStatus(msg, status, width))

    @staticmethod
    def write(msg):
        sys.stdout.write(('\n' if Console._primed else '') + (Console.indention_char * Console.indention) + msg + Console.Reset)
        Console._primed = True

    @staticmethod
    def writeLines(msgs: list):
        for msg in msgs:
            Console.write(msg)

    @staticmethod
    def writeStatus(msg: str, status, width=75):
        Console.write(Console.formatStatus(msg, status, width))


if __name__ == '__main__':
    sys.stdout.write(f"{Console.Blue}Test{Console.Reset}\n")

