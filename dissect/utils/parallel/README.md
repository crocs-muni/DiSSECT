# Experiment parallelizer

Helps parallelize experiments on a single machine by executing computing jobs on a given number of threads in parallel.

The experiment should be designed in such a way that jobs are independent of each other, no communication is required
between jobs. Each job should save it's results to an individual result file (JSON ideally). Individual result files
could be merged by user after experiment finishes.

Take a look at `example_experiment.py`. It defines some basic dummy experiment.

The `example_script.sage` represents an individual job script which is executed by the parallelizer with parameters
passed via CLI.

Example of usage:

```bash
python3 -m example_experiment --sage /Applications/SageMath/sage --resdir results --tasks 2
```

- Defines path to the Sage executable
- All result files will go to the `results/` dir
- Execute 2 tasks in parallel

## Installation

```bash
pip3 install sarge shellescape coloredlogs
```
