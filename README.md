# wordfreq

A small CLI that counts word frequencies, reading from stdin or file arguments.

## Install

Requires Python 3 (standard library only — no dependencies).

```sh
git clone https://github.com/igorjpimenta/wordfreq
cd wordfreq
chmod +x wordfreq
```

## Usage

Reads stdin when no files are given:

```sh
echo 'the quick brown fox jumps over the lazy dog the fox' | ./wordfreq
```

Output:

```
3 the
2 fox
1 brown
1 dog
1 jumps
1 lazy
1 over
1 quick
```

Or pass one or more files (concatenated):

```sh
./wordfreq sample.txt
./wordfreq file1.txt file2.txt
```

## Options

| Option | Description |
| --- | --- |
| `FILE ...` | Input files, concatenated. Reads stdin when omitted. |
| `--top N` | Limit output to the top N words. Defaults to 10; must be >= 1. |

Show help:

```sh
./wordfreq --help
```

## Tokenization

The tool lowercases all text, then extracts tokens matching `[a-z0-9]+` —
ASCII letters and digits only. Every other character (punctuation,
whitespace, symbols) acts as a delimiter and is stripped. So
`Hello, world!` yields the words `hello` and `world`.

## Output

One line per word in the format:

```
<count> <word>
```

Sorted deterministically: count descending, then word ascending.

Missing files exit with a nonzero status and a `wordfreq: <path>: No such
file or directory` message on stderr.

## Examples

```sh
$ echo 'Hello, world! Hello again.' | ./wordfreq --top 2
2 hello
1 world
```

```sh
$ ./wordfreq --top 2 sample.txt
3 world
2 hello
```

## Tests

```sh
python3 -m pytest test_wordfreq.py -v
```
