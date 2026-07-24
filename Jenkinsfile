pipeline {
    agent any // Or specify your designated Docker build node: agent { label 'docker-node' }
    
    // triggers {
    //     // Triggers the pipeline when the configured webhook is received
    //     githubPush() 
    }

    environment {
        // Define your variables here for easy updates
        DOCKER_REGISTRY = '005696749434.dkr.ecr.us-east-1.amazonaws.com/dev/cicd' // Change if using AWS ECR, GCP Artifact Registry, etc.
        IMAGE_NAME      = '005696749434.dkr.ecr.us-east-1.amazonaws.com/dev/cicd/pca-quiz'
        IMAGE_TAG       = "${env.BUILD_NUMBER}" // Uses Jenkins build number for unique tagging
        CONTAINER_NAME  = 'my-running-app'
        PORT_MAPPING    = '8080:8080'
    }

    stages {
        stage('Checkout SCM') {
            steps {
                // Jenkins automatically uses the SCM configured in the pipeline job UI,
              sh 'echo passed'
              git branch: 'main', url: 'https://github.com/sheik-13/pca-quiz-app.git'
            }
        }

        stage('Build Code') {
            steps {
                // Swap this with your actual build command (e.g., npm install, mvn package, pip install)
                echo "Running code build steps..."
                sh 'make build || echo "Replace with your build command"'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image ${IMAGE_NAME}:${IMAGE_TAG}..."
                sh 'docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest .'
            }
        }

        stage('Push to Registry') {
            steps {
                // Ensure you have added a 'Username with password' credential in Jenkins named 'docker-hub-creds'
                withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER')]) {
                    sh 'echo "$DOCKER_PASS" | docker login ${DOCKER_REGISTRY} -u "$DOCKER_USER" --password-stdin'
                    sh 'docker push ${IMAGE_NAME}:${IMAGE_TAG}'
                    sh 'docker push ${IMAGE_NAME}:latest'
                }
            }
        }

        stage('Deploy to Container') {
            steps {
                // This stops the old container, removes it, and runs the new image.
                // Note: This executes on the Jenkins agent. For remote servers, you'd use SSH.
                script {
                    echo "Deploying the new container..."
                    sh """
                        docker stop ${CONTAINER_NAME} || true
                        docker rm ${CONTAINER_NAME} || true
                        docker run -d --name ${CONTAINER_NAME} -p ${PORT_MAPPING} \
                        --restart unless-stopped \
                        ${IMAGE_NAME}:${IMAGE_TAG}
                    """
                }
            }
        }
    }

    post {
        always {
            // Security and workspace hygiene
            sh 'docker logout ${DOCKER_REGISTRY}'
            cleanWs()
        }
        success {
            echo "Pipeline completed successfully! Container is running."
        }
        failure {
            echo "Pipeline failed. Check the logs for details."
        }
    }
}