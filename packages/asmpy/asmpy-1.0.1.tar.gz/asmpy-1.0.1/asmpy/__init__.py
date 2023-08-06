'''
  mmm    mmm   mmmmm  mmmm   m   m
 "   #  #   "  # # #  #" "#  "m m"
 m"""#   """m  # # #  #   #   #m#
 "mm"#  "mmm"  # # #  ##m#"   "#
                      #       m"
                      "      ""
ASMpy - is python backend for nasm, yasm.

'''

cmd = ''

def move(register, value):
    global cmd
    cmd+="mov "+register+", "+value+"\n"
def interrupt(code):
    global cmd
    cmd+="int "+code+"\n"
def mkboot():
    global cmd
    cmd+="times 510-($-$$) db 0\ndw 0xAA55\n"
def lodsb():
    global cmd
    cmd+="lodsb\n"
def printchar(char):
    move("AH","0x0e")
    move("AL","'"+char+"'")
    interrupt("0x10")
def printchar_f(char):
    move("AL","'"+char+"'")
    interrupt("0x10")
def initvideo():
    move("AH","0x0e")
def jump(to):
    global cmd
    cmd+="jmp "+to+"\n"
def call(to):
    global cmd
    cmd+="call "+to+"\n"
def printtext(text):
    for i in text:
        printchar(i)
def printtext_f(text):
    for i in text:
        printchar_f(i)
def db(value):
    global cmd
    cmd+="db "+value+"\n"
def dw(value):
    global cmd
    cmd+="dw "+value+"\n"
def dr(value):
    global cmd
    cmd+="dr "+value+"\n"
def do(value):
    global cmd
    cmd+="do "+value+"\n"
def compare(val, val1):
    global cmd
    cmd+="cmp "+val+", "+val1+"\n"
def je(sect):
    global cmd
    cmd+="je "+sect+"\n"
def jo(sect):
    global cmd
    cmd+="jo "+sect+"\n"
def jz(sect):
    global cmd
    cmd+="jz "+sect+"\n"
def halt():
    global cmd
    cmd+="hlt\n"
def push(value):
    global cmd
    cmd+="push "+value+"\n"
def pop(value):
    global cmd
    cmd+="pop "+value+"\n"
def pusha():
    global cmd
    cmd+="pusha\n"
def popa():
    global cmd
    cmd+="popa\n"
def include(f):
    global cmd;
    cmd+="%include "+f+"\n"
def putreturn():
    move("AL","0x0d");
    interrupt("0x10");
def int10h():
    interrupt("0x10")
def inc(val):
    global cmd
    cmd+="inc "+val+"\n"
def execute(stri):
    global cmd
    cmd+=stri+"\n"