import asyncio
from typing import List

import typer

from app.scripts.ingest import ingest_files

app = typer.Typer(help="RAG ingestion CLI (ingest, reindex).")


@app.command()
def ingest(
    paths: List[str] = typer.Argument(..., help="Files or glob patterns."),
    collection: str = typer.Option("docs", "--collection", "-c"),
    chunk_size: int = typer.Option(200, help="Words per chunk."),
    chunk_overlap: int = typer.Option(40, help="Overlap in words."),
    mode: str = typer.Option("fixed", "--mode", "-m", help="'fixed' or 'semantic'"),
    reset: bool = typer.Option(
        False, "--reset", help="Delete existing collection before ingesting."
    ),
):
    total = asyncio.run(
        ingest_files(
            file_patterns=paths,
            collection_name=collection,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            reset=reset,
            mode=mode,
        )
    )
    typer.echo(f"Ingested total {total} chunks.")


@app.command("reindex")
def reindex(
    paths: List[str] = typer.Argument(..., help="Files or glob patterns."),
    collection: str = typer.Option("docs", "--collection", "-c"),
    chunk_size: int = typer.Option(200, help="Words per chunk."),
    chunk_overlap: int = typer.Option(40, help="Overlap in words."),
    mode: str = typer.Option("fixed", "--mode", "-m", help="'fixed' or 'semantic'"),
):
    total = asyncio.run(
        ingest_files(
            file_patterns=paths,
            collection_name=collection,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            reset=True,  # always reset for reindex
            mode=mode,
        )
    )
    typer.echo(f"Reindexed collection '{collection}' with {total} chunks.")


if __name__ == "__main__":
    app()
