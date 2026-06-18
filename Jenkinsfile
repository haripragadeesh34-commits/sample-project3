pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = 'docker.io'
        DOCKER_REPO = 'haripragadeesh34'
        IMAGE_NAME = 'python-flask-app'
        IMAGE_TAG = "${BUILD_NUMBER}"
        KUBE_NAMESPACE = 'default'
    }

    parameters {
        choice(
            name: 'ENVIRONMENT',
            choices: ['dev', 'staging', 'production'],
            description: 'Deployment environment'
        )
        string(
            name: 'REPLICAS',
            defaultValue: '2',
            description: 'Number of Kubernetes replicas'
        )
    }

    stages {
        stage('Checkout') {
            steps {
                echo '====== Checking out code ======'
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo '====== Building Python application ======'
                sh '''
                    apt-get update
                    apt-get install -y python3-venv python3-pip
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                echo '====== Running tests ======'
                sh '''
                    . venv/bin/activate
                    python -m pytest tests/ -v --junitxml=test-results.xml || true
                '''
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '====== Building Docker image ======'
                sh '''
                    docker build \
                        --tag ${DOCKER_REGISTRY}/${DOCKER_REPO}/${IMAGE_NAME}:${IMAGE_TAG} \
                        --tag ${DOCKER_REGISTRY}/${DOCKER_REPO}/${IMAGE_NAME}:latest \
                        .
                '''
            }
        }

        stage('Push to Registry') {
            steps {
                echo '====== Pushing image to Docker registry ======'
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USR', passwordVariable: 'DOCKER_PSW')]) {
                    sh '''
                        echo $DOCKER_PSW | docker login -u $DOCKER_USR --password-stdin ${DOCKER_REGISTRY}
                        docker push ${DOCKER_REGISTRY}/${DOCKER_REPO}/${IMAGE_NAME}:${IMAGE_TAG}
                        docker push ${DOCKER_REGISTRY}/${DOCKER_REPO}/${IMAGE_NAME}:latest
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            when {
                expression { params.ENVIRONMENT != null }
            }
            steps {
                echo "====== Deploying to ${ENVIRONMENT} environment ======"
                sh '''
                    # Update kubeconfig (adjust based on your setup)
                    # kubectl config use-context <your-context>

                    # Create or update deployment
                    kubectl set image deployment/python-flask-app \
                        python-flask-app=${DOCKER_REGISTRY}/${DOCKER_REPO}/${IMAGE_NAME}:${IMAGE_TAG} \
                        -n ${KUBE_NAMESPACE} || \
                    kubectl apply -f k8s/deployment.yaml \
                        -n ${KUBE_NAMESPACE}

                    # Scale deployment
                    kubectl scale deployment python-flask-app \
                        --replicas=${REPLICAS} \
                        -n ${KUBE_NAMESPACE}

                    # Wait for rollout
                    kubectl rollout status deployment/python-flask-app \
                        -n ${KUBE_NAMESPACE} \
                        --timeout=5m
                '''
            }
        }

        stage('Verify Deployment') {
            when {
                expression { params.ENVIRONMENT != null }
            }
            steps {
                echo '====== Verifying deployment ======'
                sh '''
                    # Check pod status
                    kubectl get pods -l app=python-flask-app -n ${KUBE_NAMESPACE}

                    # Check service endpoints
                    kubectl get svc python-flask-app -n ${KUBE_NAMESPACE}

                    # Get logs from pods
                    kubectl logs -l app=python-flask-app -n ${KUBE_NAMESPACE} --tail=50
                '''
            }
        }

        stage('Cleanup') {
            steps {
                echo '====== Cleaning up ======'
                sh 'docker logout ${DOCKER_REGISTRY} || true'
                cleanWs()
            }
        }
    }

    post {
        success {
            echo '✓ Pipeline completed successfully'
        }
        failure {
            echo '✗ Pipeline failed'
        }
    }
}
