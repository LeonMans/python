#!/usr/bin/env python3
"""Generate histograms for individual processes.

This script wraps ``hist_hweight.calc_hist_ord`` so that each process is
handled separately.  The output for each process is placed in a unique
subdirectory ``<mode>_<process>`` under ``scale_unc``.

Usage
-----
    python hist_processes.py MODE PROC1,PROC2 [options]

Options
-------
  --order   perturbative order (default: nlo)
  --ngamma  photon power for rescaling (default: 1)
  --pdf     PDF set to use (default: NNPDF31_nlo_as_0118_luxqed)
  --path    directory containing the input histograms
  --out-path  directory for the output histograms
  --iord    comma separated list of strong coupling orders (default: none)

The list of available processes per mode is defined in ``proc_info.py``.
"""
import argparse
import sys
import os

sys.path.append('../')
from proc_info import get_process
import hweight_input as hweight


def main():
    parser = argparse.ArgumentParser(description="Create histograms for individual processes")
    parser.add_argument("mode", help="name of the calculation mode")
    parser.add_argument("processes", help="comma separated list of processes")
    parser.add_argument("--order", default="nlo")
    parser.add_argument("--ngamma", type=int, default=1)
    parser.add_argument("--pdf", default="NNPDF31_nlo_as_0118_luxqed")
    parser.add_argument("--path", default="/mount/vol2/data/stremmer/event_files/tt_semi/nlo_qcut/")
    parser.add_argument("--out-path", dest="out_path", default="../../samples/nlo/")
    parser.add_argument("--iord", default="", help="comma separated list of strong coupling orders")
    args = parser.parse_args()

    procs, corrfac = get_process(args.mode, args.ngamma)
    corr_map = dict(zip(procs, corrfac))

    if args.iord:
        iorders = [int(x) for x in args.iord.split(',') if x]
    else:
        iorders = []

    req_procs = [p.strip() for p in args.processes.split(',') if p.strip()]
    for proc in req_procs:
        if proc not in corr_map:
            raise ValueError(f"Process '{proc}' not defined for mode '{args.mode}'")
        sub = f"_{proc}"
        hweight.calc_hist_ord(
            args.order,
            args.mode,
            [proc],
            args.pdf,
            args.path,
            args.out_path,
            iord=iorders,
            sub=sub,
            rescal=[corr_map[proc]],
        )
        print(f"Histogram for {proc} written to {args.out_path}{args.pdf}/scale_unc/{args.mode}{sub}")


if __name__ == "__main__":
    main()
