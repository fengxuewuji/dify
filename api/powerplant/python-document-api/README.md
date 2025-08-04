# Python Document API

This project is a Flask-based API for generating Word and PDF documents. It provides endpoints to create documents based on predefined templates and serves them to users.

## Project Structure

```
python-document-api
├── src
│   ├── __init__.py
│   ├── app.py
│   ├── routes
│   │   ├── __init__.py
│   │   ├── word_routes.py
│   │   └── pdf_routes.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── word_service.py
│   │   └── pdf_service.py
│   ├── utils
│   │   ├── __init__.py
│   │   └── helpers.py
│   └── templates
│       ├── word_template.docx
│       └── pdf_template.html
├── tests
│   ├── __init__.py
│   ├── test_word_service.py
│   └── test_pdf_service.py
├── output
│   ├── word_files
│   └── pdf_files
├── requirements.txt
├── config.py
├── run.py
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd python-document-api
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Start the Flask application:
   ```
   python run.py
   ```

2. Access the API endpoints:
   - **Generate Word Document**: `POST /api/word/generate`
   - **Generate PDF Document**: `POST /api/pdf/generate`

## Testing

To run the tests for the Word and PDF services, use:
```
pytest tests/
```

## License

This project is licensed under the MIT License.