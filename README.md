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

