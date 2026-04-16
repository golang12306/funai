; write.S — 手动触发一次 Ring3 → Ring0 系统调用
; 编译：nasm -f elf64 write.S -o write.o && ld write.o -o write && ./write

section .data
msg db 'hello', 0x0a          ; 5个字符 + 换行符

section .text
global _start

_start:
    ; write(fd=1, buf=msg, count=5)
    ; x86_64 Linux 系统调用号：__NR_write = 1
    mov rax, 1                ; RAX = 系统调用号
    mov rdi, 1                ; RDI = fd (stdout)
    mov rsi, msg              ; RSI = 缓冲区地址
    mov rdx, 5                ; RDX = 字节数
    syscall                   ; ← 触发 Ring0 切换

    ; 退出程序
    mov rax, 60               ; __NR_exit_group = 60
    xor rdi, rdi              ; status = 0
    syscall