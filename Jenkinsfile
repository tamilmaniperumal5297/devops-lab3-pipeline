pipeline {
    agent any

    environment {
        AWS_REGION     = 'ap-south-1'
        AWS_ACCOUNT_ID = '351387070227'
        ECR_REPO_NAME  = 'devops-lab3-app'
        CLUSTER_NAME   = 'sre-lab-eks-cluster'
        ECR_URI        = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO_NAME}"
    }

    stages {
        stage('1. Code Validation') {
            steps {
                echo 'Validating Python application syntax...'
                sh 'python3 -m py_compile app.py'
            }
        }

        stage('2. ECR Authentication & Docker Build') {
            steps {
                withCredentials([
                    string(credentialsId: 'aws-access-key-id', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'aws-secret-access-key', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    echo "Authenticating with ECR in ${AWS_REGION}..."
                    sh "aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"

                    echo "Building container image..."
                    sh "docker build -t ${ECR_URI}:${BUILD_NUMBER} -t ${ECR_URI}:latest ."
                }
            }
        }

        stage('3. Push Image to Amazon ECR') {
            steps {
                withCredentials([
                    string(credentialsId: 'aws-access-key-id', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'aws-secret-access-key', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    echo "Pushing images to ECR..."
                    sh "docker push ${ECR_URI}:${BUILD_NUMBER}"
                    sh "docker push ${ECR_URI}:latest"
                }
            }
        }

        stage('4. Deploy Manifests to EKS') {
            steps {
                withCredentials([
                    string(credentialsId: 'aws-access-key-id', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'aws-secret-access-key', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    echo "Updating kubeconfig for EKS cluster ${CLUSTER_NAME}..."
                    sh "aws eks update-kubeconfig --region ${AWS_REGION} --name ${CLUSTER_NAME}"

                    echo 'Applying Kubernetes manifests to EKS cluster...'
                    sh 'kubectl apply -f configmap.yaml'
                    sh 'kubectl apply -f secret.yaml'
                    sh 'kubectl apply -f service.yaml'
                    sh 'kubectl apply -f deployment.yaml'
                }
            }
        }

        stage('5. Verify Rollout') {
            steps {
                withCredentials([
                    string(credentialsId: 'aws-access-key-id', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'aws-secret-access-key', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    echo 'Verifying deployment rollout status on EKS...'
                    sh 'kubectl rollout status deployment/devops-lab3-deployment --timeout=120s'
                }
            }
        }
    }
}