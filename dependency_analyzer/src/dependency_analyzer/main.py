#!/usr/bin/env python
import json
import re

from pydantic import BaseModel

from crewai.flow.flow import Flow, listen, start

from dependency_analyzer.crews.analyze_dependency_crew.analyze_dependency_crew import AnalyzeDependencyCrew
from dependency_analyzer.crews.update_dependency_crew.update_dependency_crew import UpdateDependencyCrew
import os


class DependencyAnalyzerState(BaseModel):
    input: str = ""
    output: str = ""


class DependencyAnalyzerFlow(Flow[DependencyAnalyzerState]):

    @start()
    def read_package_json(self):
        print("Reading package.json file")
        file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'package.json')
        try:
            with open(file_path, 'r') as file:
                self.state.input = file.read()
                print(self.state.input)
        except FileNotFoundError:
            print(f"The file at {file_path} was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
            print("File read", self.state.input)

    @listen(read_package_json)
    def analyze_dependency(self):
        print("Analyze dependency of package.json file")
        result = (
            AnalyzeDependencyCrew()
            .crew()
            .kickoff(inputs={"json_file": self.state.input})
        )
        print("Dependency analyzed", result.raw)

    @listen(analyze_dependency)
    def update_dependencies(self):
        print("Updating dependencies")
        result = (
            UpdateDependencyCrew()
            .crew()
            .kickoff(inputs={"json_file": self.state.input})
        )

        #print("Updated dependencies", result.raw)
        self.state.output = result.raw
        print("Updated dependencies", self.state.output)

    @listen(update_dependencies)
    def save_updated_json(self):
        print("Update json file content:", self.state.output)
        try:
            package_json_content = json.loads(self.state.output)
            out_file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'updated_package.json')
            with open(out_file_path, "w") as f:
                json.dump(package_json_content, f)  # Write the JSON content back to the file
        except json.JSONDecodeError:
            print("The output is not valid JSON.")
        except Exception as e:
            print(f"An error occurred: {e}")


def kickoff():
    dependency_flow = DependencyAnalyzerFlow()
    dependency_flow.kickoff()


def plot():
    dependency_flow = DependencyAnalyzerFlow()
    dependency_flow.plot()


if __name__ == "__main__":
    kickoff()
    #plot()
