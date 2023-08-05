# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cancer_data', 'cancer_data.processors']

package_data = \
{'': ['*'],
 'cancer_data': ['data/preview/.keep',
                 'data/processed/.keep',
                 'data/raw/.keep',
                 'data/reference/.keep']}

install_requires = \
['gtfparse>=1.2.0,<2.0.0',
 'pandas>=1.0.5,<2.0.0',
 'requests>=2.24.0,<3.0.0',
 'scipy>=1.5.1,<2.0.0',
 'tables>=3.6.1,<4.0.0',
 'tqdm>=4.48.0,<5.0.0',
 'xlrd>=1.2.0,<2.0.0']

setup_kwargs = {
    'name': 'cancer-data',
    'version': '0.1.1',
    'description': 'Preprocessing for various cancer genomics datasets',
    'long_description': '# cancer_data\n\nThis package handles the downloading and processing of several public genomics datasets useful for cancer research.\n\n## Datasets\n\nA complete description of the datasets may be found in [schema.txt](https://github.com/kevinhu/cancer-data/blob/master/cancer_data/schema.txt).\n\n| Collection                                    | Datasets                                                     | Portal                                                       |\n| --------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |\n| Cancer Cell Line Encyclopedia (CCLE)          | Many (see portal)                                            | https://portals.broadinstitute.org/ccle/data (registration required) |\n| Cancer Dependency Map (DepMap)                | Genome-wide CRISPR-cas9 and RNAi screens, gene expression, mutations, and copy number | https://depmap.org/portal/download/                          |\n| The Cancer Genome Atlas (TCGA)                | Mutations, RNAseq expression and splicing, and copy number   | https://xenabrowser.net/datapages/?cohort=TCGA%20Pan-Cancer%20(PANCAN)&removeHub=https%3A%2F%2Fxena.treehouse.gi.ucsc.edu%3A443 |\n| The Genotype-Tissue Expression (GTEx) Project | RNAseq expression and splicing                               | https://gtexportal.org/home/datasets                         |\n\n## Features\n\nThe goal of this package is to make statistical analysis and coordination of these datasets easier. To that end, it provides the following features:\n\n1. Harmonization: datasets within a collection have sample IDs reduced to the same format. For instance, all CCLE+DepMap datasets have been modified to use Achilles/Arxspan IDs, rather than cell line names.\n2. Speed: processed datasets are all stored in high-performance [HDF5 format](https://en.wikipedia.org/wiki/Hierarchical_Data_Format), allowing large tables to be loaded orders of magnitude faster than with CSV or TSV formats.\n3. Space: tables of purely numerical values (e.g. gene expression, methylation, drug sensitivities) are stored in half-precision format.\n\n## How it works\n\nThe [schema](https://github.com/kevinhu/cancer-data/blob/master/cancer_data/schema.txt) serves as the reference point for all datasets used. Each dataset is identified by a unique `id` column, which also serves as its access identifier.\n\nDatasets are downloaded from the location specified in `download_url`, after which they are checked against the provided `downloaded_md5` hash.\n\nThe next steps depend on the `type` of the dataset:\n\n- `reference` datasets, such as the hg19 FASTA files, are left as-is.\n- `primary_dataset` objects are preprocessed and converted into HDF5 format.\n- `secondary_dataset` objects are defined as being made from `primary_dataset` objects. These are also processed and converted into HDF5 format.\n\nTo keep track of which datasets are necessary for producing another, the `dependencies` column specifies the dataset `id`s that are required for making another. For instance, the `ccle_proteomics` dataset is dependent on the `ccle_annotations` dataset for converting cell line names to Achilles IDs. When running the processing pipeline, the script will automatically check that dependencies are met, and raise an error if they are not found.\n\n## Notes\n\n### Filtering\nSome datasets have filtering applied to reduce their size. These are listed below:\n- CCLE, GTEx, and TCGA splicing datasets have been filtered to remove splicing events with many missing values as well as those with low standard deviations.\n- When constructing binary mutation matrices (`depmap_damaging` and `depmap_hotspot`), a minimum mutation frequency is used to remove especially rare mutations.\n\n### System requirements\nThe size of the downloaded raw files is approximately 15 GB, and that of the processed HDFs is about 20 GB. On a relatively recent machine with a fast SSD,  processing all of the files after download takes about 3-4 hours. At least 16 GB of RAM is recommended for handling the large splicing tables.\n',
    'author': 'Kevin Hu',
    'author_email': 'kevinhuwest@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kevinhu/cancer_data',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
