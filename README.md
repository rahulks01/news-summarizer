# News Summarizer

## Project Description
News Summarizer is a Django-based web application that generates concise news summaries from longer articles. This project is designed to help a local newspaper create quick, digestible summaries for their daily newsletter. The application features user authentication (login/signup), chat storage for users to refer to past conversations, and a well-designed frontend. It utilizes the Ivis Labs API for summarization instead of OpenAI's API.

## Prerequisites
Ensure you have the following installed on your system:
- Python 3.8+
- pip (Python package manager)
- Virtualenv

## Setup and Running the Project

1. **Clone the Repository**
   ```sh
   git clone https://github.com/rahulks01/news-summarizer.git
   cd news-summarizer
   ```

2. **Initialize a Virtual Environment**
   ```sh
   python -m venv venv
   source venv/bin/activate   # On macOS/Linux
   venv\Scripts\activate      # On Windows
   ```

3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**
   Create a `.env` file in the root directory and add your OpenAI API key in the following format:
   ```sh
   OPENAI_API_KEY=YOUR_API_KEY
   ```

5. **Apply Migrations**
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Run the Development Server**
   ```sh
   python manage.py runserver
   ```

7. **Access the Application**
   Open your browser and go to:
   ```
   http://127.0.0.1:8000/
   ```

## Contributors
- **Rahul Kumar Singh** - 4NI22CS166
- **Raj Shekhar** - 4NI22CS167
- **Raj Singh Rathour** - 4NI22CS168
- **Rakesh M N** - 4NI22CS169
- **Rakshith Gowda** - 4NI22CS170
