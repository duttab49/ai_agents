from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class AnalyzeDependencyCrew:
    """AnalyzeDependency Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def analyze_dependency_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["analyze_dependency_agent"],
            llm='ollama/llama3.2',
        )

    @task
    def analyze_dependencies(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_dependencies"],
        )

    @crew
    def crew(self) -> Crew:
        """Analyze the dependencies in package.json file"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
