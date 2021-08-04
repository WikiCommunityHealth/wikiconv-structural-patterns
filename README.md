# WikiConv Structural Patterns
This repository contains most of the work developed by Francesco Bozzo during his Bachelor's Degree traineeship at Eurecat in 2021.
The project has been supervised by Cristian Consonni and David Laniado.

### The project
This project aims to provide a tool to develop and analyze metrics on Wikipedia Talk Pages using the [WikiConv Dataset](https://github.com/conversationai/wikidetox/tree/main/wikiconv), described in [this article](https://arxiv.org/abs/1810.13181).

It is a modular program which can be used to calculate any metric on any type of sorting.
Here it is possible to find some of its main features:
- it can handle compressed inputs in order to reduce the required disk space to store the datasets;
- it can handle streams of data using Python generators, preventing the loading of the full dataset in RAM;
- each run is fully configurable through a TOML file where it is possible to provide the sorting pivot field and the full list of metrics to analyze;
- the output of the analysis is stored in a PostgreSQL database with a well-defined format;
- it groups the metrics by year-month according to the format `YYYY-MM`;
- new metrics to track can be easily implemented thanks to its modular structure enforced by the Object Oriented Programming paradigm.

### TOML configurable runs
TODO

### Metrics
Each trackable metric has to be implemented as a class inside the [metric folder](https://github.com/WikiCommunityHealth/wikiconv-structural-patterns/tree/main/src/analyzer/metrics). It must inherit from the abstract base class [`Metric`](https://github.com/WikiCommunityHealth/wikiconv-structural-patterns/blob/main/src/analyzer/metrics/metric.py). Each metric child class need to respect the base class backbone, implementing the two following methods:
- `block-preprocessing()`, that takes as input a stream of records which represents a block, and should process them in order to compute a specific metric on a monthly basis;
- `output-metrics()`, which takes as input a metric computed on a monthly basis and should calculate other related values, including cumulative and normalized forms.

### Implemented metrics
TODO

### Usage
```bash
cd src/
python -m analyzer ../data/pages/wikiconv-page-ca/* ./config_page.toml -c gzip
```
