TOPOS: Tissue-of-Origin Predictor of Onco-Samples
=================================================

A versatile machine-learning classifier based on SVMs to predict the cancer type of primary, metastasis and cell line samples.

Installation
------------

You can download TOPOS and sample input files from [here] (https://drive.google.com/open?id=1TW2kvmtVfqS1MtTNCJH9ZOc6XSZejukH).

To get it ready, you just have to unzip and cd into the topos directory.

```
unzip topos.zip
cd topos
```

Usage
-----

./topos [-h] [-v VERBOSE] n_genes normalization input_matrix output_predictions

Required positional parameters:

* n_genes : number of genes to be used in the training and prediction on the user's data. For example, if ``` n_genes ``` is 200, TOPOS will select the 200 most informative genes according to its gene ranking, and will use as many of those genes as are present in the user's data. We recommend to use 
* normalization: strategy used to scale the features in the user's data to the usual mean of 0 and standard deviation of 1. The two possible values are ``` train ``` and ``` self ```. If ``` train ```, the user's data will be scaled in the same way as the training matrix. This is the recommended behaviour if the user's data comes from the same distribution as the training data. On the other hand, ``` self ``` will scale the user's data independently of the training data, thus enforcing that each feature has a mean of EXACTLY 0 and a standard deviation of EXACTLY 1. This is recommended if the user's data comes from a distribution different to the training data, so as to minimize the batch effect.
* input_matrix: tab-separated file (tsv) with user's data, in the following format: columns represent genes (named with Entrez ids) and rows represent samples. Columns and samples must be named, so there will be a column and a row index. Sample input files are provided in the folder ``` sample_input_matrices ```.
* Output predictions: path where to write the tab-separated file (tsv) with the predictions. Sample names will be maintained, and predictions will be provided in OncoTree codes.

Optional positional parameters:

* -h, --help: shows the basic usage and a description of each parameter.
* -v, --verbose: control the verbosity of execution. If ``` True ```, an explanation for each step performed will be printed to ``` stdout ```.

Example
-------

```
./topos 500 train ./sample_input_matrices/X_primary_1.tsv P_primary.tsv --verbose True
```
