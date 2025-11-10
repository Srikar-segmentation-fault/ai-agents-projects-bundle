# agents.py
import os
from dotenv import load_dotenv
from crewai import Agent, LLM
from crewai_tools import SerperDevTool

# Load environment variables from .env file
load_dotenv()

# Initialize SerperDevTool with API Key
search_tool = SerperDevTool()

# Initialize LLM (IBM watsonx or other model)
llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    temperature=0.5,
    max_completion_tokens=1200,
    top_p=0.9,
    stop=["Task Complete", "END_OF_REPORT"],
    stream=False,
    base_url="https://api.groq.com/openai/v1"
)

# 🧠 Research Agent Definition
research_agent = Agent(
    role='Senior Research Analyst',
    goal='Uncover cutting-edge information and insights on any subject with comprehensive analysis',
    backstory="""You are an expert researcher with extensive experience in gathering, analyzing, 
    and synthesizing information across multiple domains. You excel at identifying key trends, 
    finding reliable data sources, and producing valuable reports.""",
    verbose=True,
    allow_delegation=False,
    llm=llm,
    tools=[search_tool]
)

# ✍️ Writer Agent Definition
writer_agent = Agent(
    role='Tech Content Strategist',
    goal='Craft well-structured and engaging content based on research findings',
    backstory="""You are a skilled content strategist known for translating 
    complex topics into clear and compelling narratives. You write engaging blog 
    posts for tech audiences, balancing depth and readability.""",
    verbose=True,
    llm=llm,
    allow_delegation=True
)


# 💬 Social Media Strategist Agent
social_media_agent = Agent(
    role='Social Media Strategist',
    goal='Create engaging short-form content and social posts that highlight the main insights from research and blog articles.',
    backstory="""You are an expert in crafting platform-specific social media content for tech audiences. 
    You can take a long article or research and turn it into catchy, concise, and thought-provoking posts 
    suitable for platforms like LinkedIn, X (Twitter), and Threads.""",
    verbose=True,
    llm=llm,
    allow_delegation=False
)

# Store agents for import
AGENTS = {
    "Research Agent": research_agent,
    "Writer Agent": writer_agent,
    "Social Media Agent": social_media_agent
}
