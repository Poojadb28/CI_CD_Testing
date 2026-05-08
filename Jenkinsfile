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
                echo =====================================
                echo VERIFYING PYTHON
                echo =====================================

                echo Python Path:
                echo %PYTHON%

                "%PYTHON%" --version
                '''
            }
        }

        // ======================================================
        // CREATE VIRTUAL ENVIRONMENT
        // ======================================================

        stage('Create Virtual Environment') {

            steps {

                bat '''
                echo =====================================
                echo CREATING VIRTUAL ENVIRONMENT
                echo =====================================

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
                echo =====================================
                echo INSTALLING DEPENDENCIES
                echo =====================================

                call venv\\Scripts\\activate

                python -m pip install --upgrade pip

                pip install -r requirements.txt
                '''
            }
        }

        // ======================================================
        // VERIFY ENVIRONMENT
        // ======================================================

        stage('Verify Environment') {

            steps {

                bat '''
                echo =====================================
                echo VERIFYING ENVIRONMENT
                echo =====================================

                call venv\\Scripts\\activate

                python --version

                pip --version

                pip list
                '''
            }
        }

        // ======================================================
        // CREATE REPORT FOLDERS
        // ======================================================

        stage('Create Report Folders') {

            steps {

                bat '''
                echo =====================================
                echo CREATING REPORT FOLDERS
                echo =====================================

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
                echo =====================================
                echo RUNNING PYTEST SUITE
                echo =====================================

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

            cleanWs(
                deleteDirs: true,
                disableDeferredWipeout: true
            )
        }
    }
}