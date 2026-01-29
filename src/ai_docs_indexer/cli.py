"""CLI interface for ai-docs-indexer."""

from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel

from . import __version__
from .formatters import IndexData, get_formatter
from .scanner import scan_directory

console = Console()


def parse_extensions(ctx, param, value: str | None) -> tuple[str, ...]:
    """Parse comma-separated extensions into a tuple."""
    if value is None:
        return (".md", ".mdx")

    extensions = []
    for ext in value.split(","):
        ext = ext.strip()
        if not ext.startswith("."):
            ext = f".{ext}"
        extensions.append(ext)

    return tuple(extensions)


@click.group()
@click.version_option(version=__version__, prog_name="ai-docs-indexer")
def main():
    """Generate compressed documentation indexes for AI agent context files."""
    pass


@main.command()
@click.argument("path", type=click.Path(exists=True, file_okay=False, resolve_path=True))
@click.option(
    "-o", "--output",
    type=click.Path(dir_okay=False),
    help="Output file path. If not specified, prints to stdout.",
)
@click.option(
    "-f", "--format",
    "formats",
    type=click.Choice(["pipe", "json", "yaml"]),
    multiple=True,
    default=["pipe"],
    help="Output format(s). Can be specified multiple times.",
)
@click.option(
    "-n", "--name",
    default="Documentation Index",
    help="Name for the index.",
)
@click.option(
    "-r", "--root",
    help="Root path to use in output (default: scanned path).",
)
@click.option(
    "-e", "--extensions",
    callback=parse_extensions,
    help="Comma-separated file extensions to include (default: .md,.mdx).",
)
@click.option(
    "-i", "--instruction",
    help="Instruction text for AI agents.",
)
@click.option(
    "--include-hidden/--no-hidden",
    default=False,
    help="Include hidden files and directories.",
)
@click.option(
    "--follow-symlinks/--no-follow-symlinks",
    default=False,
    help="Follow symbolic links.",
)
@click.option(
    "--stdout",
    is_flag=True,
    help="Force output to stdout even if --output is specified.",
)
@click.option(
    "-q", "--quiet",
    is_flag=True,
    help="Suppress status messages.",
)
def scan(
    path: str,
    output: str | None,
    formats: tuple[str, ...],
    name: str,
    root: str | None,
    extensions: tuple[str, ...],
    instruction: str | None,
    include_hidden: bool,
    follow_symlinks: bool,
    stdout: bool,
    quiet: bool,
):
    """
    Scan a documentation directory and generate an index.

    PATH is the directory to scan for documentation files.
    """
    scan_path = Path(path)
    root_path = root if root else f"./{scan_path.name}"

    if not quiet:
        console.print(f"[blue]Scanning[/] {scan_path}")

    try:
        result = scan_directory(
            scan_path,
            extensions=extensions,
            include_hidden=include_hidden,
            follow_symlinks=follow_symlinks,
        )
    except ValueError as e:
        console.print(f"[red]Error:[/] {e}")
        raise SystemExit(1)

    if not quiet:
        console.print(
            f"[green]Found[/] {result.total_files} files "
            f"in {len(result.directories)} directories"
        )

    # Build index data
    index_data = IndexData(
        name=name,
        root=root_path,
        directories=result.directories,
        instruction=instruction,
    )

    # Generate output for each format
    for format_name in formats:
        formatter = get_formatter(format_name)
        formatted = formatter.format(index_data)

        if stdout or output is None:
            if len(formats) > 1:
                console.print(Panel(formatted, title=f"[bold]{format_name}[/]"))
            else:
                click.echo(formatted)
        else:
            # Determine output path
            if len(formats) > 1:
                # Multiple formats: add format suffix
                out_path = Path(output)
                final_path = out_path.with_suffix(f".{format_name}{out_path.suffix}")
            else:
                final_path = Path(output)

            final_path.write_text(formatted)
            if not quiet:
                console.print(f"[green]Wrote[/] {final_path}")


@main.command()
def formats():
    """List available output formats."""
    from .formatters import JsonFormatter, PipeFormatter, YamlFormatter

    formatters = [PipeFormatter(), JsonFormatter(), YamlFormatter()]

    console.print("[bold]Available formats:[/]\n")
    for f in formatters:
        console.print(f"  [cyan]{f.name}[/] - {f.file_extension} files")


if __name__ == "__main__":
    main()
