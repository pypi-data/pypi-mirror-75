import argparse

def msg(name=None):                                                            
    return '''copy views
         [-h, display help message]
         [-f, filter out target columns]
         [-r, rename target]
        '''

def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="log to console", action="store_true")
    parser.add_argument("-s", "--safe", help="ask for confirmation before executing copy operations", action="store_true")
    parser.add_argument("-c", "--configuration", help="re-input configuration values", action="store_true")
    parser.add_argument("-e", "--echo", help="echo configuration values", action="store_true")
    parser.add_argument("-v", "--version", help="display snowctl version", action="store_true")
    return parser.parse_args()

def cmd_parser(user_input):
    parser = argparse.ArgumentParser(usage=msg())
    parser.add_argument("-f", "--filter", help="filter columns in target views", action="store_true")
    parser.add_argument("-r", "--rename", help="rename target views", action="store_true")
    args, unknown = parser.parse_known_args(user_input)
    return args
