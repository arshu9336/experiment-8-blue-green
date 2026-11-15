
pipeline {
    agent any

    environment {
        APP_NAME = 'bluegreen-app'
        NAMESPACE = 'bluegreen'
        SERVICE = 'bg-production'
        ARCHIVE = '/tmp/bluegreen-app.tar'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Detect Active Environment') {
            steps {
                script {
                    env.ORIGINAL_SLOT = sh(
                        script: "kubectl get service ${SERVICE} -n ${NAMESPACE} -o jsonpath='{.spec.selector.slot}'",
                        returnStdout: true
                    ).trim()

                    if (env.ORIGINAL_SLOT == 'blue') {
                        env.TARGET_SLOT = 'green'
                    } else if (env.ORIGINAL_SLOT == 'green') {
                        env.TARGET_SLOT = 'blue'
                    } else {
                        error("Unknown active slot: ${env.ORIGINAL_SLOT}")
                    }

                    echo "Currently active: ${env.ORIGINAL_SLOT}"
                    echo "Deploying to inactive slot: ${env.TARGET_SLOT}"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t ${APP_NAME}:${BUILD_NUMBER} .
                    docker save ${APP_NAME}:${BUILD_NUMBER} -o ${ARCHIVE}
                '''
            }
        }

        stage('Import Image into K3s') {
            steps {
                sh '''
                    sudo -n /usr/bin/ctr \
                      --address /run/k3s/containerd/containerd.sock \
                      -n k8s.io images import ${ARCHIVE}
                '''
            }
        }

        stage('Deploy Inactive Environment') {
            steps {
                sh '''
                    kubectl apply -f kubernetes/${TARGET_SLOT}.yaml -n ${NAMESPACE}

                    kubectl set image deployment/bg-${TARGET_SLOT} \
                      bluegreen-app=${APP_NAME}:${BUILD_NUMBER} \
                      -n ${NAMESPACE}

                    kubectl set env deployment/bg-${TARGET_SLOT} \
                      COLOR=$(echo ${TARGET_SLOT} | tr '[:lower:]' '[:upper:]') \
                      APP_VERSION=1.0 \
                      BUILD_NUMBER=${BUILD_NUMBER} \
                      -n ${NAMESPACE}

                    kubectl rollout status deployment/bg-${TARGET_SLOT} \
                      -n ${NAMESPACE} --timeout=180s
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                    kubectl wait --for=condition=Ready pod \
                      -l app=bluegreen,slot=${TARGET_SLOT} \
                      -n ${NAMESPACE} --timeout=180s

                    kubectl get pods -n ${NAMESPACE}
                    kubectl get deployment bg-${TARGET_SLOT} -n ${NAMESPACE}
                '''
            }
        }

        stage('Switch Production Traffic') {
            steps {
                sh '''
                    kubectl patch service ${SERVICE} -n ${NAMESPACE} \
                      -p '{"spec":{"selector":{"app":"bluegreen","slot":"'${TARGET_SLOT}'"}}}'

                    echo "Production traffic switched to ${TARGET_SLOT}"
                    kubectl get service ${SERVICE} -n ${NAMESPACE} -o yaml
                '''
            }
        }
    }

    post {
        failure {
            script {
                if (env.ORIGINAL_SLOT?.trim()) {
                    echo "Restoring production traffic to ${env.ORIGINAL_SLOT}"
                    sh """
                        kubectl patch service ${SERVICE} -n ${NAMESPACE} \
                          -p '{"spec":{"selector":{"app":"bluegreen","slot":"${env.ORIGINAL_SLOT}"}}}'
                    """
                }
            }
        }
        success {
            echo 'Blue-Green deployment completed successfully!'
        }
    }
}

