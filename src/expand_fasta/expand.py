from pathlib import Path
from warnings import warn
import json
import logging
from rich import print
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")


def fasta_to_dict(filepath: Path) -> dict[str, str]:
    """Reads a FASTA-formatted file into a python dictionary

    Args:
        filepath (Path): The path to the fasta file

    Returns:
        dict[str, str]: A dictionary where the sequence IDs are the keys, and the sequences are the values
    """

    fasta_string_lines = open(filepath, "r").readlines()

    sequences = {}
    header = ""
    for line in fasta_string_lines:
        line = line.strip()
        if line.startswith(">"):
            header = line.strip().strip(">")
            if header in sequences:
                logging.warning(
                    f"There is already a line with the header {header} and it will be overwritten"
                )
            sequences[header] = ""
        else:
            sequences[header] += line.strip()

    return sequences


def dict_to_fasta(
    fasta_dict: dict[str, str], output_file: Path, sort: bool = False
) -> None:
    """Writes a FASTA dictionary object to a file, optionally sorting it

    Args:
        fasta_dict (dict[str, str]): The dictionary containing the sequences and their keys
        output_file (Path): Where to write the resulting file
        sort (bool, optional): Sort the output fasta file by sequence name. Defaults to False.
    """

    if sort:
        log.info("Sorting the FASTA dictionary")
        fasta_dict = dict(sorted(fasta_dict.items(), key=lambda item: item[0]))

    with open(output_file, "w") as fh:
        log.info(f"Writing the contents of the dictionary to {output_file}")
        for header in fasta_dict:
            fh.write(">" + header + "\n")
            fh.write(fasta_dict[header] + "\n")

        log.info("Done writing.")


def expand_fasta_dictionary(
    sequences: dict[str, str],
    names: dict[str, list[str]],
    use_namefile_as_reference: True,
) -> dict[str, str]:
    """Expands collapsed sequences in a fasta-formatted dictionary based on a name dictionary.

    Args:
        sequences (dict[str, str]): The collapsed sequences.
        names (dict[str, list[str]]): The mapping of collapsed sequences to uncollapsed names
        use_namefile_as_reference (bool, optional): Uses the sequence names in the namefile to get the sequences from the collapsed file. If you're using a subset of the sequences that are present in the namefile, set this to false. Defaults to True.

    Returns:
        dict[str, str]: A new dictionary containing a sequence for each name in the uncollapsed lists
    """

    new_fasta_file: dict[str, str] = {}
    name_iterable = list(names.keys())

    missing_names_from_fasta = []
    missing_names_from_namefile = []

    if not use_namefile_as_reference:
        name_iterable = list(sequences.keys())

    for name in name_iterable:
        collapsed_seq = sequences.get(name)

        if collapsed_seq is None:
            missing_names_from_fasta.append(name)
            continue

        old_names = names.get(name)

        if old_names is None:
            missing_names_from_namefile.append(name)
            continue

        for old_name in old_names:
            new_fasta_file[old_name] = collapsed_seq

    if len(missing_names_from_fasta) > 0:
        log.warning(
            f"Failed to find {len(missing_names_from_fasta)} names in the FASTA file that *were* present in the namefile:"
        )
        log.warning(missing_names_from_fasta)

    if len(missing_names_from_namefile) > 0:
        log.warning(
            f"Failed to find {len(missing_names_from_namefile)} names in the NAMEFILE that *were* present in the FASTA file:"
        )
        log.warning(missing_names_from_namefile)

    return new_fasta_file


def expand_without_namefile(sequences: dict[str, str], num_seq_element_idx: int = 5) -> dict[str, str]:
    uncollapsed_seqs: dict[str, str] = {}

    for name, seq in sequences.items():
        split_name = name.split("_")

        if num_seq_element_idx >= len(split_name):
            log.error(f"The sequence with name '{name}' is likely in the incorrect format, since after splitting with '_' it doesn't have the right length")
            exit(1)

        num_seqs_portion = split_name[4]
        
        if not num_seqs_portion.isnumeric():
            log.error(f"The number portion is not numeric for sequence {name}. We attempted to convert '{num_seqs_portion}' to an int.")
            exit(1)
            
        number_of_seqs = int(num_seqs_portion)
        
        for seq_num in range(number_of_seqs):
            
            # TODO: This could throw unexpected IndexOutOfBoundsError
            new_name = "_".join(split_name[:5])
            new_name += f"_{str(seq_num).rjust(4, '0')}"
            uncollapsed_seqs[new_name] = seq
            
    return uncollapsed_seqs
        


def read_name_mapping(namefile: Path) -> dict[str, list[str]]:
    """Read the old-to-new name mapping in from a json file.

    Args:
        namefile (Path): The path to the json file holding the name mapping. It is assumed that this JSON is valid and correctly formatted.

    Returns:
        dict[str, list[str]]: The name mapping as a dictionary where each key is a new name (collapsed) and each value is a list of the 1-* old names that were collapsed
    """

    # TODO: add schema validation

    name_mapping: dict[str, list[str]] = json.load(open(namefile, "r"))

    return name_mapping


def workflow(
    collapsed_fasta: Path,
    new_to_old_names: Path,
    output_fasta: Path,
    use_namefile_ref: bool = True,
):
    log.info("Reading the collapsed sequences")
    collapsed_seqs = fasta_to_dict(collapsed_fasta)
    log.info("Done.")

    log.info("Reading the name mappings")
    name_mapping = read_name_mapping(new_to_old_names)
    log.info("Done.")

    log.info("Uncollapsing.")
    uncollapsed_sequences = expand_fasta_dictionary(
        collapsed_seqs, name_mapping, use_namefile_ref
    )
    log.info("Done.")

    log.info("Writing to file.")
    dict_to_fasta(uncollapsed_sequences, output_fasta, False)
    log.info("Done. Exiting.")


def workflow_expand_without_namefile(collapsed_fasta: Path,
    output_fasta: Path,
    num_seq_element: int = 5):
    
    log.info("Reading the collapsed sequences")
    collapsed_seqs = fasta_to_dict(collapsed_fasta)
    log.info("Done.")

    log.info("Uncollapsing *without* namefile.")
    uncollapsed_sequences = expand_without_namefile(
        collapsed_seqs, num_seq_element
    )
    log.info("Done.")

    log.info("Writing to file.")
    dict_to_fasta(uncollapsed_sequences, output_fasta, False)
    log.info("Done. Exiting.")

    