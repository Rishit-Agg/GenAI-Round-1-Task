#  Persona ChatBot (Groq + LangChain + Streamlit)

This is a chatbot with multiple personas:
- RoastBot
- ShakespeareBot
- EmojiBot

##  How to Run
1. Clone the repo:
   
   git clone https://github.com/Rishit-Agg/chatbot-groq-langchain.git
   cd chatbot-groq-langchain


2. Create & activate virtual environment:

    python -m venv venv
    .\venv\Scripts\activate      # Windows
   
    source venv/bin/activate     # Mac/Linux

4. Install dependencies:

    pip install -r requirements.txt

5. Add your GROQ_API_KEY to a .env file:

    GROQ_API_KEY=your_api_key_here

6. Run the chatbot:

    streamlit run app.py


✨ Features

1. Multiple chatbot personas

2. Memory of conversation

3. Built with Groq + LangChain + Streamlit
