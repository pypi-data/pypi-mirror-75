# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 21:39:34 2020

@author: Gideon Pomeranz

main.py

This is the main script that get called on the command line

"""
### Packages ###
import sys
import argparse
#from __init__ import __version__
from .align import align

#----------------------------------------------------------------------------#
# These are the functions that actually do the computational steps
def parse_align(args):
    """Parser for the `align` command.
    :param args: Command-line arguments dictionary, as parsed by argparse
    :type args: dict
    """
    align(
        args.f,
        args.o,
        args.x,
        threads=args.t,
        memory=args.m,
        )
#----------------------------------------------------------------------------#
# Here are all the commands that are give to scGP so you can run scGP COMMAND
COMMAND_TO_FUNCTION = {
    'align': parse_align,
}

#----------------------------------------------------------------------------#
### Parser helpers ###
def setup_align_args(parser, parent):
    """Helper function to set up a subparser for the `align` command.
    :param parser: argparse parser to add the `align` command to
    :type args: argparse.ArgumentParser
    :param parent: argparse parser parent of the newly added subcommand.
                   used to inherit shared commands/flags
    :type args: argparse.ArgumentParser
    :return: the newly added parser
    :rtype: argparse.ArgumentParser
    """

    parser_ref = parser.add_parser(
        'align',
        description='Build a kallisto index and transcript-to-gene mapping and aligns',
        help='Build a kallisto index and transcript-to-gene mapping and aligns',
        parents=[parent],
    )
    parser_ref._actions[0].help = parser_ref._actions[0].help.capitalize()

    required_ref = parser_ref.add_argument_group('required arguments')
    required_ref.add_argument(
        '-f',
        metavar='INDEX',
        help='Path to the file holding the sample and fasta information',
        type=str,
        required=True
    )
    required_ref.add_argument(
        '-o',
        metavar='ORGANISM',
        help='Name of the organism used. Example: human,mouse,....',
        type=str,
        required=True
    )
    required_ref.add_argument(
        '-x',
        metavar='TECHNOLOGY',
        help=(
            'Technology used to generate scRNA-seq'
        ),
        type=str,
        required=True
    )
    parser_ref.add_argument(
        '-t',
        metavar='THREADS',
        help='Number of threads to use (default: 8)',
        type=str,
        default=8
    )
    parser_ref.add_argument(
        '-m',
        metavar='MEMORY',
        help='Maximum memory used (default: 4G)',
        type=str,
        default='4G'
    )
    
    return parser_ref

#----------------------------------------------------------------------------#
def main():
    """Command-line entrypoint.
    """
    # Main parser
    parser = argparse.ArgumentParser(
        description='scGP'
    )
    parser._actions[0].help = parser._actions[0].help.capitalize()

    subparsers = parser.add_subparsers(
        dest='command',
        metavar='<CMD>',
    )

    # Add common options to this parent parser
    parent = argparse.ArgumentParser(add_help=False)
    

    # Command parsers
    parser_align = setup_align_args(subparsers, parent)
    

    command_to_parser = {
        'align': parser_align,
    }
    
    if len(sys.argv) == 2:
        if sys.argv[1] in command_to_parser:
            command_to_parser[sys.argv[1]].print_help(sys.stderr)
        else:
            parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    COMMAND_TO_FUNCTION[args.command](args)
    #try:
        #COMMAND_TO_FUNCTION[args.command](args)
    #except Exception:
        #print("Something happened")
