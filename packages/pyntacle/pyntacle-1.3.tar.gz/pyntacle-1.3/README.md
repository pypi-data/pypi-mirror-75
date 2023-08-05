![Pyntacle logo](http://pyntacle.css-mendel.it/images/title_joined.png)

A Python package for network analysis based on non canonical
metrics and HPC computing

- **Compatibility**: Python 3.7
- **Contributions**: bioinformatics@css-mendel.it
- **Website**: http://pyntacle.css-mendel.it
- **Conda**: https://anaconda.org/bfxcss/pyntacle [![Anaconda-Server Badge](https://anaconda.org/bfxcss/pyntacle/badges/platforms.svg)](https://anaconda.org/bfxcss/pyntacle) [![Anaconda-Server Badge](https://anaconda.org/bfxcss/pyntacle/badges/downloads.svg)](https://anaconda.org/bfxcss/pyntacle)
- **Docker Hub**: https://hub.docker.com/r/mazzalab/pyntacle
- **Bug report**: https://github.com/mazzalab/pyntacle/issues
- [![Anaconda-Server Badge](https://anaconda.org/bfxcss/pyntacle/badges/platforms.svg)](https://anaconda.org/bfxcss/pyntacle)


### Description
Pyntacle answers the need for a unified software tool for the analysis of biological networks based on non-canonical 
topological metrics. It exploits the power of parallel computing for efficiently calculating the critical properties 
of networks at the local, meso, and global scales.


### CUDA support (experimental)

Independently of the OS in use, if you need CUDA support, you must
also install the CUDA toolkit by downloading and installing the Toolkit from the
[_NVIDIA website_](https://developer.nvidia.com/cuda-toolkit).

**NOTE** GPU-base processing is an **experimental** feature in the current version (1.2), and is not covered by the command-line interface. This is because of weird behaviors of Numba with some hardware configurations that we were not be able to describe and circumvent so far. Although currently accessible by APIs, the GPU feature will be stable in the release 2.0, when Pyntacle will have covered the possibility to manage huge matrices for which replacing fine-grained parallelism with GPU computing would make sense.


## License
This work is licensed under a [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
