# German Asphalt Pavement Distress Dataset (GAPs)

The <ins>G</ins>erman <ins>A</ins>sphalt <ins>P</ins>avement Distres<ins>s</ins>
(GAPs) dataset addresses the issue of comparability in the pavement distress
domain by providing a standardized high-quality dataset of large size.
This does not only enable researchers to compare their work with other
approaches, but also allows to analyze algorithms on real world road surface
evaluation data.

For details see the
[GAPs dataset website](http://www.tu-ilmenau.de/neurob/data-sets-code/gaps/).

## Installation
```bash
pip install gaps-dataset
```

## Content
- Download script for GAPs dataset
- Examples for downloading patches and images

## Changelog
__Version 2.1.2 (2020/08/04)__
- adapted ftp connection

__Version 2.1.1 (2019/10/15)__
- Examples are now installed using pip

__Version 2.1.0 (2019/10/01)__
- Added script to generate patches of arbitrary size

__Version 2.0.2 (2019/09/25)__
- Added checksums for 50k ZEB subsets

__Version 2.0.1 (2019/09/12)__
- Added examples folder
- Fixed python 3 include issue

__Version 2.0.0 (2019/09/11)__
- Added support for GAPs v2 dataset

__Version 1.1.5 (2019/08/21)__
- Bugfix for loading chunks of validation or training set

__Version 1.1.4 (2017/10/27)__
- Support of python 2 and python 3

__Version 1.1.1 (2017/08/15)__
- Download of images possible (python 2 only)

__Version 1.0.0 (2017/05/09)__
- Download script for patches of size 64x64 (python 2 only)
