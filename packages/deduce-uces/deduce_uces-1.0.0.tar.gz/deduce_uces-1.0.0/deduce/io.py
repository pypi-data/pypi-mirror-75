import re
import os
from typing import List

from gffutils import DataIterator

from deduce.types import MinimalUCE

FASTA_HEADER_RE = ">.*"  # Matches FASTA headers
FASTA_SEQ_RE = f"[ACGTURYKMSWBDHVN-]+"  # Matches FASTA nucleotide sequences

STATE_EXPECT_HEADER = 0
STATE_EXPECT_SEQUENCE = 1
STATE_EXPECT_EITHER = 2


def validate_fasta(filename):
    """Validate that a given file exists and is a correctly-formed FASTA file."""

    if not os.path.exists(filename):
        return f"File does not exist: {filename}"

    # Compile the regexes to speed up validation of large files
    header_re = re.compile(FASTA_HEADER_RE)
    seq_re = re.compile(FASTA_SEQ_RE)

    # Small state machine to verify that lines are valid and in the correct order
    state = STATE_EXPECT_HEADER

    line_count = 0
    with open(filename) as f:
        for line in f:
            # Skip blank lines
            if line.strip() == "":
                line_count += 1
                continue

            if state == STATE_EXPECT_EITHER:
                if re.fullmatch(header_re, line.strip()):
                    state = STATE_EXPECT_SEQUENCE
                elif re.fullmatch(seq_re, line.strip()):
                    pass
                else:
                    return f"Invalid input on line {line_count}: {line.strip()}"

            elif state == STATE_EXPECT_HEADER:
                if re.fullmatch(header_re, line.strip()):
                    state = STATE_EXPECT_SEQUENCE
                else:
                    return f"Expected valid header on line {line_count}"

            elif state == STATE_EXPECT_SEQUENCE:
                if re.fullmatch(seq_re, line.strip()):
                    state = STATE_EXPECT_EITHER
                else:
                    return f"Expected valid sequence on line {line_count}"

            else:
                raise ValueError(f"Invalid state in validate_fasta: {state}")

            line_count += 1

    if line_count == 0:
        return f"File is empty"

    return None


def read_gff3(filename) -> List[MinimalUCE]:
    uces = []
    for feature in DataIterator(filename):
        if feature.featuretype == "conserved_region":
            uces.append(
                MinimalUCE(feature.attributes["ID"][0], feature.start - 1, feature.end)
            )

    return uces
