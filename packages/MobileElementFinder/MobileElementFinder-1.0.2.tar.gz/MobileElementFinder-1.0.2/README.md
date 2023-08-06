![logo](images/logo.png)

`MobileElementFinder` is a tool for identifying Mobile Genetic Elements (MGEs) in Whole Genome Shotgun sequence data.

It is designed to predict mobile elements in assembled whole genome sequenced
bacterial DNA. MGEs are predicted by aligning the assembled contigious
sequences to reference seqeunces of previously known elements. Putative
composite transposons are flagged. This command line version of MobileElementFinder
is designed to run either on your local machine or inside a docker container.

**NOTE: MobileElementFinder is also availabe as an online software service on
[https://cge.cbs.dtu.dk/services/MobileElementFinder/](https://cge.cbs.dtu.dk/services/MobileElementFinder/)**
## Installation

Clone repository.

Ensure that the following software dependencies are installed. If dependencies are not
put into your `$PATH` you have to supply their location to MobileElementFinder.

- [Ncbi blast v2.10.0 or newer](ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST)
- [KMA v1.2.3 or newer (Optional)](https://bitbucket.org/genomicepidemiology/kma/src/master/)

Depending on your operating system the dependancies might be available on it's
package manager system.

For [Homebrew](https://brew.sh/) on macOS.

```bash
$ brew install blast
```

To install MobileElementFinder with the database simply install it from pypi.

```bash
$ pip install MobileElementFinder
```

## Using MobileElementFinder

Use the command `$ mefinder find --help` to see the full list of options.

MobileElementFinder takes assembled contiguous nucleotide sequences as input. Specify the
sequence file with the `--contig` flag. The path to and name of the output files
are specified as an argument.

```bash
$ mefinder find --contig /path/to/genome.fna output_name
```

MobileElementFinder reports predicted mobile elements in two files. Predicted MGEs and
their quality metrics are written to a CSV file and their nucleotide sequence is
written to a FASTA file. The first five rows in the CSV file contains comments,
beginning with # and containing key-value paired metadata on how the file was
generated. The user might be required to manually specify that these rows should
be omitted depending on the downstream spreadsheet application or parser.

MobileElementFinder can additionally output the location of MGEs on the different contigs
in [GFF3
format](https://github.com/The-Sequence-Ontology/Specifications/blob/master/gff3.md)
by using the `--gff` flag. This to allow visualization with genomic browser
software. The user can optionally choose to annotate the sequence depth of the
predicted elements by aligning the raw reads, used to assemble the sample, with
KMA. To enable this specifies the sequence files in fastq format with the `fastq`
flag.

### Options and configuration of MobileElementFinder

The operation of MobileElementFinder can be modulated by either giving the program
optional flags or by supplying the program with a personal configuration file.

```bash
Usage: mobileElementFinder.py find [OPTIONS] OUTPUT

  Find mobile element in sequence data.

Options:
  -c, --contig PATH        Specify pre-assembled contigs to perform analysis
                           on.

  -f, --fq-file PATH       Sequencing files in fastq format. Only used for
                           annotating sequence depth in GFF files (Optional)

  --config FILE            Path to user defined config
  -j, --json               Write output in json format.
  -g, --gff                Write MGE location on contig in gff format.
  -t, --threads INTEGER    Number of threads [default: 1]
  --min-coverage FLOAT     Minimum coverage
  --max-evalue INTEGER     Maximum alignment e-value
  --temp-dir PATH          Set directory for temporary files.
  --kma-path TEXT          Path to KMA, if the executable is not in PATH
  --blastn-path TEXT       Path to Blast, if the executable is not in PATH
  --makeblastdb-path TEXT  Path to Blast, if the executable is not in PATH
  --db-path PATH           Path to MGEdb
  --help                   Show this message and exit.
  ```

- **threads** :: set number of processor threads the software is allowed to use
- **min-coverage** :: set the threshold for minimum total alignment coverage of
  blast HSPs. Valid range 0 < x < 1.
- **min-identity** :: set the threshold for minimum total sequence identity
  between template and query. Valid range 0 < x < 1.
- **json** :: Write extended output in machine readable json format.
- **makeblastdb-path** :: Set custom path to blast.
- **db-path** :: Path to MGEdb. This is primarily used if Mobile Element Finder
is not installed as a python package.

  Using a custom configuration file is only recommended for advanced users. An
  example configuration file is located in `./example.config.ini`. To specify the
  path of your configuration file use the flag `--config`.

## Update MobileElementFinder

MobileElementFinder is updated with pip.

```bash
pip install -e . --upgrade
```

## Run MobileElementFinder in docker (Optional)

You can optionally use a containerized version of MobileElementFinder. This simplifies
some aspects of running the tool by ensuring that software dependencies are
correctly installed.

### Installation

Pre-built docker images of MobileElementFinder are hosted on Dockerhub. You can either
pull the latest image or a specific version with the following command.

```bash
# pull the latest build
$ docker pull mkhj/mobile_element_finder:latest

# pull version 1.0.0
$ docker pull mkhj/mobile_element_finder:1.0.0
```

### Using MobileElementFinder

To run MobileElementFinder from outside the docker container use the following make
command. It will forward the arguments to the containerized MobileElementFinder tool.

```bash
$ make run CMD="mefinder find -t 4 -f ./data/forward_reads.fastq -f ./data/reverse_reads.fastq result"
```

The folders `volumes/data` and `volumes/finder` are linked as docker volumes
which allows accesss to the local computers file system. Put the fastq and
assembled contigs in `volumes/data`. MobileElementFinder writes temporary files by default
to the temporary folder which is linked to `volumes/finder` in order to access
temporary files outside the docker image.

The tool can be run interactivly inside the container by first using the command.

```bash
$ make bash
```

## Development

Run the following command in your terminal of choice to install the development
requirements.

```bash
pip install -r requirements-devel.txt
```

To run the automated integration tests with tox use the following commands.

```bash
tox py37 py36
```

To lint the code run

```bash
tox lint
```
