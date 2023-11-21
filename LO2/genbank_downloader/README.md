# Downloading GenBank files from a list of accession numbers 

`download_genbank.py` takes a file with a list of NCBI accession numbers and downloads the associated GenBank file. Files are downloaded asynchronously for speed.

## Requirements

All requirements have been preinstalled within the docker image. The subset required to run `download_genbank.py` are:

- click 
- cogent3 
- unsync

## Example usage

- For help and options
```bash
$ python download_genbank.py
Usage: download_genbank.py [OPTIONS]

  downloads limit accessions from GenBank

Options:
  -p, --path PATH      path to genbank accession file  [required]
  -o, --outdir PATH    path to write genbank formatted sequence files
                       [required]
  -l, --limit INTEGER  number of accessions to download  [default: 10]
  --help               Show this message and exit.

```

- To download GenBank (.gb.gz) files for the first 10 accessions (default limit)
```bash
$ python download_genbank.py -p refsoil_id.txt -o refsoil
```

- To download GenBank (.gb.gz) files for the first 20 accessions
```bash
$ python download_genbank.py -p refsoil_id.txt -o refsoil -l 20
```