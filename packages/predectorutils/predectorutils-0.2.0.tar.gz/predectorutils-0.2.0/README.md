# predector-utils
Utilities for running the predector pipeline.

[![Build Status](https://travis-ci.org/ccdmb/predector-utils.svg?branch=master)](https://travis-ci.org/ccdmb/predector-utils)


This is where the models and more extensive utility scripts are developed.

All command line tools are accessible under the main command `predutils`.

## `predutils r2js`

Convert the output of one of the analyses into a common [line delimited JSON](http://ndjson.org/) format.
The json records retain all information from the original output files, but are much easier to parse because each line is just JSON.

Basic usage:

```bash
predutils r2js \
  -o outfile.ldjson \
  --pipeline-version 0.0.1 \
  signalp3_nn \
  signalp3_nn_results.txt
```


Analyses available to parse in place of `signalp3_nn` are:
`signalp3_nn`, `signalp3_hmm`, `signalp4`, `signalp5`, `deepsig`, `phobius`, `tmhmm`,
`deeploc`, `targetp_plant` (v2), `targetp_non_plant` (v2), `effectorp1`, `effectorp2`,
`apoplastp`, `localizer`, `pfamscan`, `dbcan` (HMMER3 domtab output), `phibase` \*, `pepstats`.

\* assumes search with MMseqs with tab delimited output format columns: query, target, qstart, qend, qlen, tstart, tend, tlen, evalue, gapopen, pident, alnlen, raw, bits, cigar, mismatch, qcov, tcov.


## `predutils encode`

Preprocess some fasta files.

1. Strips trailing `*` amino acids from sequences, replaces internal `*`s and other redundant amino acids with `X`, and converts sequences to uppercase.
2. removes duplicate sequence using a checksum, saving the mapping table to recover the duplicates at the end of the analysis.
3. Replace the names of the deduplicated sequences with a short simple one.


Basic usage:

```bash
predutils encode \
  output.fasta \
  output_mapping.tsv \
  input_fastas/*
```

Note that it can take multiple input fasta files, and the filename is saved alongside the sequences in the output mapping table to recover that information.


By default, the temporary names will be `SR[A-Z0-9]5` e.g. `SR003AB`.
You can change the prefix (default `SR`) with the `--prefix` flag, and the number of id characters (default 5) with the `--length` parameter.



## `predutils split_fasta`

Splits a fasta files into several files each with a maximum of n sequences.

Basic usage:

```bash
predutils split_fasta --template 'chunk{index}.fasta' --size 100 in.fasta
```

The `--template` parameter accepts python `.format` style string formatting, and
is provided the variables `fname` (the input filename) and `index` (the chunk number starting at 1).
To pad the numbers with zeros for visual ordering in directories, use the something like `--template '{fname}.{index:0>4}.fasta'`.
Directories in the template will be created for you if they don't exist.


## `predutils decode`

The other end of `predutils encode`.
Takes the common line delimited format from analyses and separates them back
out into the original filenames.

```bash
predutils decode \
  --template 'decoded/{filename}.ldjson' \
  output_mapping.tsv \
  results.ldjson
```

We use the template flag to indicate what the filename output should be, using python format
style replacement. Available values to `--template` are `filename` and `filename_noext`.
The latter is just `filename` without the last extension.


## `predutils tables`

Take the common line delimited output from `predutils r2js` and recover a tabular version of the raw data.
Output filenames are controlled by the `--template` parameter, which uses python format style replacement.
Currently, `analysis` is the only value available to the template parameter.
Directories in the template will be created automatically.

```
predutils tables \
  --template "my_sample-{analysis}.tsv" \
  results.ldjson
```


## `predutils gff`

Take the common line-delimited json output from `predutils r2js` and get a GFF3 formatted
set of results for analyses with a positional component (e.g. signal peptides, transmembrane domains, alignment results).

```
predutils gff \
  --outfile "my_sample.gff3" \
  results.ldjson
```

By default, mmseqs and HMMER search results will be filtered by the built in significance thresholds.
To include all matches in the output (and possibly filter by your own criterion) supply the flag `--keep-all`.


## `predutils rank`

Take the common line-delimited json output from `predutils r2js` and get a summary table
that includes all of the information commonly used for effector prediction, as well as
a scoring column to prioritise candidates.

```
predutils rank \
  --outfile my_samples-ranked.tsv \
  results.ldjson
```


To change that Pfam or dbCAN domains that you consider to be predictive of effectors,
supply a text file with each pfam or dbcan entry on a new line (do not include pfam version number or `.hmm` in the ids) to the parameters `--dbcan` or `--pfam`.

You can also change the weights for how the score columns are calculated.
See `predutils rank --help` for a full list of parameters.
