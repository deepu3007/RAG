# PDF Query and chat Application 

This project is a Streamlit-based web application that allows users to upload PDF files and ask questions about their content. The application leverages Google Generative AI (Gemini LLM) to process queries and provide relevant responses based on the content of the uploaded PDFs. You can now chat with the pdf.

## Features

- **Upload PDF Files**: Users can upload multiple PDF files to the application.
- **Query PDFs**: Users can ask questions about the content of the uploaded PDFs.
- **Conversational Interface**: The application maintains a conversational chat interface for user interactions.
- **Context Awareness**: The application remembers the context of the conversation for more relevant responses.

## Project Structure

RAG/
├── utils/
│ ├── load_docs.py
│ ├── split_docs.py
│ └── create_and_retrieve.py
├── main.py
├── requirements.txt
└── README.md


- `utils/`: Contains utility scripts for loading and splitting documents, and creating and retrieving data from the vector database.
- `app.py`: The main Streamlit application script.
- `requirements.txt`: Lists the Python dependencies required to run the application.
- `README.md`: Project documentation.

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Python 3.8 or higher
- [Streamlit](https://streamlit.io/)

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/RAG.git
    cd RAG
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    - Create a `.env` file in the root directory of the project.
    - Add your Google API key to the `.env` file:
      ```
      GOOGLE_API_KEY=your-google-api-key
      ```

### Running the Application

1. **Start the Streamlit application**:
    ```bash
    streamlit run main.py
    ```

2. **Open your web browser** and navigate to `http://localhost:8501` to access the application.

## Usage

1. **Upload PDF Files**: Use the file uploader to select and upload multiple PDF files.
2. **Ask Questions**: Enter your questions in the input box and submit. The application will process your query and display the response in the chat interface.
3. **Review Responses**: The chat interface will display the user queries and corresponding responses from the assistant.

## Project Details

### Loading Documents

The `utils/load_docs.py` script handles loading and reading the content of PDF files.

### Splitting Documents

The `utils/split_docs.py` script handles splitting the loaded documents into smaller chunks for better processing.

### Creating and Retrieving Data

The `utils/create_and_retrieve.py` script handles creating a vector database from document chunks and retrieving relevant information based on user queries.

### Streamlit Application

The `app.py` script is the main application file. It sets up the Streamlit interface, handles file uploads, processes user queries, and displays the chat interface.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Streamlit](https://streamlit.io/) for the awesome web app framework.
- [Google Generative AI](https://cloud.google.com/generative-ai) for the language model API.
- All open-source contributors whose libraries were used in this project.

---

Feel free to reach out if you have any questions or need further assistance!

