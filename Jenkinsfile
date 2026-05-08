pipeline {

    agent any

    options {

        timestamps()

        disableConcurrentBuilds()

        buildDiscarder(
            logRotator(numToKeepStr: '10')
        )

        timeout(
            time: 90,
            unit: 'MINUTES'
        )
    }

    environment {

        PYTHON = "C:\\Users\\pooja.db\\AppData\\Local\\Programs\\Python\\Python311\\python.exe"

        PYTHONUNBUFFERED = '1'

        PIP_DISABLE_PIP_VERSION_CHECK = '1'
    }

    stages {

        // ======================================================
        // CLEAN WORKSPACE
        // ======================================================

        stage('Clean Workspace') {

            steps {

                cleanWs()
            }
        }

        // ======================================================
        // CHECKOUT CODE
        // ======================================================

        stage('Checkout Code') {

            steps {

                checkout scm
            }
        }

        // ======================================================
        // VERIFY PYTHON
        // ======================================================

        stage('Verify Python') {

            steps {

                bat '''
                echo Python Path:
                echo %PYTHON%

                "%PYTHON%" --version

                where python
                '''
            }
        }

        // ======================================================
        // CREATE VENV
        // ======================================================

        stage('Create Virtual Environment') {

            steps {

                bat '''
                "%PYTHON%" -m venv venv
                '''
            }
        }

        // ======================================================
        // INSTALL DEPENDENCIES
        // ======================================================

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

        // ======================================================
        // VERIFY ENVIRONMENT
        // ======================================================

        stage('Verify Environment') {

            steps {

                bat '''
                call venv\\Scripts\\activate

                python --version

                pip --version

                where python

                pip list
                '''
            }
        }

        // ======================================================
        // CREATE REPORT DIRECTORIES
        // ======================================================

        stage('Create Report Folders') {

            steps {

                bat '''
                if not exist reports mkdir reports

                if not exist screenshots mkdir screenshots

                if not exist logs mkdir logs

                if not exist downloads mkdir downloads
                '''
            }
        }

        // ======================================================
        // RUN PYTEST
        // ======================================================

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

    // ==========================================================
    // POST ACTIONS
    // ==========================================================

    post {

        always {

            archiveArtifacts(
                artifacts: 'reports/**/*.*',
                allowEmptyArchive: true
            )

            archiveArtifacts(
                artifacts: 'screenshots/**/*.*',
                allowEmptyArchive: true
            )

            archiveArtifacts(
                artifacts: 'logs/**/*.*',
                allowEmptyArchive: true
            )

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