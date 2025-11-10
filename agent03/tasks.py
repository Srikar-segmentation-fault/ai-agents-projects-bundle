# tasks.py (add below writer_task)
from crewai import Task
from agents import research_agent, writer_agent, social_media_agent

research_task = Task(
    description="Analyze the major {topic}, identifying key trends and technologies. Provide a detailed report on their potential impact.",
    agent=research_agent,
    expected_output="A detailed report on {topic}, including trends, emerging technologies, and their impact."
)

writer_task = Task(
    description="Create an engaging blog post based on the research findings about {topic}. Tailor the content for a tech-savvy audience.",
    agent=writer_agent,
    expected_output="A 4-paragraph blog post on {topic}, written clearly and engagingly for tech enthusiasts."
)

# 🧩 New Task for Social Media Strategist
social_media_task = Task(
    description="""Generate a concise summary and short-form posts for LinkedIn and X (Twitter) 
    based on the blog content about {topic}. Ensure tone consistency and engaging hooks.""",
    agent=social_media_agent,
    expected_output="""A short LinkedIn post (100-150 words) and a tweet (max 280 chars) 
    summarizing the {topic} in an engaging and insightful way."""
)

TASKS = {
    "Research Task": research_task,
    "Writer Task": writer_task,
    "Social Media Task": social_media_task
}
