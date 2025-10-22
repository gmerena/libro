pipeline {
    agent { label 'host' }

    stages {
        stage('Setup venv') {
            steps {
                sh '''
                python3 -m venv .venv
                . .venv/bin/activate
                pip install --upgrade pip
                '''
            }
        }

        stage('Lint') {
            steps {
                sh '. .venv/bin/activate && ruff src/ tests/'
            }
        }

        stage('Test') {
            steps {
                sh '. .venv/bin/activate && pytest tests/test_api.py'
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
