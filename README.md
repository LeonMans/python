# My Python Project

This repository contains several helper scripts used for histogram and cross
section calculations.  A new helper script, `hist_processes.py`, allows one to
create histograms for specific processes individually.

## Creating histograms for individual processes

To generate histograms for a given mode and a list of processes, run:

```bash
python python/calc_hist/hist_processes.py MODE "PROC1,PROC2" [options]
```

The available options mirror those in `hist_hweight.py` (PDF set, paths, etc.).
Each specified process is handled separately and the results are written to
`<out_path>/<pdf>/scale_unc/<mode>_<process>`.

Example:

```bash
python python/calc_hist/hist_processes.py RS "dg_susx,gu"
```

This will produce two sets of histograms, one for `dg_susx` and one for `gu`.
