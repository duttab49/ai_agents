from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class UpdateDependencyCrew:
    """UpdateDependency Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def update_dependency_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["update_dependency_agent"],
            llm='ollama/llama3.2',
        )

    @task
    def update_dependencies(self) -> Task:
        return Task(
            config=self.tasks_config["update_dependencies"],
        )

    @crew
    def crew(self) -> Crew:
        """Update the dependencies in package.json file"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
