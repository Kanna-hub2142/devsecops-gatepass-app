pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS_ID = 'DOCKER_HUB_CREDENTIALS' 
        DOCKER_IMAGE_NAME = 'devsecops-gatepass' 
        CONTAINER_NAME = 'devsecops-gatepass-container'
        CONTAINER_PORT = '8000'
        HOST_PORT = '8000'
    }

    stages {
        
        stage ("clean workspace") {
            steps {
                cleanWs()
            }
        }
        
        stage('github checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/Kanna-hub2142/devsecops-gatepass-app.git'
            }
        }

        // stage('OWASP Dependency Check') {
        //     steps {
        //         dependencyCheck additionalArguments: '--format HTML', odcInstallation: 'owasp-dp-check-12.1.19'
        //     }
        // }

        // stage('trivy scan') {
        //     steps {
        //         sh '''trivy fs . \\
        //             --severity HIGH,CRITICAL \\
        //             --format template \\
        //             --template "@contrib/html.tpl" \\
        //             --output trivy-fs-report.html
        //             '''
        //     }
        // }


        stage('Sonar Analysis') {
            steps {
                withCredentials([string(credentialsId: 'SONAR_TOKEN', variable: 'SONAR_TOKEN')]) {
                sh '''
                    set +x
                    
                    python3 -m venv env
                    source ./env/bin/activate

                    pip install pysonar

                    # Run pysonar with secure token
                    pysonar \\
                    -Dsonar.token=$SONAR_TOKEN \\
                    -Dsonar.projectKey=kanna-hub2142_devsecops-gatepass-app \\
                    -Dsonar.organization=kanna-hub2142 \\
                    # Optionally specify host if needed:
                    # -Dsonar.host.url=https://your-sonar-host
                '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    
                    sh "docker build -t ${DOCKER_IMAGE_NAME}:latest ."
                }
            }
        }

        stage('trivy docker image scan') {
            steps {
                sh "trivy image --format table -o trivy_report.html --severity HIGH,CRITICAL ${DOCKER_IMAGE_NAME}:latest"
            }
        }
        
        stage('Push Docker Image') {
            steps {
                script {
                    
                    withCredentials([
                        usernamePassword(credentialsId: "${DOCKER_CREDENTIALS_ID}", 
                        passwordVariable: 'DOCKER_PASSWORD', 
                        usernameVariable: 'DOCKER_USERNAME')
                    ]) {
                        sh "echo \$DOCKER_PASSWORD | docker login -u \$DOCKER_USERNAME --password-stdin"
                    }

                    
                    sh "docker push ${DOCKER_IMAGE_NAME}:latest"
                }
            }
        }

        stage("Stopping Old Container") {
            steps {
                script {
                  sh "docker stop ${CONTAINER_NAME} || true"
                }
            }
        }

        stage("Removing Old Container") {
            steps {
                script {
                  sh "docker rm ${CONTAINER_NAME} || true"
                }
            }
        }

        // stage("Running latest image") {
        //     steps {
        //         script {
        //           sh """
        //             docker run -d \
        //               --name ${CONTAINER_NAME} \
        //               -p ${HOST_PORT}:${CONTAINER_PORT} \
        //               ${DOCKER_IMAGE_NAME}:latest
        //           """
        //         }
        //     }
        // }
        
    }
}
