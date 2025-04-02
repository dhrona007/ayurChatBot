## AyurBot - Prakriti Determination Chatbot

AyurBot is a command-line interface (CLI) chatbot designed to determine an individual's **Prakriti** (constitution) based on Ayurvedic principles. It analyzes user responses to a series of questions and identifies the dominant dosha: **Vata**, **Pitta**, or **Kapha**.

## Features

- **Prakriti Assessment**: Answers 6 questions to determine your Ayurvedic constitution.
- **Simple CLI Interface**: Easy-to-use text-based interaction.
- **Dynamic Scoring**: Logic-based scoring system to calculate dosha dominance.
- **Environment Variable Support**: Secure API key management using `.env`.

## Prerequisites

- Python 3.7 or higher
- A [Together API key](https://www.together.ai/) (required for initialization, though AI integration is a planned feature)
- Basic understanding of terminal/command-line usage

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/ayurbot.git
   cd ayurbot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Together API key**:
   - Create a `.env` file in the project root.
   - Add your API key:
     ```env
     TOGETHER_API_KEY=your_api_key_here
     ```

## Usage

1. **Run the application**:
   ```bash
   python app.py
   ```

2. **Choose an option**:
   - Enter `1` to start the Prakriti assessment.
   - Enter `2` to exit.

3. **Answer the questions**:
   - Respond to the bot’s prompts with keywords like "skinny", "warm", "yes", etc.
   - Example:
     ```
     Bot: How would you describe your body frame? (Skinny, medium, or perfect)
     You: skinny
     ```

4. **Get your result**:
   - After answering all questions, AyurBot will display your dominant dosha (e.g., "VATA").

## Project Structure

| File               | Description                                                                 |
|--------------------|-----------------------------------------------------------------------------|
| `app.py`           | Main application logic, CLI interface, and scoring system.                 |
| `brain.py`         | Contains questions, answer mappings, and predefined bot responses.         |
| `requirements.txt` | Lists dependencies (e.g., `together`, `python-dotenv`).                    |
| `.env`             | Stores environment variables like the Together API key (create manually).   |

## Future Enhancements

- Integrate Together API for AI-generated responses.
- Add a web interface using Flask or Streamlit.
- Expand question set for more accurate Prakriti analysis.
- Include personalized Ayurvedic recommendations based on results.

## Contributing

Contributions are welcome!  
1. Fork the repository.  
2. Create a feature branch: `git checkout -b feature/new-feature`.  
3. Commit changes: `git commit -m "Add new feature"`.  
4. Push to the branch: `git push origin feature/new-feature`.  
5. Submit a pull request.

## License

This project is open-source under the [MIT License](LICENSE).

## Acknowledgements

- Ayurvedic principles for Prakriti classification.
- [Together](https://www.together.ai/) for AI infrastructure (future integration).
```
