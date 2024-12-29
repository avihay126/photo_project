# Flask Microservices Backend

This is a simple Flask application named "backend" that connects to a MySQL database. The application is structured using a microservices architecture and utilizes environment variables for configuration.

## Project Structure

```
backend
├── app
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   └── config.py
├── .env
├── requirements.txt
└── README.md
```

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd backend
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   Create a `.env` file in the root directory with the following content:
   ```
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_NAME=your_database_name
   ```

5. **Run the Application**
   ```bash
   export FLASK_APP=app
   export FLASK_ENV=development
   flask run
   ```

## Usage

Once the application is running, you can access the API endpoints defined in `routes.py`. Use tools like Postman or curl to interact with the API.

## License

This project is licensed under the MIT License.