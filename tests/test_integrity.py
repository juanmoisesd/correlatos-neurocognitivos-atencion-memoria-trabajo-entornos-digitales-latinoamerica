import os
import pytest

def test_data_directories_exist():
    assert os.path.exists('data/raw')
    assert os.path.exists('data/clean')
    assert os.path.exists('data/analysis_ready')

def test_essential_docs_exist():
    assert os.path.exists('README.md')
    assert os.path.exists('LICENSE')
    assert os.path.exists('CITATION.cff')
