# Buffer Overflow (BOF)

## Background
In this project, we exploited a vulnerability to gain root permissions.
The program we attacked is sudo - a standard program included on Unix systems, and
used to execute commands with root permissions.
* Like most file systems, each file is owned by a user/group
* One of the permissions bits on a file is the setuid bit
* When set, this bit causes a program to automatically run under the
permissions of the user owning the file
* The sudo program is owned by the root user and has the setuid bit on
* When a user tries to use sudo, it checks the user belongs to the sudo’ers user
group, and then executes the command
It should now be clear why it’s attractive to attack the sudo program. With our goal
set clearly, let’s begin

## Cracking sudo
We have a [sudo](q1/sudo.c) program, which receives a password and executes a command as root iff the password is correct.
However, you we don’t know the password… We also have the source code for the program.

The vulnerability in this code is using strcat with wrong sizes.
Since the buffer length is 20, and 10 bytes are already full and that the password is also 10 bytes long,
So we actually can get to the address buffer[20] (normally buffer[19] would be \0) and put there whatever we want.
Using IDA and the source code we can see that the variable auth is right above the buffer on the stack.
So if we overflow the buffer it actually overflows into auth.
We can see that when auth is 1 the validation returns true. 
Since auth was already initialized to zero, if we change the last bit of it to 1, it will be 1.
This would not work if auth was not initialized to zero because then the high bytes of auth (the bytes we don't have access to) will not be zero.
So using this fact, we can put in the last byte of our password the value of 1. 

## Opening Bash

### Crashing sudo
In order to open bash we need to understand how the program works. We do it by crashing it. We're crashing the program and generating a core dump. 
We then can open the core dump using GDB and understand how the buffer is arranged.

The vulnerability here is that there is an unsafe use of strcat.
There is no length checking for the password and it is passed into the strcat as is, and a buffer overflow occured.
Using this we could just input a long password to overwrite the return address (RA) and crash the program.
We used an informative input so we would understand where the RA is by reading the stack pointer (ESP) is.
This caused a segmentation fault and generated a core dump.

### Writing the shellcode
The core dump of a program is a “snapshot” of the program memory and
registers at the point in time right when it crashed. We can open it using GDB to find some important things.

* Find where the buffer begins (let’s call this X)
* Find at which offset from the beginning of the buffer, we have the
value we want to “update” (let’s call this offset Y)
* Now, we know what we should do - create a buffer of size Y, beginning
with the shellcode, followed by padding (if needed) until we reach a
length of Y, and then finally add the address X.
* Now, the final part is writing the shellcode. This was done here by making a syscall to execve

After crashing the program and creating a core file, we read it using gdb.
We crashed the program with an easy to identify input, this way we can identify the addresses of the registers.
We used GDB to find the address of the beginning of the buffer (by looking at the address of the first byte of the input).
Also using GDB, we can find the address where instruction pointer (EIP) is pointing to (the address of EIP when the program crashed).
By substracting those two values we can find out what is the offset from the beginning of the buffer to the return address (RA).
Inside this offset we put our shellcode and in RA we put the address of the beginning of the buffer.
also a small nop slide was used to make sure we don't miss anything in the shellcode.
The shellcode was written in assembly, it was important not to write any 0's otherwise the strcat would stop cat'ing and the RA would not be overwritten.
the shellcode is bassically: execve(/bin/sh, [/bin/sh, null], [null]) since these are the parameters needed to execve.
to create 0's (or null) we used xor of a register with itself, and by doing that the shellcode did not contain 0's.
After the shellcode we still had some space until the RA so it was padded with nop's.

And finally the password that was inputed was: nop_slide + shellcode + nop_padding + address_of_beginning_of_buffer.
By using this we achieved root access.











