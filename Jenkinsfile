
pipeline {
    agent any

    environment {
        APP_NAME = 'bluegreen-app'
        NAMESPACE = 'bluegreen'
        DEPLOYMENT = 'bg-green'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t ${APP_NAME}:${BUILD_NUMBER} .
                    docker tag ${APP_NAME}:${BUILD_NUMBER} ${APP_NAME}:latest
                '''
            }
        }

        stage('Deploy Green') {
            steps {
                sh '''
                    kubectl apply -f kubernetes/green.yaml -n ${NAMESPACE}
                    kubectl rollout status deployment/${DEPLOYMENT} \
                        -n ${NAMESPACE} --timeout=180s
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                    kubectl get pods -n ${NAMESPACE}
                    kubectl get deployment ${DEPLOYMENT} -n ${NAMESPACE}
                '''
            }
        }
    }
}

pipeline {
    agent any

    environment {
        APP_NAME = 'bluegreen-app'
        NAMESPACE = 'bluegreen'
        DEPLOYMENT = 'bg-green'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t ${APP_NAME}:${BUILD_NUMBER} .
                    docker tag ${APP_NAME}:${BUILD_NUMBER} ${APP_NAME}:latest
                '''
            }
        }

        stage('Deploy Green') {
            steps {
                sh '''
                    kubectl apply -f kubernetes/green.yaml -n ${NAMESPACE}
                    kubectl rollout status deployment/${DEPLOYMENT} \
                        -n ${NAMESPACE} --timeout=180s
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                    kubectl get pods -n ${NAMESPACE}
                    kubectl get deployment ${DEPLOYMENT} -n ${NAMESPACE}
                '''
            }
        }
    }
}
