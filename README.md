# 💥 Expand FASTA

A simple python tool to expand a FASTA file that was previously collapsed, if given a name mapping in JSON format.

## Installation
### With PipX
You can get this to run using [`pipx`](https://github.com/pypa/pipx). To install `pipx` you can run:

```shell
brew install pipx
pipx ensurepath
sudo pipx ensurepath --global # optional to allow pipx actions with --global argument
```

or 

```shell
sudo apt update
sudo apt install pipx
pipx ensurepath
sudo pipx ensurepath --global # optional to allow pipx actions with --global argument
```


Then, simply run:

```shell
pipx install git+https://github.com/HIVDiversity/expand-fasta.git
```

Now the command `expand-fasta` has been installed. 

### From Source
You can also clone this repo and then run the `main.py` file. You'll need to install the dependencies `typer` and `rich`. 

## Usage

You can see the help page by running

```shell
expand-fasta --help
```

Which will return:

```text
Usage: expand-fasta [OPTIONS] COLLAPSED_FASTA NEW_TO_OLD_NAMES OUTPUT_FASTA                                   
                                                                                                               
╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    collapsed_fasta       PATH  The path to the uncollapsed input file. [default: None] [required]         │
│ *    new_to_old_names      PATH  The path to the mapping file in json format [default: None] [required]     │
│ *    output_fasta          PATH  The path to write the files to. [default: None] [required]                 │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --use-fasta-names          If set, will fetch the sequences in the FASTA file using the names in the name   │
│                            file.                                                                            │
│ --help                     Show this message and exit.                                                      │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

#### `--use-fasta-names`

This option defines how the program goes about fetching names provided. It can either use the names in the namefile as the reference, or it can use the names in the fasta file as the reference. 

If you expect all of the sequences in NAMEFILE to be represented in the FASTA file, then you can ignore this option. 

If not specified, the behaviour of the program is as follows:

1. Retrieve a "new name" from the name file
2. Look for this name in the FASTA file.
3. Uncollapse it

If this option is specified, however, the behaviour is as follows:

1. Retrieve a "new name" from the **fasta file**
2. Look for this name in the **name file**. 
3. Uncollapse the sequence




