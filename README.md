# THE TEENAGE YEARS

## Project Overview

"The Teenage Years" is a modern web application designed to explore and visualize the experiences of teenagers in 2026. The application aims to provide insights into the challenges, stories, and voices of teenagers through various interactive features.

## Features

- **Homepage**: An engaging landing page that describes the challenges of teenage life.
- **Stories**: A section dedicated to sharing personal stories from teenagers.
- **Polls**: Interactive polls to gather opinions and experiences from users.
- **Quizzes**: Fun quizzes to engage users and provide insights into their teenage experiences.
- **About Page**: Information about the project and its significance in listening to the voices of youth.

## Project Structure

```
the-teenage-years
├── app
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   ├── templates
│   │   ├── base.html
│   │   ├── index.html
│   │   └── about.html
│   ├── static
│   │   ├── css
│   │   │   └── styles.css
│   │   ├── js
│   │   │   └── scripts.js
│   │   └── assets
│   └── forms.py
├── instance
│   └── config.py
├── tests
│   ├── __init__.py
│   └── test_routes.py
├── venv
├── requirements.txt
├── config.py
├── run.py
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/the-teenage-years.git
   ```
2. Navigate to the project directory:
   ```
   cd new-repo-teenies-main
   ```
3. Create a virtual environment:
   ```
   python -m venv venv
   ```
4. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```
5. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

To run the application, execute the following command:

```
python run.py
```

The application will be accessible at `http://127.0.0.1:5000`.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
