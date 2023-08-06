from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="Orange3–MNE",
    description="Electrophysiological data processing widgets for Orange 3 based on the MNE for Python library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    entry_points={
        "orange.widgets": (
            "EEG – 1. Data IO = EegDataIO.widgets",
            "EEG – 2. Preprocessing = EegPreprocessing.widgets",
            "EEG – 3. Feature extraction = EegFeatureExtraction.widgets",
            "EEG – 4. Classification = EegClassification.widgets",
            "EEG – 5. Visualization = EegVisualization.widgets"
        )
    },

    author="Filip Jani",
    author_email="jsem@filek.cz",
    keywords="orange3 add-on mne eeg electrophysiology",
    url="https://gitlab.com/fifal/orange-mne-library",

    install_requires=[
        "mne==0.20.3",
        "PyQt5",
        "keras==2.4.3",
        "keras-metrics==1.1.0",
        "tensorflow==2.2.0"
    ],
    version='1.0.2'
)