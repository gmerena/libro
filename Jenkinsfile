pipeline {
    agent any

    environment {
        VENV = "${WORKSPACE}/.venv"
        PATH = "${WORKSPACE}/.venv/bin:${env.PATH}"
    }

    stages {
        stage('Setup venv') {
            steps {
                sh '''
                    python3 -m venv $VENV
                    source $VENV/bin/activate
                '''
            }
        }

        stage('Lint') {
            steps {
                sh '''
                    source $VENV/bin/activate
                    ruff src/ tests/
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    source $VENV/bin/activate
                    pytest tests/test_api.py
                '''
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
