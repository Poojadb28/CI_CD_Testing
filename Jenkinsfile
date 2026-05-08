// pipeline {
//     agent any

//     environment {
//         PYTHON = "C:\\Users\\pooja.db\\AppData\\Local\\Programs\\Python\\Python311\\python.exe"
//     }

//     options {
//         timestamps()
//         disableConcurrentBuilds()
//     }

//     stages {

//         stage('Checkout Code') {
//             steps {
//                 checkout scm
//             }
//         }

//         stage('Install Dependencies') {
//             steps {
//                 bat "%PYTHON% -m pip install --upgrade pip"
//                 bat "%PYTHON% -m pip install -r requirements.txt"
//                 bat "%PYTHON% -m pip install pytest-html pytest-xdist pytest-rerunfailures"
//             }
//         }

//         stage('Prepare Folders') {
//             steps {
//                 bat "if not exist reports mkdir reports"
//                 bat "if not exist screenshots mkdir screenshots"
//                 bat "if not exist downloads mkdir downloads"
//             }
//         }

//         stage('Run Tests') {
//     steps {
//         bat """
// set PYTHONIOENCODING=utf-8
// %PYTHON% -m pytest tests/ ^
// -v ^
// --headless ^
// --html=reports/report.html ^
// --self-contained-html ^
// --capture=sys ^
// --reruns 1
// """
//     }
// }
//     }

//     post {

//         always {
//             archiveArtifacts artifacts: 'screenshots/*.png', allowEmptyArchive: true

//             publishHTML(target: [
//                 reportDir: 'reports',
//                 reportFiles: 'report.html',
//                 reportName: 'Automation Test Report',
//                 keepAll: true,
//                 alwaysLinkToLastBuild: true,
//                 allowMissing: true
//             ])
//         }

//         success {
//             echo "Build SUCCESS"
//         }

//         failure {
//             echo "Build FAILED - Check HTML Report"
//         }
//     }
// }

pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 90, unit: 'MINUTES')
    }

    environment {
        PYTHONUNBUFFERED = '1'
        PIP_DISABLE_PIP_VERSION_CHECK = '1'
    }

    stages {

        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Create Virtual Environment') {
            steps {
                bat '''
                python -m venv venv
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                call venv\\Scripts\\activate

                python -m pip install --upgrade pip

                pip install -r requirements.txt

                pip install pytest
                pip install pytest-html
                pip install pytest-xdist
                pip install pytest-rerunfailures
                pip install pytest-timeout
                pip install webdriver-manager
                '''
            }
        }

        stage('Verify Environment') {
            steps {
                bat '''
                call venv\\Scripts\\activate

                python --version
                pip --version

                where python
                '''
            }
        }

        stage('Create Report Folders') {
            steps {
                bat '''
                if not exist reports mkdir reports
                if not exist screenshots mkdir screenshots
                if not exist logs mkdir logs
                '''
            }
        }

        stage('Run PyTest Suite') {
            steps {
                bat '''
                call venv\\Scripts\\activate

                pytest ^
                -v ^
                --tb=short ^
                --maxfail=5 ^
                --reruns 1 ^
                --reruns-delay 3 ^
                --timeout=300 ^
                --html=reports/report.html ^
                --self-contained-html ^
                tests/
                '''
            }
        }
    }

    post {

        always {

            archiveArtifacts artifacts: 'reports/**/*.*', allowEmptyArchive: true
            archiveArtifacts artifacts: 'screenshots/**/*.*', allowEmptyArchive: true
            archiveArtifacts artifacts: 'logs/**/*.*', allowEmptyArchive: true

            publishHTML(target: [
                reportDir: 'reports',
                reportFiles: 'report.html',
                reportName: 'PyTest Automation Report',
                keepAll: true,
                alwaysLinkToLastBuild: true,
                allowMissing: true
            ])
        }

        success {
            echo 'Automation Suite Executed Successfully'
        }

        unstable {
            echo 'Some Tests Failed / Flaky Tests Detected'
        }

        failure {
            echo 'Build Failed'
        }

        cleanup {
            cleanWs(deleteDirs: true)
        }
    }
}
