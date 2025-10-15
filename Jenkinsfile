pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/NairVinayak/ci-cd-assignment-5.git',
                    credentialsId: 'github-creds'
            }
        }

        stage('Setup Python') {
            steps {
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                bat 'pytest --junitxml=report.xml'
            }
            post {
                always {
                    junit 'report.xml'
                }
            }
        }

        stage('Package') {
            steps {
                bat 'python hello.py'
            }
        }

        stage('Deploy to EC2') {
            steps {
                echo 'Deployment step (can be extended later)'
            }
        }
    }

    post {
        failure {
            echo 'Pipeline failed.'
        }
        success {
            echo 'Pipeline completed successfully.'
        }
    }
}
