import argparse
import json
import subprocess
import sys

import pandas as pd
import numpy as np


class Probe:
    finished = False

    def __init__(self, config):
        self.config = config

    def start(self):
        self.process = proc = subprocess.Popen(
            [sys.executable, "-m", "import_profile.probe"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        proc.stdin.write(json.dumps(self.config).encode("utf-8"))
        proc.stdin.write(b"\n")
        proc.stdin.flush()

    def read_output(self):
        if not self.finished:
            self.output = json.loads(
                self.process.stdout.readline().decode("utf-8")
            )
            self.finished = True
        return self.output

    def stop(self):
        proc = self.process
        self.read_output()
        proc.stdin.write(b"bye\n")
        proc.stdin.flush()
        proc.wait()


def main():
    ap = argparse.ArgumentParser(description="profile module imports")
    ap.add_argument(
        "-N",
        "--runs",
        type=int,
        default=3,
        help="number of trials (default: 3)",
    )
    ap.add_argument("--output-csv", help="CSV output file")
    ap.add_argument("modules", nargs="+", help="modules to load")
    A = ap.parse_args()

    relevant_modules = A.modules
    relevant_modules_set = set(relevant_modules)

    rows = []

    config = {"modules": relevant_modules}

    background_probe = Probe(config)
    background_probe.start()
    output = background_probe.read_output()
    # Keep the background probe alive, so that shared objects (DLLs)
    # don't count towards `memory.uss`

    # First step: sort the imports
    relevant_modules = []
    for timestamp, logtype, *args in output:
        if logtype == "end_import":
            module_name = args[0]
            if module_name in relevant_modules_set:
                relevant_modules.append(module_name)

    if set(relevant_modules) != relevant_modules_set:
        raise AssertionError(
            "failed to sort modules, missing modules {!r}".format(
                relevant_modules_set - set(relevant_modules)
            )
        )

    config = {"modules": relevant_modules}
    print(" ".join(relevant_modules))

    for i in range(A.runs):
        probe = Probe(config)
        probe.start()
        output = probe.read_output()
        probe.stop()

        first = True
        start_timestamp = None
        imported = set()
        process_status = None

        for timestamp, logtype, *args in output:
            if logtype == "sys_modules":
                for module_name in args[0]:
                    imported.add(module_name)
            elif logtype == "process":
                process_status = args[0].copy()
                if start_timestamp is None:
                    process_status["time"] = 0.0
                    start_timestamp = timestamp
                else:
                    process_status["time"] = timestamp - start_timestamp
            elif logtype == "end_manual_import" or (
                logtype == "begin_manual_import" and first
            ):
                row = {}
                row.update(
                    ("imported." + k, int(k in imported))
                    for k in relevant_modules
                )
                row.update(process_status)
                rows.append(row)
                first = False

    background_probe.stop()

    df = pd.DataFrame(rows)

    independent_columns = set(
        c for c in df.columns if c.startswith("imported.")
    )
    dependent_columns = set(df.columns) - independent_columns

    independent = df[list(sorted(independent_columns))]
    independent = independent.rename(
        {"imported." + k: k for k in relevant_modules}, axis=1
    )
    independent = independent[relevant_modules]
    independent["*base*"] = 1.0

    dependent = df[list(sorted(dependent_columns))].copy()

    X = independent.values
    Y = dependent.values
    # solve XA = Y
    coeff_, residuals, rank, singular = np.linalg.lstsq(X, Y, rcond=None)

    coeff = pd.DataFrame(
        data=coeff_, columns=dependent.columns, index=independent.columns
    )

    for k in coeff.columns:
        if k.startswith("memory."):
            v = coeff[k]
            v /= 1024.0 ** 2
            v[:] = v.where(abs(v) >= 0.01, 0.0)

    if A.output_csv:
        coeff.to_csv(A.output_csv)

    print()
    print(coeff[["time", "cpu.user", "cpu.system", "memory.uss", "memory.rss"]])
    print(
        """
time       = seconds of real time since the import trial began
cpu.user   = seconds of CPU time spent in this process
cpu.system = seconds of CPU time spent waiting for the OS kernel, such
             as waiting for file I/O to complete
memory.uss = unique set size - memory taken up by process, minus
             shared objects/DLLs (megabytes)
memory.rss = resident set size (megabytes)"""
    )
