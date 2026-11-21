
# Django Todo Application with CI/CD Pipeline

## Project Overview
This project is a Django-based Todo Application integrated with a CI/CD pipeline using GitHub and Jenkins.

It demonstrates how DevOps practices can automate code checkout, dependency installation, Django system checks, and automated testing.

## Technologies Used
- Python
- Django
- HTML and CSS
- Git and GitHub
- Jenkins
- PowerShell

## Application Features
- Add Tasks
- Complete Tasks
- Delete Tasks
- Task Analytics Dashboard
- Monthly Productivity Report
- Task Completion Percentage

## DevOps Workflow

1. Develop the application using Django.
2. Push source code to GitHub.
3. Jenkins fetches the latest code from GitHub.
4. Install project dependencies.
5. Run Django system checks.
6. Execute automated test cases.
7. Display the build result.

## Jenkins Pipeline Stages
- Checkout
- Check Python
- Install Dependencies
- Django Check
- Run Tests

## Automated Testing
The project includes automated tests for:
- Home page loading
- Task creation
- Task completion
- Task deletion
- Task analytics

## How to Run Locally

Clone the repository:

```bash
git clone https://github.com/GhadgeGayatri06/Django-Todo-CI-CD.git
```

Open the project folder:

```bash
cd Django-Todo-CI-CD
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Set Django Secret Key in PowerShell:

```powershell
$env:DJANGO_SECRET_KEY = "your-local-secret-key"
```

Run migrations:

```bash
python manage.py migrate
```

Start the server:

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000/

## Run Automated Tests

```bash
python manage.py test
```

## Author
Gayatri Ghadge
