"""
General wrapper for manager.py
Wrapper is intended to be executed by the manager.py per one computation job.
Wrapper could call another scripts or call specific sage methods.

Implementation is not yet finished.
"""
import argparse


def main():
    etypes = ['cli', 'method']
    parser = argparse.ArgumentParser(description='Wrapper for the sage script')
    parser.add_argument('-s', '--script', dest='script',
                        help='Sage script file to load')
    parser.add_argument('-a', '--action', dest='action', choices=etypes,
                        help='Action to perform on the sage script')
    parser.add_argument('-f', '--function', dest='function',
                        help='Function name to call')
    parser.add_argument('-j', '--json', dest='json',
                        help='JSON input to pass to the function')
    parser.add_argument('-c', '--cli', dest='cli',
                        help='Command line arguments to pass to the script')

    # parser.add_argument('-p', '--prime', action='store', help='')
    # parser.add_argument('-s', '--seed', action='store', help='')
    # parser.add_argument('-f', '--outfile', action='store', help='')
    args = parser.parse_args()

    # generate_x962_curves(args.count, args.prime, args.seed, jsonfile= args.outfile)

    if args.action == 'method':
        # Load Sage script to this namespace
        load(args.script)
        fnc = args.function


    elif args.action == 'cli':
        pass
    else:
        raise ValueError('Unknown action')


if __name__ == '__main__':
    main()
