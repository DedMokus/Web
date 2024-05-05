const connectAPI = "http://127.0.0.1:8000";

function showContent(targetId) {
    var contentDiv = document.getElementById('content');

    switch (targetId) {
        case 'home':
            contentDiv.innerHTML=`
                <h2>
                    Добро пожаловать в сервис анализа вебинаров!
                </h2>    
            `;
            break;

        case 'upload-block':
            contentDiv.innerHTML=`
                <div class="block" id="upload-block">
                    <div class="load-box" id="load-box">
                        <form id="upload-form">
                            <label class="slice">
                                <input class="form-control" type="file" id="fileInput" accept="upload/*" required>
                            </label>
                            <button class="btn btn-outline-dark" type="submit">Загрузить</button>
                        </form>
                    </div>
                </div>
            `;
            document.getElementById('upload-form').addEventListener('submit', function(event) {
                event.preventDefault(); // Предотвращаем стандартное поведение формы
                
                var fileInput = document.getElementById('fileInput');
                var file = fileInput.files[0]; // Получаем выбранный файл
                
                var formData = new FormData(); // Создаем объект FormData для отправки данных
                
                formData.append('file', file); // Добавляем файл в FormData с ключом 'file'

                console.log("File load");
                
                // Отправляем запрос POST на ваш API
                fetch(connectAPI+"/upload", {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    console.log('Ответ от сервера:', data);
                    if (data.success) {
                        var successMessage = document.createElement('p');
                        successMessage.className = "success-message";
                        successMessage.textContent = "Load success";
                        document.getElementById("load-box").appendChild(successMessage);
                        // Очищаем форму
                        document.getElementById('upload-form').reset();
                    }
                })
                .catch(error => {
                    console.error('Ошибка при отправке запроса:', error);
                });
                });
            break;
        
        case 'global-stat-block':
            contentDiv.innerHTML = "";
            contentDiv.innerHTML = `
                <div id="global-stat-block">
                
                </div>
            `;
            fetch(connectAPI+"/general-data", {
                method: 'GET'
            })
            .then(response => response.json())
            .then(data => {
                
                var host = document.getElementById('global-stat-block');

                var block = document.createElement('div');
                block.className = 'img_block';

                var img = document.createElement('img');
                img.className = 'img_img';
                img.src = data['path'];

                var pred = document.createElement('p');
                pred.className = 'prediction';
                pred.textContent = data["data"];

                block.appendChild(img);
                block.appendChild(pred);

                host.appendChild(block);
            })
            .catch(error => {
                console.error('Ошибка при отправке запроса:', error);
            });
            break;
        
        case 'sep-stat-block':
            contentDiv.innerHTML = "";
            contentDiv.innerHTML = `
                <div id="sep-stat-block"></div>
            `;
            fetch(connectAPI+"/sep-data", {
                method: 'GET'
            })
            .then(response => response.json())
            .then(data => {
                var host = document.getElementById('sep-stat-block');

                data.forEach(function(predict) {
                    console.log(predict);

                    var block = document.createElement('div');
                    block.className = 'img_block';

                    var img = document.createElement('img');
                    img.className = 'img_img';
                    img.src = predict['path'];

                    var pred = document.createElement('p');
                    pred.className = 'prediction';
                    pred.textContent = predict["data"];

                    block.appendChild(img);
                    block.appendChild(pred);

                    host.appendChild(block);

                });
            });
            break;

        case 'login-block':
            contentDiv.innerHTML=`
                <div class="login-div">
                    <div id="buttonsContainer">
                        <button id="registrationButton">Регистрация</button>
                        <button id="loginButton">Вход</button>
                    </div>

                    <div id="registrationForm" style="display: none;">
                        <h2>Регистрация</h2>
                        <form id="regForm">
                            <input type="text" id="regUsername" placeholder="Имя пользователя" required>
                            <input type="password" id="regPassword" placeholder="Пароль" required>
                            <input type="password" id="confirmPassword" placeholder="Подтвердите пароль" required>
                            <input type="submit" value="Зарегистрироваться">
                            <p id="registrationError" class="error"></p>
                        </form>
                    </div>

                    <div id="loginForm" style="display: none;">
                        <h2>Вход</h2>
                        <form id="loginForm">
                            <input type="text" id="loginUsername" placeholder="Имя пользователя" required>
                            <input type="password" id="loginPassword" placeholder="Пароль" required>
                            <input type="submit" value="Войти">
                            <p id="loginError" class="error"></p>
                        </form>
                    </div>

                </div>
            `;
            document.getElementById("registrationButton").addEventListener("click", function() {
                document.getElementById("registrationForm").style.display = "block";
                document.getElementById("loginForm").style.display = "none";
            });
    
            document.getElementById("loginButton").addEventListener("click", function() {
                document.getElementById("registrationForm").style.display = "none";
                document.getElementById("loginForm").style.display = "block";
            });

            document.getElementById("regForm").addEventListener("submit", function(event) {
                event.preventDefault();
                var regUsername = document.getElementById("regUsername").value;
                var regPassword = document.getElementById("regPassword").value;
                var confirmPassword = document.getElementById("confirmPassword").value;
                var registrationError = document.getElementById("registrationError");
    
                if (regPassword !== confirmPassword) {
                    registrationError.textContent = "Пароли не совпадают";
                } else {
                    var formData = {
                        "username": regUsername,
                        "password": regPassword
                    };
                    fetch(connectAPI+"/register", {
                        method: 'POST',
                        body: formData
                    })
                    .then(response => response.json())
                    .then(data => {
                        console.log('Ответ от сервера:', data);
                        if (data.success) {
                            var messageForm = document.getElementById('registrationError');
                            messageForm.textContent = "Registration success!";
                        }
                    })
                    .catch(error => {
                        var messageForm = document.getElementById('registrationError');
                        messageForm.textContent = "Registration failed";
                        console.error('Ошибка при отправке запроса:', error);
                    });
                }
            });
    
            document.getElementById("loginForm").addEventListener("submit", function(event) {
                event.preventDefault();
                var loginUsername = document.getElementById("loginUsername").value;
                var loginPassword = document.getElementById("loginPassword").value;
                var loginError = document.getElementById("loginError");
    
                var formData = {
                    "username": loginUsername,
                    "password": loginPassword
                };
                fetch(connectAPI+"/login", {
                    method: "POST",
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    console.log("Ответ от сервера:", data);
                    if (data.success) {
                        var messageForm = document.getElementById('loginError');
                            messageForm.textContent = "Login success!";
                    }
                })
                .catch(error => {
                    var messageForm = document.getElementById('loginError');
                        messageForm.textContent = "Login failed";
                        console.error('Ошибка при отправке запроса:', error);
                });
                alert("Вход успешен!");
                loginError.textContent = "";
            });
            break;

        default:
            contentDiv.innerHTML = `
                <h2>Page not found!</h2>
            `;
            break;
    }
}