#!/usr/bin/env python3
"""Tests for wordfreq (stdlib only: unittest, no third-party deps).

Run from repo root:
    python3 test_wordfreq.py
    python3 -m unittest test_wordfreq -v
    python3 -m pytest test_wordfreq.py -v
"""
import subprocess
import sys
import tempfile
import os
import unittest

WORDFREQ = "./wordfreq"


def run(args, input_text=None):
    return subprocess.run(
        [sys.executable, WORDFREQ] + args,
        input=input_text,
        capture_output=True,
        text=True,
    )


class TestWordfreq(unittest.TestCase):
    def test_stdin_top2(self):
        r = run(["--top", "2"], input_text="Hello hello world!\n")
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stdout, "2 hello\n1 world\n")

    def test_help_exits_0(self):
        r = run(["--help"])
        self.assertEqual(r.returncode, 0)
        self.assertIn("usage", r.stdout.lower())

    def test_missing_file_nonzero(self):
        r = run(["/nonexistent-file-xyz.txt"])
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("No such file", r.stderr)

    def test_file_concat_order(self):
        with tempfile.TemporaryDirectory() as d:
            t1 = os.path.join(d, "t1.txt")
            t2 = os.path.join(d, "t2.txt")
            with open(t1, "w") as f:
                f.write("Apple, apple! banana?")
            with open(t2, "w") as f:
                f.write("banana cherry.")
            r = run(["--top", "10", t1, t2])
            self.assertEqual(r.returncode, 0)
            self.assertEqual(r.stdout, "2 apple\n2 banana\n1 cherry\n")

    def test_file_single(self):
        with tempfile.TemporaryDirectory() as d:
            t3 = os.path.join(d, "t3.txt")
            with open(t3, "w") as f:
                f.write("dog cat dog\n")
            r = run(["--top", "5", t3])
            self.assertEqual(r.returncode, 0)
            self.assertEqual(r.stdout, "2 dog\n1 cat\n")

    def test_lowercase_punctuation(self):
        r = run(["--top", "10"], input_text="Hello, HELLO hello... world! World? WORLD:\n")
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stdout, "3 hello\n3 world\n")

    def test_digits_kept(self):
        r = run(["--top", "10"], input_text="abc123 ABC123!\n")
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stdout, "2 abc123\n")

    def test_tie_order_word_asc(self):
        r = run(["--top", "10"], input_text="b a b a c\n")
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stdout, "2 a\n2 b\n1 c\n")

    def test_top_limit(self):
        r = run(["--top", "2"], input_text="a b c\n")
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stdout, "1 a\n1 b\n")

    def test_default_top_is_10(self):
        words15 = " ".join(f"w{i:02d}" for i in range(1, 16)) + "\n"
        r = run([], input_text=words15)
        expected = "".join(f"1 w{i:02d}\n" for i in range(1, 11))
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stdout, expected)

    def test_empty_stdin(self):
        r = run(["--top", "5"], input_text="")
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stdout, "")

    def test_punct_only_stdin(self):
        r = run(["--top", "5"], input_text="!!! ??? ...\n")
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stdout, "")

    def test_top_zero_rejected(self):
        r = run(["--top", "0"], input_text="a b\n")
        self.assertNotEqual(r.returncode, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
