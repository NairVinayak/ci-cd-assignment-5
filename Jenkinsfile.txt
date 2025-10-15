pipeline {
  agent any
  environment {
    DEPLOY_USER = "ubuntu"                          // remote EC2 user
    DEPLOY_HOST = "3.110.178.47"                   // replace with your EC2 public IP
    DEPLOY_PATH = "/home/ubuntu/deploy/sample-app" // remote deploy path
    SSH_CRED_ID = "ec2-ssh-key"                    // credential id you will create in Jenkins
  }
  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Setup Python') {
      steps {
        sh 'python3 --version || true'
        sh 'python3 -m venv .venv || python -m venv .venv'
        sh '. .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt'
      }
    }

    stage('Test') {
      steps {
        sh '. .venv/bin/activate && pytest -q'
      }
    }

    stage('Package') {
      steps {
        // optional: build docker image here, or create a tarball to copy
        sh 'tar -czf sample-app.tar.gz hello.py requirements.txt'
      }
    }

    stage('Deploy to EC2') {
      steps {
        // copy artifact and extract on remote host via SSH
        sshagent (credentials: [env.SSH_CRED_ID]) {
          sh """
            scp -o StrictHostKeyChecking=no sample-app.tar.gz ${DEPLOY_USER}@${DEPLOY_HOST}:${DEPLOY_PATH}/
            ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_HOST} 'mkdir -p ${DEPLOY_PATH} && tar -xzf ${DEPLOY_PATH}/sample-app.tar.gz -C ${DEPLOY_PATH} && cd ${DEPLOY_PATH} && python3 -m venv .venv || true && . .venv/bin/activate && pip install -r requirements.txt && pkill -f hello.py || true && nohup python3 hello.py > app.log 2>&1 &'
          """
        }
      }
    }
  }

  post {
    always {
      junit '**/test-*.xml'  // if you produce junit xmls
      archiveArtifacts artifacts: 'sample-app.tar.gz', fingerprint: true
    }
    success {
      echo 'Pipeline succeeded!'
    }
    failure {
      echo 'Pipeline failed.'
    }
  }
}
