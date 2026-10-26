#!/usr/bin/env python3
"""Self-contained tests for wordfreq (stdlib only, no pytest required)."""
import subprocess
import sys

WORDFREQ = "./wordfreq"


def run(args, input_text=None):
    return subprocess.run(
        [sys.executable, WORDFREQ] + args,
        input=input_text,
        capture_output=True,
        text=True,
    )


def check(name, cond, detail=""):
    print(("PASS" if cond else "FAIL") + f" {name}" + (f" -- {detail}" if detail and not cond else ""))
    return cond


def main():
    ok = True
    r = run(["--top", "2"], input_text="Hello hello world!\n")
    ok &= check("stdin top2", r.returncode == 0 and r.stdout == "2 hello\n1 world\n", repr(r.stdout))

    r = run(["--help"])
    ok &= check("help exits 0", r.returncode == 0 and "usage" in r.stdout.lower(), repr((r.returncode, r.stdout[:80])))

    r = run(["/nonexistent-file-xyz.txt"])
    ok &= check("missing file nonzero", r.returncode != 0 and "No such file" in r.stderr, repr((r.returncode, r.stderr)))

    # file args concatenated + punctuation stripping + deterministic order
    with open("/tmp/wordfreq/_t1.txt", "w") as f:
        f.write("Apple, apple! banana?")
    with open("/tmp/wordfreq/_t2.txt", "w") as f:
        f.write("banana cherry.")
    r = run(["--top", "10", "/tmp/wordfreq/_t1.txt", "/tmp/wordfreq/_t2.txt"])
    ok &= check(
        "file concat + order",
        r.returncode == 0 and r.stdout == "2 apple\n2 banana\n1 cherry\n",
        repr(r.stdout),
    )

    # default top is 10
    r = run([], input_text="a b c\n")
    ok &= check("default top", r.returncode == 0 and r.stdout == "1 a\n1 b\n1 c\n", repr(r.stdout))

    print("ALL PASS" if ok else "SOME FAILED")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
