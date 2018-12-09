TOPOS: Tissue-of-Origin Predictor of Onco-Samples
=================================================

A versatile machine-learning classifier based on SVMs to predict the cancer type of primary, metastasis and cell line samples.

Installation
------------

If you don't have the required python3 modules installed (pandas, scikit-learn and scipy), go to step 1. If you have them installed, you can go directly to step 2.

### 1. Installing required python modules

These are the commands that you need to execute in order to get Ubuntu 16.04 LTS ready after a fresh installation.

```
sudo apt install python3-pip
pip3 install pandas
pip3 install scikit-learn==0.19.1
pip3 install scipy
pip3 install numpy==1.13.3
```

### 2. Getting TOPOS ready

There are to ways to use TOPOS: loading a pretrained model on the gene signature of 110 genes, or retraining the model. Using the pretrained model is recommended if every gene in the gene signature is provided in the user's data. However, retraining the model is needed if some genes are missing.

### a) Pretrained model

You can download TOPOS and the pretrained model [here](https://www.dropbox.com/s/yztuim6gb8a90he/topos.zip?dl=0). Then you just have to unzip, cd into the `topos` directory and make TOPOS executable.

```
unzip topos.zip
cd topos
sudo chmod +x topos
```

### b) Retrained model

In addition to the previous steps, you'll have to download the training matrix, which can find [here](https://www.dropbox.com/s/doh8eb0pky2y33a/df_train_prim_met_lines.pkl.zip?dl=0). Then you just have to unzip it and copy to the `required_data` directory.

```
unzip df_train_prim_met_lines.pkl.zip
mv df_train_prim_met_lines.pkl topos/required_data/
```


Usage
-----

```
./topos [-h] [-v VERBOSE] prediction_mode n_genes normalization input_matrix output_predictions
```

Required positional parameters:

* prediction_mode: desired mode to make predictions. The two possible values are ```pretrained``` and ```retrained```. If ```pretrained```, TOPOS will make predictions based on a pretrained model on the 110 genes of the gene signature. These genes are shown in the 110 first rows of ```topos/required_data/rfe_ranking.tsv```. If ```retrained```, TOPOS will retrain a model on the genes available. In order to do this, you'll need to download the training matrix (see "Getting TOPOS ready" above). Retraining is needed if the user's data lacks any of the 110 genes in the gene signature.
* n_genes : number of genes to be used in the training and prediction on the user's data. For example, if ``` n_genes ``` is 200, TOPOS will select the 200 most informative genes according to its gene ranking, and will use as many of those genes as are present in the user's data. If prediction_mode is set to ```pretrained```, n_genes will be 110 regardless of the user's input for this argument. If prediction_mode is ```retrained```, we recommend to set n_genes lower than 500 so that TOPOS' execution time stays short.
* normalization: strategy used to scale the features in the user's data to the usual mean of 0 and standard deviation of 1. The two possible values are ``` train ``` and ``` self ```. If ``` train ```, the user's data will be scaled in the same way as the training matrix. This is the recommended behaviour if the user's data comes from the same distribution as the training data. On the other hand, ``` self ``` will scale the user's data independently of the training data, thus enforcing that each feature has a mean of EXACTLY 0 and a standard deviation of EXACTLY 1. This is recommended if the user's data comes from a distribution different to the training data, so as to minimize the batch effect.
* input_matrix: tab-separated file (tsv) with user's data, in the following format: columns represent genes (named with Entrez ids) and rows represent samples. Columns and samples must be named, so there will be a column and a row index. Expression values must be provided in TPM. Sample input files are provided in the folder ``` sample_input_matrices ```.
* Output predictions: path where to write the tab-separated file (tsv) with the predictions. Sample names will be maintained, and predictions will be provided in OncoTree codes.

Optional positional parameters:

* -h, --help: shows the basic usage and a description of each parameter.
* -v, --verbose: control the verbosity of execution. If ``` True ```, an explanation for each step performed will be printed to ``` stdout ```.

Example
-------

Loading the pretrained model of TOPOS, scaling the user's data in a way that enforces that every feature has a mean of 0 and a standard deviation of 1, and saving the predictions to ```P_primary_pretrained.tsv```.

```
./topos pretrained 110 self ./sample_input_matrices/X_primary.tsv P_primary_pretrained.tsv --verbose True
```

Retraining TOPOS on the 500 best genes, scaling the user's data in the same way as the training matrix, and saving the predictions to ```P_primary_retrained.tsv```.

```
./topos retrained 500 train ./sample_input_matrices/X_primary.tsv P_primary_retrained.tsv --verbose True
```
