
**SuperalloyDataExtractor**
----------------------
The functions of superalloydataextractor toolkit include batch downloading documents in XML and TXT format from the Elsevier database, locating target sentences from the full text and automatically extracting triple information in the form of <material name, property specifier, value>.

This package is released under MIT License, please see the LICENSE file for details.

**Features**
----------------------
- Rule-based named entity recognition for superalloy.
- An automated data extraction pipeline for superalloy.
- Algorithm based on distance and number of entities, processing multiple relationship extraction without labeling samples.

**Superalloy Data Extractor Code**
----------------------
This code extracts data of property from TXT files. These TXT files need to be supplied by the researcher. The code is written in Python3. To run the code:

    1. Fork this repository
    2. Download the word embeddings
    	- Available here: https:
    	- Download all 4 files and place in the superalloydataextractor/bin folder
    	- Place all files in superalloydataextractor/data

**USAGE**
----------------------
Clone this github repository and run
```
python3 setup.py install
```

Or simply use the code in your own project.

**LICENSE**
----------------------
All source code is licensed under the MIT license.

**Install**
----------------------
```
pip install superalloydataextractor
```
or if you are an Anaconda user, run:

```
conda install -c superalloydataextractor superalloydataextractor
```
