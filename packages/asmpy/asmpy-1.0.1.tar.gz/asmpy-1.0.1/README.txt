ASMpy is a python backend for nasm or yasm.
It makes easy to writing operating systems.

I renamed these instructions:

jmp - jump
mov - move
hlt - halt
int - interrupt
cmp - compare

And added functions:

mkboot - alias for "times 510-($-$$) db 0" and "dw 0xAA55" (makes bootloader)
printchar - prints a one symbol
printchar_f - prints a one symbol without "mov AH, 0x0e" (before it you must call initvideo())
initvideo - alias for "mov AH, 0x0e" (tty mode)
printtext - prints a text
printtext_f - same as printtext

cmd - is a buffer

Example:

import asmpy

asmpy.printtext("Hello world!!!");
asmpy.mkboot()

open("hello_world.asm","w").write(asmpy.cmd)

And you get a hello_world.asm file.
Compile it with nasm or yasm:

nasm hello_world.asm

Run your program with qemu:

qemu-system-x86_64 hello_world

You get a Hello world on BIOS!