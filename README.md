# wordfreq

Small CLI that counts word frequencies from stdin or file args.

## Usage

```sh
echo 'Hello hello world!' | ./wordfreq --top 2
./wordfreq --help
./wordfreq file1.txt file2.txt --top 10
python3 wordfreq --top 5 < input.txt
```

## Tokenization rule

Lowercase all text, then extract tokens matching `[a-z0-9]+`.
All other characters (punctuation, whitespace, symbols) act as delimiters
and are stripped. Sorting is deterministic: count descending, then word
ascending. Output format is `<count> <word>` per line.

## Options

- `FILE ...` — input files, concatenated. Reads stdin when omitted.
- `--top N` — limit output to top N words (default: 10, must be >= 1).
- `--help` — print help and exit 0.

Missing/unreadable files exit nonzero with a `wordfreq: <path>: ...` message
on stderr. No dependencies beyond Python 3 stdlib.

## Tests

```sh
python3 -m pytest test_wordfreq.py -v
# or without pytest:
python3 test_wordfreq.py
```
