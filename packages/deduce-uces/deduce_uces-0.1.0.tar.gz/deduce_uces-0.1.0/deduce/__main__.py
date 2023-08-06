import argparse
import multiprocessing

from deduce.Logger import LOG_LEVEL_TAGS, Logger
from deduce.commands.align import command_align
from deduce.commands.extend import command_extend
from deduce.commands.find import command_find
from deduce.commands.minimise import command_minimise
from deduce.output.output import OUTPUT_FORMATS


def range_similarity(arg):
    try:
        min_similarity = float(arg)
    except ValueError:

        raise argparse.ArgumentTypeError("Minimum similarity must be a float")
    if min_similarity < 50 or min_similarity > 100:
        raise argparse.ArgumentTypeError(
            "minimum similarity must be between 50.0 and 100.0"
        )
    return min_similarity


def range_genome_num(arg):
    try:
        genome = int(arg)
    except ValueError:

        raise argparse.ArgumentTypeError("Minimum Genome number must be an integer")
    if genome < 2:
        raise argparse.ArgumentTypeError(
            "Minimum genomes must be between 2 and the number of genomes provided"
        )
    return genome


def range_length(arg):
    try:
        min_length = int(arg)
    except ValueError:
        raise argparse.ArgumentTypeError("Minimum UCE length must be an integer")
    return min_length


def parse_args():
    parser = argparse.ArgumentParser(
        description="Find ultraconserved elements across multiple genomes"
    )

    # Global arguments
    parser.add_argument(
        "--log_level",
        choices=list(LOG_LEVEL_TAGS.values()),
        default="INFO",
        help="the minimum severity level of logs that will be sent to stderr",
    )

    parser.add_argument(
        "--threads",
        type=int,
        default=multiprocessing.cpu_count(),
        help="The number of CPU threads to use",
    )

    subparsers = parser.add_subparsers(help="Commands")

    ###########################
    ##         find          ##
    ###########################
    parser_find = subparsers.add_parser(
        "find", help="Find all UCEs in the set of input genomes"
    )

    parser_find.set_defaults(func=command_find)

    parser_find.add_argument(
        "genomes", metavar="GEN", type=str, nargs="+",
    )

    parser_find.add_argument(
        "--min_length",
        type=range_length,
        default=100,
        help="the minimum number of base pairs required to constitute a UCE. 100bp by default",
    )

    parser_find.add_argument(
        "--min_genomes",
        type=int,
        default=None,
        help="the minimum number of genomes the sequence must be found in. All genomes provided by default",
    )

    parser_find.add_argument(
        "--canonical", action="store_true", help="canonical kmers (both strands)",
    )

    parser_find.add_argument(
        "--dump_hashes",
        type=str,
        default=None,
        help="if provided, Jellyfish hashes will be output to the given directory rather than deleted after the program completes",
    )

    parser_find.add_argument(
        "--output", type=str, default="deduce_uces.fa", help="The output filename"
    )

    ###########################
    ##        align          ##
    ###########################
    parser_align = subparsers.add_parser(
        "align", help="Align a set of UCEs with a reference genome"
    )

    parser_align.set_defaults(func=command_align)

    parser_align.add_argument(
        "uces",
        metavar="UCES",
        type=str,
        help="A FASTA file containing one or more UCEs",
    )

    parser_align.add_argument(
        "genomes",
        metavar="GENOME",
        type=str,
        nargs="+",
        help="FASTA files containing reference genome",
    )

    parser_align.add_argument(
        "--output_format",
        choices=list(OUTPUT_FORMATS.keys()),
        default="gff",
        help="The output format for the alignment",
    )

    ###########################
    ##        minimise       ##
    ###########################
    parser_minimise = subparsers.add_parser("minimise", help="Minimise set of UCEs")

    parser_minimise.set_defaults(func=command_minimise)

    parser_minimise.add_argument(
        "uces",
        metavar="UCES",
        type=str,
        help="A FASTA file containing one or more UCEs",
    )

    parser_minimise.add_argument(
        "alignments",
        metavar="ALIGNMENT",
        type=str,
        nargs="+",
        help="GFF files containing aligned UCEs",
    )

    parser_minimise.add_argument(
        "--output_format",
        choices=list(OUTPUT_FORMATS.keys()),
        default="gff",
        help="The output format for the minimised alignments",
    )

    ###########################
    ##        extend         ##
    ###########################
    parser_extend = subparsers.add_parser(
        "extend", help="Extend a set of UCEs with non-exact matches"
    )

    parser_extend.set_defaults(func=command_extend)

    parser_extend.add_argument(
        "uces",
        metavar="UCES",
        type=str,
        help="A FASTA file containing one or more UCEs",
    )

    parser_extend.add_argument(
        "--alignments",
        metavar="ALIGNMENT",
        type=str,
        nargs="+",
        help="GFF files containing aligned UCEs",
    )

    parser_extend.add_argument(
        "--genomes",
        metavar="GENOME",
        type=str,
        nargs="+",
        help="FASTA files containing a genome",
    )

    parser_extend.add_argument(
        "--min_similarity",
        type=range_similarity,
        default=100,
        nargs=1,
        help="the minimum percentage similarity required to constitute a UCE. 100 by default",
    )

    parser_extend.add_argument(
        "--min_length",
        type=range_length,
        default=100,
        help="the minimum number of base pairs required to constitute a UCE. 100bp by default",
    )

    parser_extend.add_argument(
        "--output_format",
        choices=list(OUTPUT_FORMATS.keys()),
        default="gff",
        help="The output format for the minimised alignments",
    )

    return parser.parse_args()


def main():
    args = parse_args()
    logger = Logger({v: k for k, v in LOG_LEVEL_TAGS.items()}[args.log_level])

    args.func(args, logger)


if __name__ == "__main__":
    main()
