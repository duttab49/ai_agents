from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# Importing crewAI tools
from crewai_tools import (
    DirectoryReadTool,
    FileReadTool
)

# Instantiate tools
directory_path = input("Please enter the directory path: ")
docs_tool = DirectoryReadTool(directory=directory_path)
file_tool = FileReadTool(directory=directory_path)

@CrewBase
class SourceCodeAnalyzer():
	"""SourceCodeAnalyzer crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def security_expert(self) -> Agent:
		return Agent(
			config=self.agents_config['security_expert'],
			llm='ollama/llama3.2',
			tools=[docs_tool, file_tool],
			verbose=True
		)

	@task
	def security_analysis_task(self) -> Task:
		return Task(
			config=self.tasks_config['security_analysis_task'],
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the SourceCodeAnalyzer crew"""

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
		)
