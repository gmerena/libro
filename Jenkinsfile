pipeline {
    agent any

    stages {
        stage('Setup venv & UV') {
            steps {
                sh '''
                python3 -m venv .venv
                . .venv/bin/activate
                pip install --upgrade pip uv
                uv sync
                '''
            }
        }

        stage('Lint') {
            steps {
                sh '''
                . .venv/bin/activate
                ruff check
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                . .venv/bin/activate
                pytest tests/test_api.py
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
    }
}
