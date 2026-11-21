
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Check Python') {
            steps {
                bat 'python --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Django Check') {
            steps {
                bat 'python manage.py check'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'python manage.py test'
            }
        }
    }
}

