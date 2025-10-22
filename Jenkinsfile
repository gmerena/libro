pipeline {
    agent {
        docker {
            image 'python:3.13-slim-bookworm'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    environment {
        VENV = "${WORKSPACE}/.venv"
        PATH = "${WORKSPACE}/.venv/bin:${env.PATH}"
    }

    stages {
        stage('Setup venv & Install dependencies') {
            steps {
                sh '''
                    python -m venv $VENV
                    pip install --upgrade pip
                    pip install uv ruff pytest
                    uv sync
                '''
            }
        }

        stage('Lint') {
            steps {
                sh 'ruff app/ tests/'
            }
        }

        stage('Test') {
            steps {
                sh 'pytest tests/test_api.py'
            }
        }

        stage('Build Docker') {
            steps {
                sh 'docker build -t libro:latest .'
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
    }
}
