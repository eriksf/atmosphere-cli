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
                sh 'python --version'
                sh 'pip install pipenv'
                sh 'pipenv install --dev'
                sh "pytest --verbose --cov atmosphere --cov-report xml:${test_output_dir}/${job}/coverage.xml --junit-xml ${test_output_dir}/${job}/pytest.xml"
                // pysh "behave --no-capture --no-capture-stderr --tags=-@xfail --format=progress3 --junit --junit-directory ${test_output_dir}/${job}/behave_reports --logging-level DEBUG features"
                junit "${test_output_dir}/${job}/**/pytest.xml, ${test_output_dir}/${job}/behave_reports/*.xml"
                cobertura autoUpdateHealth: false, autoUpdateStability: false, coberturaReportFile: "${test_output_dir}/${job}/**/coverage.xml", conditionalCoverageTargets: '70, 0, 0', failUnhealthy: false, failUnstable: false, lineCoverageTargets: '80, 0, 0', maxNumberOfBuilds: 0, methodCoverageTargets: '80, 0, 0', onlyStable: false, sourceEncoding: 'ASCII', zoomCoverageChart: false
            }
        }
    }
}

pipeline {
    agent any

    options {
        timestamps()
    }

    environment {
        test_output_dir = "test_reports"
    }

    stages {

        stage('Checkout code') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: '**']], userRemoteConfigs: [[url: 'https://github.com/eriksf/atmosphere-cli.git']]])
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
            cleanWs()
        }
        failure {
            emailext attachLog: true, body: '''${SCRIPT, template="groovy-html.template"}''', mimeType: 'text/html', subject: "[JENKINS] ${currentBuild.fullDisplayName} - ${currentBuild.result}", to: 'eferlanti@tacc.utexas.edu'
        }
    }
}
