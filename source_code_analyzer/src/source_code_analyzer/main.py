#!/usr/bin/env python
import os
import sys
import warnings

# Add the directory containing source_code_analyzer to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from source_code_analyzer.crew import SourceCodeAnalyzer

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    SourceCodeAnalyzer().crew().kickoff()

if __name__ == "__main__":
    run()