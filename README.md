# Deploying Machine Learning Models

Code used in a workshop on deploying machine learning models and MLOPs for the November 2021 Cohort Training for the AIMLAC Doctoral Training Centre, UK.

The repro is an example of how to produce a reproducible pipeline for training a machine learning model for text categorisation. It focuses on the binary classification task of separating ham from spam text messages, using a [kaggle dataset of 5157 text messages](https://www.kaggle.com/team-ai/spam-text-message-classification).

The various stages of the presentation have been labelled with git tags, so you can easily jump to the stage of interest. These stages are described below with the commands used to create them (if applicable).

## Setting up the virtual environment (0-dependencies)

Populate the `unpinned-requirements.txt` with the main depdendencies required by the project.

Additional test and development depdendencies can be set in `requirements_test.txt` and `requirements_dev.txt` respectively.

Run:

```
make update-requirements-txt
``` 

...to populate `requirements.txt`, and:

```
make virtualenv
```

...to create a virtual environment.

To activate the virtual environment run: 

```
source ./build/virtualenv/bin/activate
```

You can also add the following to your ~/.bashrc (or equivalent) to allow you to just run `activate`:

```
function activate {
    source build/virtualenv/bin/activate
}
```

You'll then need to run `source ~/.bashrc` to make this function available in your current shell.

## Adding the raw data to Data Version Control (1-data-version-control)

The next step is to get the data. This is available from [kaggle](https://www.kaggle.com/team-ai/spam-text-message-classification) on an [CC0 license](https://creativecommons.org/publicdomain/zero/1.0/), but you will need to have a kaggle account and be signed in to access the download link.

The downloaded dataset should be:

|name|size|rows|
|---|---|---|
|SPAM text message 20170820 - Data.csv|485.7kb|5574|

Download this dataset and put it in a new folder called `./data/raw/`

```
mkdir -p ./data/raw
```

Then add `dvc[s3]` to the unpinned depdendencies and update the virtualenv:

```
echo "dvc[s3]" >> unpinned_requirements.txt
make update-requirements-txt virtualenv
```

Next, add the raw data to dvc with:

```
dvc add data/raw/SPAM\ text\ message\ 20170820\ -\ Data.csv
```

This will add two new files `./data/raw/.gitignore`, and will prompt us to add both, which we should do:

```
git add ./data/raw/.gitignore ./data/raw/SPAM text message 20170820 - Data.csv.dvc

# Commit following your own flow, but as an example:

git commit -m 'new: Added raw data to data/raw'
```

Optionally (though, ideally) you can also set a dvc remote, for example an s3 bucket:

```
dvc remote add s3 s3://mantisnlp-blogs/deploying-ML
dvc remote default s3
dvc push
```

