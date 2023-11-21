"""
Description:
    This script downloads GenBank files given an input file of a list of NCBI
    accession numbers. Files are download asynchronously for speed. 

    Use at your own discretion, particularly when downloading many files at
    once as there are limits to the number of HTTP requests that can be made.

Usage:
    python3 download_genbank.py

Requirements:
    click, cogent3, unsync

Authors: Gavin Huttley, Fred Jaya, Robert McArthur
"""

import os
import pathlib
import random
import threading
import time
import urllib.request
from urllib.error import HTTPError

import click
from cogent3.util.io import atomic_write
from unsync import unsync

url_template = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=%s&rettype=gb&retmode=text"


def load_accessions(path: os.PathLike) -> list[str]:
    return [l.strip() for l in path.read_text().splitlines()]

@unsync
def download_one(outdir, accession, bar, lock):
    outpath = outdir / f"{accession}.gb.gz"
    if outpath.exists():
        with lock:
            bar.update(1)
        return

    url = url_template % accession

    done = False
    while not done:
        # To overcome HTTP request limit (~3s/request)
        try:
            f = urllib.request.urlopen(url)
            data = f.read()
            done = True
        except HTTPError as e:
            if e.code == 429:
                # stagger requests
                time.sleep(3 + random.random())
            else:
                raise e

    with atomic_write(outpath, mode="wb") as out:
        out.write(data)
        with lock:
            bar.update(1)


def download(outdir, accessions):
    lock = threading.Lock()
    with click.progressbar(length=len(accessions), label="Downloading GenBank Files") as bar:
        tasks = [download_one(accession=accession, outdir=outdir, bar=bar, lock=lock) for accession in accessions]
        results = [task.result() for task in tasks]


@click.command(no_args_is_help=True)
@click.option(
    "-p",
    "--path",
    type=pathlib.Path,
    required=True,
    help="path to genbank accession file",
)
@click.option(
    "-o",
    "--outdir",
    type=pathlib.Path,
    required=True,
    help="path to write genbank formatted sequence files",
)
@click.option(
    "-l",
    "--limit",
    default=10,
    show_default=True,
    help="number of accessions to download",
)
def main(path, outdir, limit):
    """downloads limit accessions from GenBank"""
    path = pathlib.Path(path)

    accessions = load_accessions(path=path)
    accessions = accessions[:limit]
    outdir.mkdir(exist_ok=True)
    start = time.time()

    download(outdir=outdir, accessions=accessions)
    print(f"Downloaded in {time.time()-start:.2f} seconds.")


if __name__ == "__main__":
    main()
