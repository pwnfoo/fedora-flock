from __future__ import print_function
from __future__ import absolute_import
from termcolor import colored
from six.moves import input
import os
import fedmsg
import argparse
import calendar
import fedmsg.meta
import stats
import output
from parseGroup import GroupParser


def interactive_input(args):
    stats.values['user'] = str(input("FAS Username (required) \t: ")).lower()
    stats.values['delta'] = 604800 * int(input("Number of weeks (default : 1)\t: "))
    stats.weeks = int(args.weeks)
    stats.category = str(input("Enter category (default : None)\t: ")).lower() or ''
    stats.start = str(input("Start Time (MM/DD/YYYY) \t: ")) or ''
    stats.end = str(input("Start Time (MM/DD/YYYY) \t: ")) or ''
    output.mode = str(input("Output Type (default : text) \t: ")).lower() or 'text'
    output.filename = str(input("Filename [default : $username] \t: ")).lower() or \
        stats.values['user']


def assign_values(args):
    stats.values['user'] = str(args.user).lower()
    stats.category = args.category.lower()
    stats.start = args.start
    stats.end = args.end
    stats.weeks = int(args.weeks)
    stats.group = args.group
    stats.log = args.log
    output.mode = args.mode.lower()
    output.filename = stats.filename =  args.output.lower()


def add_arguments(parser):
    parser.add_argument('--category', '-c', help="Sub Category", default='')
    parser.add_argument('--end', '-e', help="End Date", default='')
    parser.add_argument('--group', '-g', help="FAS Group", default='')
    parser.add_argument('--interactive', '-i', help="Enable interactive mode",
                            action='store_true')
    parser.add_argument('--log', '-l', help="Enable full log reporting",
                            action='store_true')
    parser.add_argument('--mode', '-m', help="Type of Output", default='text')
    parser.add_argument('--output', '-o', help="Output name", default='stats')
    parser.add_argument('--start', '-s', help="Start Date", default='')
    parser.add_argument('--user', '-u', help='FAS username')


def generator(args, mode, user):
    if mode=='group':
        args.user = user
        stats.values['user'] = user

    # Else, use the argparse values. No arguments is handled by argparse.
    assign_values(args)

    stats.return_users()
    # For png and SVG, we need a drawable object to be called


def main():
    # fedmsg config
    config = fedmsg.config.load_config()
    fedmsg.meta.make_processors(**config)

    # Initializing to None to prevent errors while generating multiple reports
    stats.unicode_json = {}
    i_count = 0
    group_userlist = list()

    # Argument Parser initialization
    parser = argparse.ArgumentParser(description='Fedora Statistics Gatherer')
    add_arguments(parser)
    args = parser.parse_args()

    if args.group:
        print("Gathering group statistics ..")
        group = GroupParser()
        group_userlist = list(group.group_users(args.group))

    # Check if the argument type is interactive
    if args.interactive:
        interactive_input(args)

    elif args.group:
        for user in group_userlist:
            generator(args, 'group', user)
    # Check if the user argument exists
    elif args.user is None :
        if not args.group:
            print(colored("[!] ", 'red') + "Username is required. Use -h for help")
            return 1
    else:
        generator(args, 'user', args.user.lower())




if __name__ == '__main__':
    main()
