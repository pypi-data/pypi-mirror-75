import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyntacle",
    version="1.3",
    author="Tommaso Mazza",
    author_email="bioinformatics@css-mendel.it",
    description="A Python package for network analysis based on non canonical metrics and HPC computing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://pyntacle.css-mendel.it/",
    packages=setuptools.find_packages(),
    classifiers=[
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
	project_urls={
		'Documentation': 'http://pyntacle.css-mendel.it:10080/#docs',
		'Source': 'https://github.com/mazzalab/pyntacle',
		'Tracker': 'https://github.com/mazzalab/pyntacle/issues',
		'Developmental plan': 'https://github.com/mazzalab/pyntacle/projects',
	},
	keywords='network, graph, systems biology, bioinformatics',
    python_requires='>=3.7,<3.8',
	entry_points={
		'console_scripts': [
			'pyntacle = pyntacle.pyntacle:App'
        ]
	},
	install_requires=[
		"pandas",
		"seaborn",
		"setuptools",
		"colorama",
		"numba",
		"ordered-set",
		"python-igraph==0.8.2",
		"xlsxwriter==1.2.9",
		"psutil",
    ]
)