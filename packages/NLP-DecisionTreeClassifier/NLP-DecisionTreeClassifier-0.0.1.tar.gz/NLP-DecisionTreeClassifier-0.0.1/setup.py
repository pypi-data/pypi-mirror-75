from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='NLP-DecisionTreeClassifier',
    version='0.0.1',
    author="James Crone",
    author_email="jmcrone98@gmail.com",
    description='Decision Tree Classifier for text entities',
    package_dir={'Decision-Tree-Classifier-NLP': 'src'},
    install_requires=[
        'numpy',
        'sklearn',
        'pickle',
        'spacy',
        'wordfreq',
        'enchant',
        'pandas',
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.7',
)
