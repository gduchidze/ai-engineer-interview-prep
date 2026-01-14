# Agentic AI Course

A comprehensive course on building agentic AI systems using modern frameworks like LangChain, LangGraph, and CrewAI. This repository contains practical examples and implementations covering various agentic AI patterns and techniques.

## 📚 Course Structure

The course is organized into three chapters, each focusing on different aspects of agentic AI development:

### Chapter 1: Core Agentic Patterns
- **Prompt Chaining**: Sequential processing of prompts for complex tasks
- **Routing**: Dynamic decision-making and workflow routing
- **Reflexion**: Self-reflection and improvement mechanisms
- **Parallelization**: Concurrent execution of multiple agents
- **Function Calling**: Integration with external tools and APIs
- **Deep Research**: Advanced information gathering and analysis
- **Multi-Agent Collaboration**: Coordination between multiple AI agents

### Chapter 2: Advanced Agent Capabilities
- **Memory Management**: Persistent and contextual memory systems
- **Learning & Adaptation**: Continuous improvement mechanisms
- **MCP (Model Context Protocol)**: Advanced context management
- **Goal Setting & Monitoring**: Task planning and progress tracking
- **Exception Handling**: Robust error management
- **Human-in-the-Loop**: Interactive agent workflows
- **RAG (Retrieval-Augmented Generation)**: Enhanced knowledge retrieval

### Chapter 3: Production & Optimization
- **Agent-to-Agent Communication (A2A)**: Inter-agent messaging protocols
- **Resource-Aware Optimization**: Efficient resource utilization
- **Reasoning Techniques**: Advanced logical inference methods
- **Guardrails & Safety**: Security and safety mechanisms
- **Evaluation & Monitoring**: Performance tracking and metrics
- **Exploration & Discovery**: Autonomous learning strategies

## 🚀 Getting Started

### Prerequisites

- Python 3.12.12 (specified in `.python-version`)
- API key for Google Gemini (for examples using Google Generative AI)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/gduchidze/agentic-ai-course.git
cd agentic-ai-course
```

2. Set up a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory and add your API keys:
```bash
GOOGLE_API_KEY=your_google_api_key_here
```

## 📦 Dependencies

The course uses the following main frameworks and libraries:

- **LangChain** (v1.2.0): Framework for developing LLM applications
- **LangChain Community** (v0.4.1): Community integrations
- **LangGraph** (v1.0.5): Graph-based agent orchestration
- **LangChain Google GenAI** (v4.1.2): Google Generative AI integration
- **CrewAI** (v1.7.2): Multi-agent collaboration framework
- **nest-asyncio** (v1.6.0): Nested asyncio support

## 💻 Usage

Navigate to any chapter directory and run the Python scripts:

```bash
# Example: Run prompt chaining example
python chapters/chapter1/1_prompt_chaining.py

# Example: Run memory management
python chapters/chapter2/1_memory_management.py

# Example: Run A2A communication
python chapters/chapter3/1_a2a.py
```

## 🎯 Learning Path

For best results, follow the chapters in order:

1. Start with **Chapter 1** to understand fundamental agentic patterns
2. Progress to **Chapter 2** to learn advanced capabilities
3. Complete with **Chapter 3** to master production-ready implementations

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new examples or patterns
- Improve documentation
- Add new chapters or topics

## 📝 License

This project is available for educational purposes.

## 🔗 Resources

- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [CrewAI Documentation](https://docs.crewai.com/)
- [Google Gemini API](https://ai.google.dev/)

## ⚠️ Notes

- Make sure to keep your API keys secure and never commit them to version control
- Some examples may require additional setup or API access
- Refer to individual script comments for specific requirements

---

Happy learning! 🎓
