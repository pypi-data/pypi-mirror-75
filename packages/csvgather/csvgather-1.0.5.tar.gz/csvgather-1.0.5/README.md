# csvgather

Utility for gathering multiple character-separated value files and joining into
a single matrix. Similar to [csvjoin](http://csvkit.readthedocs.io/en/latest/scripts/csvjoin.html)
from the [csvkit](http://csvkit.readthedocs.io) package, or the `join` function
of [csvtk](bioinf.shenwei.me/csvtk), except allows column headers to be renamed
based on the filename. This is an extremely common operation in, e.g.
bioinformatic analyses, when the same utility, which produces a file with static
headers, is run for many samples, differing only in some portion of the
filename.

## Installation

You can install using `pip`:

```
pip install csvgather
```

## tl;dr

If you have a bunch of files created using the RNA-Seq gene expression
quantification tool [kallisto](https://pachterlab.github.io/kallisto/about)
named like:

```
<sample name>__kallisto_counts/abundance.tsv
```

and each file has the following columns:

```
target_id length eff_length est_counts tpm
```

and you want to concatenate these files to create a new matrix of `est_counts`
that looks like:

```
target_id  sample_A  sample_B  sample_C
geneA             1         2         8
geneB             0         0         0
geneC           152      1353       999
...
```

You would run:

```
csvgather -j 0 -f est_counts -t "s:est_counts:{dir}:" -t "s:__kallisto_counts::" \
    sample_*__kallisto_counts/abundance.tsv
```

## Full Explanation

Say you're starting with the following files:

```
sample_A__kallisto_counts/abundance.tsv
sample_B__kallisto_counts/abundance.tsv
sample_C__kallisto_counts/abundance.tsv
```

In each file there is an `est_counts` column that contains estiamted read
counts that map to genes or transcripts, one per row. For downstream analysis,
we need to have all of these counts in a single matrix, and having them all
in a single file is desirable.

```
target_id  sample_A  sample_B  sample_C
geneA             1         2         8
geneB             0         0         0
geneC           152      1353       999
...
```

Since the command line tools for doing this concatenation don't support
renaming columns, this concatenation would need to be implemented in custom
code for every analysis. `csvgather` is designed to enable fast and flexible
concatenation to handle this use case through the use of column name
transformations.

A column name transformation is a regular expression substitution taking the
form of `s:<pattern>:<replace>:[gi]`. Semi-colons are used rather than forward
slashes because otherwise the pattern separation character would often collide
with the directory separation character. Additionally, there are a few special
variables available in the `<replace>` string:

- {path}:      expands to the full path to the file provided on the command line
- {dir}:       the path to the file, without the filename
- {fn}:        just the filename, without the preceding path
- {basename}:  the basename of the file (i.e. full path without extension)

These substitution variables enable column names to be set using portions of
the filename.

We start with the following base command:

```
csvgather -j 0 -f est_counts sample_*__kallisto_counts/abundance.tsv
```

The `-j 0` means 'join all files on the first column', and `-f est_counts`
indicates that the column named `est_counts` should be extracted from every
file. This command would yield a file like

```
target_id  est_counts  est_counts  est_counts
geneA               1           2           8
geneB               0           0           0
geneC             152        1353         999
...
```

The columns are indistinguishable from one another. We can add a simple
transformation to the command and replace the column name with the
directory name of each file since that contains unique sample identifiers:

```
csvgather -j 0 -f est_counts -t 's:est_counts:{dir}:' est_counts sample_*__kallisto_counts/abundance.tsv
```

This will yield a file with:

```
target_id  sample_A__kallisto_counts  sample_B__kallisto_counts  sample_C__kallisto_counts
geneA                              1                          2                          8
geneB                              0                          0                          0
geneC                            152                       1353                        999
...
```

Better, but still not great. Since each of the headers now contains the
common substring `__kallisto_counts`, we can remove them using another
transformation:

```
csvgather -j 0 -f est_counts -t 's:est_counts:{dir}:' -t 's:__kallisto_counts::' \
    sample_*__kallisto_counts/abundance.tsv
```

In other words, we search for the string `__kallisto_counts` in each column name and
remove it (i.e. replace it with nothing). Finally, this yields the desired result:

```
target_id  sample_A  sample_B  sample_C
geneA             1         2         8
geneB             0         0         0
geneC           152      1353       999
...
```

Transformations are performed serially from left to right, and are applied to
each filename provided. Happy concatening.

## Usage

```
Usage: csvgather.py [options] [-j PATT]... [-f PATT]... [-t STR]... <csv_fn>...

Options:
  -h --help               This helpful help help help help is a weird word
  -d STR --delimiter=STR  Character(s) to use as the delimiter in the output,
                          can be multiple characters [default:  ]
  -o PATH --output=PATH   Output to file [default: stdout]
  -j COL --join=COL       Column(s) to join on. Can take one of four forms:
                            - 0-based integer indicating column index, can be
                              negative to index from the end of the columns
                            - a half closed interval of 0-based integers to
                              specify a range of columns (e.g. 0:4 or 0:-1)
                            - a regular expression that will use any columns it
                              matches as the join columns
                            - a pair of regular expressions to specify a range
                              of columns (e.g. geneName:strand will start with
                              the column geneName and end with column strand)
                          If more than one column matches, then a warning is
                          issued but the join continues on the aggregate of the
                          columns. ':' or special regular expression characters
                          (e.g. +, *, [, ], etc) in column names must be
                          wrapped in [], e.g. '[:]'. Can be specified multiple
                          times, in which case all selected columns are unioned
                          together [default: 0]
  -f COL --field=COL      Column(s) to select fields for concatenation. Uses
                          the same format as -j option. May be specified
                          multiple times and any matching columns will be
                          included. Column selection occurs before application
                          of transformations (-t). Joined columns are not
                          included in the field match [default: .]
  -t STR --transform=STR  A string of the form "s:patt:repl:[gi]" to apply to
                          every column name. The special strings {path}, {dir},
                          {fn}, and {basename} can be used in the repl string to
                          refer to the full path, parent directory name, file
                          name, and filename without extension (i.e. [.][^.]*$)
                          May be specified multiple times, in which case the
                          transformations will be performed sequentially in the
                          order specified on the command line [default: s:.:.:]
  --join-type=STR         Type of join, one of 'outer', 'inner', or 'left'.
                          outer will create a row for every distinct value in
                          the -j column(s), inner will report only rows that
                          are found in all files, and left will join files from
                          left to right [default: outer]
  --empty-val=VAL         The value to use when an outer or left join does not
                          find a corresponding row in a file [default: ]
  --comment=CHARS         Characters to be considered comments in input files
                          and will be skipped. Can be any number of characters
                          e.g. #@- [default: #]

```
