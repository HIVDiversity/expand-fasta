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
Usage: expand-fasta [OPTIONS] COMMAND [ARGS]...                                                
                                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────╮
│ expand                                                                                       │
│ expand-without-names   Given an collapsed FASTA file, returns a new FASTA file with the      │
│                        correct number of uncollapsed sequences, without needing a namefile.  │
╰──────────────────────────────────────────────────────────────────────────────────────────────╯
```
### Commands
The `expand` command is used when you want to map the collapsed names in the fasta file to their previously uncollapsed names. It requires you to have a namefile. 

The `expand-without-names` does what is said on the box. It will just used the sequence names to determine how many copies of the collapsed sequence to make. 

For example: `CAP040_2010_ENV_NT_0017_0001` will be left as is (since there's only one sequence) but `CAP040_2010_ENV_NT_0022_0003` will be expanded to be three sequences:

- `CAP040_2010_ENV_NT_0022_0001`
- `CAP040_2010_ENV_NT_0022_0002`
- `CAP040_2010_ENV_NT_0022_0003`

Importantly, this does mean that the last item of the new name takes on a different meaning. It is a simple counter rather than representing the number of collapsed sequences, like it did for the names in the collapsed file.

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




