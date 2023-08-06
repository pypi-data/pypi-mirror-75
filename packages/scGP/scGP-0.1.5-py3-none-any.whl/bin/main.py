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
from .preprocess import preprocess

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

def parse_process(args):
    preprocess(
        args.f,
        args.o,
        args.min_c,
        args.min_g,
        args.mito,
        args.max_g,
        args.top_g
        )
#----------------------------------------------------------------------------#
# Here are all the commands that are give to scGP so you can run scGP COMMAND
COMMAND_TO_FUNCTION = {
    'align': parse_align,
    'process': parse_process
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
        metavar='INPUT',
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
        default="8"
    )
    parser_ref.add_argument(
        '-m',
        metavar='MEMORY',
        help='Maximum memory used (default: 4G)',
        type=str,
        default='4G'
    )
    
    return parser_ref

def setup_process_args(parser, parent):
    """Helper function to set up a subparser for the `process` command.
    :param parser: argparse parser to add the `align` command to
    :type args: argparse.ArgumentParser
    :param parent: argparse parser parent of the newly added subcommand.
                   used to inherit shared commands/flags
    :type args: argparse.ArgumentParser
    :return: the newly added parser
    :rtype: argparse.ArgumentParser
    """

    parser_process = parser.add_parser(
        'process',
        description='Processes/filters and produces QC plots for aligned data',
        help='Processes/filters and produces QC plots for aligned data',
        parents=[parent],
    )
    parser_process._actions[0].help = parser_process._actions[0].help.capitalize()

    required_process = parser_process.add_argument_group('required arguments')
    required_process.add_argument(
        '-f',
        metavar='INPUT',
        help='Path to the file holding the sample and fasta information',
        type=str,
        required=True
    )
    required_process.add_argument(
        '-o',
        metavar='ORGANISM',
        help='Name of the organism used. Example: human,mouse,....',
        type=str,
        required=True
    )
    parser_process.add_argument(
        '-min_c',
        metavar='CELL_THRESHOLD',
        help=(
            'Minimum amount of cells a gene must be expressed in (Default: 3)'
        ),
        type=str,
        default="3"
    )
    parser_process.add_argument(
        '-min_g',
        metavar='GENE_THRESHOLD',
        help='Minimum amount of genes a cell must express (Default: 300)',
        type=str,
        default="300"
    )
    parser_process.add_argument(
        '-mito',
        metavar='MITOCHONDRIAL CONTENT',
        help='Maximum percentage of mitochondrial genes a cell can have (Default: 5)',
        type=str,
        default="5"
    )
    parser_process.add_argument(
        '-max_g',
        metavar='GENE_MAX_THRESHOLD',
        help='Maximum amount of genes a cell can express (Default: 30000)',
        type=str,
        default="30000"
    )
    parser_process.add_argument(
        '-top_G',
        metavar='NO_VARIABLE_GENES',
        help='Number of genes to use for subsequent analysis (Default: 1000)',
        type=str,
        default="1000"
    )
    
    return parser_process
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
    parser_process = setup_process_args(subparsers, parent)

    command_to_parser = {
        'align': parser_align,
        'process': parser_process
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
        #print("An exception occured")
