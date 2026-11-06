from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, task

groq_llm = LLM(
    model="groq/openai/gpt-oss-120b",
    temperature=0.8,
)


@CrewBase
class ShoulderDebate():
    """Angel vs. Devil crew, run in rounds"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ***** Agents *****
    @agent
    def angel(self) -> Agent:
        return Agent(config=self.agents_config['angel'], llm=groq_llm, verbose=True)

    @agent
    def devil(self) -> Agent:
        return Agent(config=self.agents_config['devil'], llm=groq_llm, verbose=True)

    # ***** Tasks *****
    @task
    def angel_opening(self) -> Task:
        return Task(config=self.tasks_config['angel_opening'], agent=self.angel())

    @task
    def devil_opening(self) -> Task:
        return Task(
            config=self.tasks_config['devil_opening'],
            agent=self.devil(),
            context=[self.angel_opening()],
        )

    @task
    def angel_rebuttal(self) -> Task:
        return Task(config=self.tasks_config['angel_rebuttal'], agent=self.angel())

    @task
    def devil_rebuttal(self) -> Task:
        return Task(
            config=self.tasks_config['devil_rebuttal'],
            agent=self.devil(),
            context=[self.angel_rebuttal()],
        )

    # ***** Crews *****
    def opening_crew(self) -> Crew:
        return Crew(
            agents=[self.angel(), self.devil()],
            tasks=[self.angel_opening(), self.devil_opening()],
            process=Process.sequential,
            verbose=True,
        )

    def rebuttal_crew(self) -> Crew:
        return Crew(
            agents=[self.angel(), self.devil()],
            tasks=[self.angel_rebuttal(), self.devil_rebuttal()],
            process=Process.sequential,
            verbose=True,
        )