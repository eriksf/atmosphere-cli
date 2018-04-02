#!groovy

def jobs = ["Python2.7", "Python3.6"]

def parallelStagesMap = jobs.collectEntries {
    ["${it}" : generateStage(it)]
}

def generateStage(job) {
    return {
        stage("stage: ${job} build") {
            sh 'mkdir -p ' + test_output_dir + "/${job}"
            withPythonEnv("${job}") {
                pysh 'python --version'
                pysh 'pip install pipenv'
                pysh 'pipenv install --dev'
                pysh "pipenv run pytest --verbose --cov atmosphere --cov-report xml:${test_output_dir}/${job}/coverage.xml --junit-xml ${test_output_dir}/${job}/pytest.xml"
                pysh "pipenv run behave --tags=-@xfail --format=progress3 --junit --junit-directory ${test_output_dir}/${job}/behave_reports features"
                junit "${test_output_dir}/${job}/**/pytest.xml, ${test_output_dir}/${job}/behave_reports/*.xml"
            }
        }
    }
}

pipeline {
    agent any

    environment {
        test_output_dir = "test_reports"
    }

    stages {

        stage('Checkout code') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: '*/master']], userRemoteConfigs: [[url: 'https://github.com/eriksf/atmosphere-cli.git']]])
            }
        }

        stage('Prepare test output') {
            steps {
                echo "In directory " + pwd()
                sh 'mkdir -p ' + test_output_dir
            }
        }

        stage('parallel stage') {
            steps {
                script {
                    parallel parallelStagesMap
                }
            }
        }
    }

    post {
        always {
            echo "Always run this step at the end!"
            // cleanWs()
        }
    }
}
