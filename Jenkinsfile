pipeline {
    agent any

    environment {
        DB_HOST = 'postgres-service'
        DB_PORT = '5432'
        DB_USER = 'postgres'
        DB_PASSWORD = 'admin'
        DB_NAME = 'libro'

        DB_POOL_MIN_SIZE = '1'
        DB_POOL_MAX_SIZE = '10'

        API_PREFIX = '/api'
    }

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
