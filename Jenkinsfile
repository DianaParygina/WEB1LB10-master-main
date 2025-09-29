pipeline {
    agent any

    environment {
        CMD = 'C:\\Windows\\System32\\cmd.exe'
        PM2_CMD = 'C:\\Users\\ashflaare\\AppData\\Roaming\\npm\\pm2.cmd'
        PYTHON_EXE = 'C:\\Program Files\\Python313\\python.exe'
        TARGET_DIR = 'C:\\Users\\Diana\\OneDrive\\Desktop\\DevOps\\WEB1LB10-master-main'
    }

    triggers { 
        githubPush() 
    }

    stages {
        stage('Start Backend Server') {
            steps {
                bat """
                    cd "${TARGET_DIR}"

                    call "${PM2_CMD}" delete django || echo No existing Django process

                    call "${PM2_CMD}" start "${PYTHON_EXE}" --name django -- manage.py runserver 127.0.0.1:8000
                """
            }
        }

        stage('Start Frontend Server') {
            steps {
                bat """
                    cd "${TARGET_DIR}\\client"

                    call "${PM2_CMD}" delete vue || echo No existing Vue process

                    call "${PM2_CMD}" start "${CMD}" --name vue -- /c "cd ${TARGET_DIR}\\client && npm run dev"

                    echo Frontend started in background via PM2
                """
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    try {
                        bat """
                            cd "${TARGET_DIR}"
                            "${PYTHON_EXE}" application\\integrationtests.py
                        """
                        echo "Tests passed! Keeping servers running."
                    } catch (err) {
                        echo "Tests failed! Stopping servers..."

                        bat """
                            "${PM2_CMD}" delete django || echo No Django process to delete
                            "${PM2_CMD}" delete vue || echo No Vue process to delete
                        """
                        error("Integration tests failed. Servers stopped.")
                    }
                }
            }
        }

        stage('Merge feature into main and sync feature') {
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                withCredentials([
                    usernamePassword(credentialsId: 'github-creds', usernameVariable: 'GIT_USER', passwordVariable: 'GIT_TOKEN'),
                    string(credentialsId: 'github-email', variable: 'GIT_EMAIL')
                ]) {
                    bat """
                        cd "${TARGET_DIR}"
                        
                        :: Настраиваем Git
                        git config user.name "%GIT_USER%"
                        git config user.email "%GIT_EMAIL%"

                        :: 1. Обновляем main
                        git checkout main
                        git pull --rebase https://%GIT_USER%:%GIT_TOKEN%@github.com/DianaParygina/WEB1LB10-master-main.git main

                        :: 2. Сливаем feature в main
                        git merge feature

                        :: 3. Пушим обновленную main на сервер
                        git push https://%GIT_USER%:%GIT_TOKEN%@github.com/DianaParygina/WEB1LB10-master-main.git main

                        :: 4. Теперь синхронизируем feature с main
                        :: feature теперь становится точной копией main
                        git checkout feature
                        git reset --hard main
                        
                        :: 5. Принудительно пушим feature
                        :: ИЗМЕНЕНО: Целевая ветка - 'feature', а не 'fix'
                        git push --force https://%GIT_USER%:%GIT_TOKEN%@github.com/AshFlaare/task_sharing_management_system.git feature

                        :: Перезапуск серверов
                        call "${PM2_CMD}" delete django || echo No Django process
                        call "${PM2_CMD}" start "${PYTHON_EXE}" --name django -- manage.py runserver 127.0.0.1:8000

                        call "${PM2_CMD}" delete vue || echo No Vue process
                        call "${PM2_CMD}" start "${CMD}" --name vue -- /c "cd ${TARGET_DIR}\\client && npm run dev"
                    """
                }
            }
        }
    }

    post {
        success {
            echo "Backend and Frontend are running via PM2!"
            echo "Backend: http://127.0.0.1:8000/"
            echo "Frontend: http://127.0.0.1:5173/"
        }
    }
}
