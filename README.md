# Chatbot with OpenAI GPT-3 for Chatbot Course
This project is a Telegram chatbot that utilizes the OpenAI GPT-3 model for generating responses. It is developed as part of a course on using GPT in chatbots.

## Requirements
To run the chatbot, you need the following dependencies:

Python 3.7 or higher
- aiogram library  (`pip install aiogram`)
- pandas library (`pip install pandas`)
- openai library (`pip install openai`)
## Getting Started
1. Clone the repository or download the source code files.

2. Install the required dependencies mentioned in the requirements section.

3. Open the main.py file and replace YOUR_TOKEN with your Telegram bot token and OpenAI API key.

4. Make sure you have a CSV file named users.csv in the same directory. This file is used to store user data.

5. Run the main.py file to start the chatbot:

```
python main.py
```
## Features
### Start Command
- The `/start` command is used to start the conversation with the chatbot.
- If the user is registered, it sends a welcome back message.
- If the user is not registered, it registers the user and sends a welcome message.
### Tokens Command
- The /tokens command allows registered users to request token replenishment.
- Users can request tokens if the last request was made at least 3 minutes ago.
- Upon successful token replenishment, it informs the user.
### Respond Function
- The respond function handles user messages and generates responses using the OpenAI Chat API.
- It checks if the user is registered and has enough tokens to generate a response.
- If the user is not registered, it informs the user to register first.
- If the user has run out of tokens, it informs the user to replenish their tokens.
- It manages the conversation context by storing and updating user messages.
- It sends the user's message and the context to the OpenAI Chat API for generating a response.
- The response is sent back to the user, and the context is updated with the assistant's reply.
### Customization
You can customize the behavior of the chatbot by modifying the code in `main.py`:

- Change the welcome messages in the `start_command` function.
- Modify the token replenishment logic in the `tokens_command` function.
- Customize the system instruction and context management in the `respond` function.
## Limitations
- The chatbot relies on the OpenAI GPT-3 model for generating responses. Any limitations or biases associated with the model apply to the chatbot.
- The chatbot requires a stable internet connection to communicate with the Telegram Bot API and the OpenAI API.
## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgments
This project was developed as part of a course on using OpenAI GPT in chatbots. Special thanks to the course instructors for their guidance and support.

Happy chatting with your GPT-powered chatbot!