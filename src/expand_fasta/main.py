import typer
import rich
from typing_extensions import Annotated
from pathlib import Path
from expand_fasta import expand

app = typer.Typer(add_completion=False, no_args_is_help=True)

@app.command("expand")
def cli_expand_fasta_file(
    collapsed_fasta: Annotated[
        Path, typer.Argument(help="The path to the uncollapsed input file.")
    ],
    new_to_old_names: Annotated[
        Path, typer.Argument(help="The path to the mapping file in json format")
    ],
    output_fasta: Annotated[
        Path, typer.Argument(help="The path to write the files to.")
    ],
    use_fasta_as_ref: Annotated[
        bool,
        typer.Option(
            "--use-fasta-names",
            help="If set, will fetch the sequences in the FASTA file using the names in the name file."
        ),
    ] = False,
):

    expand.workflow(
        collapsed_fasta=collapsed_fasta,
        new_to_old_names=new_to_old_names,
        output_fasta=output_fasta,
        use_namefile_ref= not use_fasta_as_ref,
    )

@app.command("expand-without-names")
def cli_expand_without_names(collapsed_fasta: Annotated[
        Path, typer.Argument(help="The path to the uncollapsed input file.")
    ],
    output_fasta: Annotated[
        Path, typer.Argument(help="The path to write the files to.")
    ]):
    
    expand.workflow_expand_without_namefile(
        collapsed_fasta=collapsed_fasta,
        output_fasta=output_fasta,
        # TODO: Remove hardcoded number here
        num_seq_element=5
    )

def run():
    app()

if __name__ == "__main__":
    run()
