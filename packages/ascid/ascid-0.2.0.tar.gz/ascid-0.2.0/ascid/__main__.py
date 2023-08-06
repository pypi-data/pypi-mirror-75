import argparse
import sys

from .ascid import find_repeating_strings


def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(description='ascid is the self-referential cycle identifier')

    parser.add_argument(
        'FILE',
        nargs='?',
        type=argparse.FileType('r'),
        default=sys.stdin,
        help='the file to analyze (or STDIN if omitted)'
    )

    args = parser.parse_args(argv[1:])

    all_tty = sys.stderr.isatty() == sys.stdout.isatty()

    try:
        s, offsets = find_repeating_strings(args.FILE.read())

        if all_tty:
            sys.stderr.write("Found %i occurrences of the following string at offsets %s:\n" % (len(offsets), offsets))
            sys.stderr.flush()
        # Write the actuall offsets to STDOUT, but then clear them using STDERR to hide the output
        for offset in offsets:
            sys.stdout.write("%s" % offset)
            if all_tty:
                sys.stdout.flush()
                sys.stderr.write("\r%s\r" % (' ' * len(str(offset))))
                sys.stderr.flush()
            sys.stdout.write('\n')
            if all_tty:
                sys.stdout.flush()
                # Move the cursor up a line
                sys.stderr.write('\033[1A')
                sys.stderr.flush()
        if all_tty:
            sys.stderr.write("%s\n" % repr(s))
    except KeyboardInterrupt:
        pass
