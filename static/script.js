

const connectAPI = "http://127.0.0.1:8000";


var isLogin = false;
var contentDiv = document.getElementById('content');
var currentUser = {};

function showContent(targetId) {

    function updateButton() {
        const loginbutton = document.getElementById("login-button");
        if (isLogin) {
            loginbutton.textContent = "Профиль";
        }
        else {
            loginbutton.innerText = "Вход в аккаунт";
        }
    }

    

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
                        successMessage.textContent = "Загрузка завершена";
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
                <div id="myModal" class="modal" tabindex="-1">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">Разметка времени</h5>
                            </div>
                            <div class="modal-body">
                                <p>Modal body text goes here.</p>
                            </div>
                            <div class="modal-footer">
                                <button type="button" id="btn-close" data-bs-dismiss="modal">Close</button>
                            </div>
                        </div>
                    </div>
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

                buttons = createButtons();

                block.appendChild(img);
                block.appendChild(pred);

                block.appendChild(buttons);

                host.appendChild(block);
            })
            .catch(error => {
                console.error('Ошибка при отправке запроса:', error);
            });
            break;
        
        case 'sep-stat-block':
            contentDiv.innerHTML = "";
            contentDiv.innerHTML = `
                <div id="carousel">
                    <div id="items">

                    </div>
                    <div>
                        <div id="prevBtn" class="nav-btn" style="display: none">←</div>
                        <div id="nextBtn" class="nav-btn" style="display: none">→</div>
                    </div>
                </div>
                <div id="myModal" class="modal" tabindex="-1" style="display: none">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">Разметка времени</h5>
                            </div>
                            <div class="modal-body">
                                
                            </div>
                            <div class="modal-footer">
                                <button type="button" id="btn-close" data-bs-dismiss="modal">Close</button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            const carousel = document.getElementById('carousel');
            const itemsContainer = document.getElementById('items');
            const prevBtn = document.getElementById('prevBtn');
            const nextBtn = document.getElementById('nextBtn');

            let items = [];
            let currentItemIndex = 0;
            let keepRunning = true;

            function renderItems() {
                itemsContainer.innerHTML = '';
                const currentIndex = currentItemIndex % items.length;
                const currentItem = items[currentIndex];
                var host = document.getElementById('items');
                var block = document.createElement('div');
                    
                block.className = 'img_block';

                var img = document.createElement('img');
                img.className = 'img_img';
                img.src = currentItem['path'];

                var header = document.createElement("h2")
                header.textContent = "Выводы о данном вебинаре"
                var pred = document.createElement('p');
                pred.className = 'prediction';
                pred.textContent = currentItem["data"];
                
                buttons = createButtons(currentItem['ID']);

                block.appendChild(img);
                block.appendChild(header);
                block.appendChild(pred);

                block.appendChild(buttons);

                host.appendChild(block);
            }

            
            fetch(connectAPI+"/sep-data", {
                method: 'GET'
            })
            .then(response => response.json())
            .then(data => {
                items = data;
                prevBtn.style.display = "flex";
                nextBtn.style.display = "flex";
                renderItems();
                function showPrevItem() {
                    currentItemIndex--;
                    renderItems();
                }
                
                // Показать следующий элемент
                function showNextItem() {
                    currentItemIndex++;
                    renderItems();
                }
                
                // Обработчики событий для стрелок
                prevBtn.addEventListener('click', showPrevItem);
                nextBtn.addEventListener('click', showNextItem);
            });


            



            break;

        case 'login-block':
            if (isLogin){
                contentDiv.innerHTML = "";
                contentDiv.innerHTML = `
                <div>
                    <h2>Профиль пользователя</h2>
    
                    <div>
                    <p>Имя пользователя: <span id="username"></span></p>
                    <p>Email: <span id="email"></span></p>
                    </div>
                </div>
                `;

                const username = document.getElementById('username');
                const email = document.getElementById('email');

                username.textContent = currentUser['username'];
                email.textContent = currentUser['email'];

                var checkbox = document.getElementById('notificationCheckbox').value;

            }
            else {
                contentDiv.innerHTML = "";
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
                                <input type="email" id="regEmail" placeholder="Email" required>
                                <input type="password" id="regPassword" placeholder="Пароль" required>
                                <input type="password" id="confirmPassword" placeholder="Подтвердите пароль" required>
                                <input type="submit" value="Зарегистрироваться">
                                <p id="registrationError" class="error"></p>
                            </form>
                        </div>

                        <div id="loginForm" style="display: none;">
                            <h2>Вход</h2>
                            <form id="loginForm">
                                <input type="text" id="loginEmail" placeholder="Ваш email" required>
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
                    var regEmail = document.getElementById("regEmail").value;
                    var confirmPassword = document.getElementById("confirmPassword").value;
                    var registrationError = document.getElementById("registrationError");
        
                    if (regPassword !== confirmPassword) {
                        registrationError.textContent = "Пароли не совпадают";
                    } else {
                        var formData = {
                            "username": regUsername,
                            "email": regEmail,
                            "password": regPassword
                        };
                        fetch(connectAPI+"/register", {
                            method: 'POST',
                            headers: {
                                'Content-Type': "application/json"
                            },
                            body: JSON.stringify(formData)
                        })
                        .then(response => response.json())
                        .then(data => {
                            console.log('Ответ от сервера:', data);
                            if (data.success) {
                                var messageForm = document.getElementById('registrationError');
                                messageForm.textContent = "Registration success!";
                                showContent("home");
                            } else {
                                var messageForm = document.getElementById('registrationError');
                                messageForm.textContent = "Registration failed";
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
                    var loginEmail = document.getElementById("loginEmail").value;
                    var loginPassword = document.getElementById("loginPassword").value;
        
                    var formData = {
                        "email": loginEmail,
                        "password": loginPassword
                    };
                    fetch(connectAPI+"/login", {
                        method: "POST",
                        headers: {
                            'Content-Type': "application/json"
                        },
                        body: JSON.stringify(formData)
                    })
                    .then(response => response.json())
                    .then(data => {
                        console.log("Ответ от сервера:", data);
                        if (data.success) {
                            var messageForm = document.getElementById('loginError');
                                messageForm.textContent = "Login success!";
                                isLogin = true;
                                currentUser = data.user;
                                updateButton();
                                showContent("home");
                        } else {
                            var messageForm = document.getElementById('loginError');
                            messageForm.textContent = "Login failed";
                        }
                    })
                    .catch(error => {
                        var messageForm = document.getElementById('loginError');
                            messageForm.textContent = "Login failed";
                            console.error('Ошибка при отправке запроса:', error);
                    });
                });
            }
            break;

        default:
            contentDiv.innerHTML = `
                <h2>Page not found!</h2>
            `;
            break;

        function createButtons(id = null) {
            const groupefewfs = {
                "Вежливость": "Polite", 
                "Технические проблемы": "TechProblems", 
                "Хорошее объяснение материала": "GoodExplain", 
                "Плохое объяснение материала": "BadExplain", 
                "Помощь и понимание": "Help", 
                "Реклама и спам": "Spam", 
                "Оскорбления и конфликты": "Conflict", 
                "Опоздание": "Late", 
                "Выполнение задания": "TaskComplete"
            };
            const color_sheet = {
                "Вежливость": '#0000CD',
                "Технические проблемы": '#FF0000',
                "Хорошее объяснение материала": '#000000',
                "Плохое объяснение материала и сложность": '#FFDAB9',
                "Помощь и понимание": '#FF69B4',
                "Реклама и спам": '#006400',
                "Оскорбления и конфликты": '#808080',
                "Опоздание": '#FFFF00',
                "Выполнение задания": '#800000',
            }
        

            var main = document.createElement('div');
            main.className = "class-button-block";

            var explain = document.createElement('h2');
            explain.textContent = "Выберите какие сообщения вывести:";

            main.appendChild(explain);

            

            for (const key in groupefewfs) {
                if (groupefewfs.hasOwnProperty(key)) {
                    (function() {
                        const butto = document.createElement('input');
                        butto.type = 'button';
                        butto.value = key;
                        let hrefValue;

                        if (id == null) {
                            hrefValue = '/filter?need_class=' + encodeURIComponent(groupefewfs[key]);
                        } else {
                            hrefValue = '/filter?need_class=' + encodeURIComponent(groupefewfs[key]) + '&id=' + encodeURIComponent(id);
                        }
                        butto.onclick = function() {
                            fetch(connectAPI+hrefValue)
                            .then(response => response.json())
                            .then(data => {                                
                                var modal = document.getElementById("myModal");
                                modal.style.display = "block";

                                var modalBody = document.querySelector(".modal-body");
                                modalBody.innerHTML = "";

                                // Определяем кнопку "Close" в модальном окне
                                var closeButton = document.getElementById("btn-close");
                                closeButton.onclick = function() {
                                    var modal = document.getElementById("myModal");
                                    modal.style.display = "none"; // Закрываем модальное окно
                                };

                                // Закрываем модальное окно при клике за его пределами
                                window.onclick = function(event) {
                                    var modal = document.getElementById("myModal");
                                    if (event.target == modal) {
                                        modal.style.display = "none"; // Закрываем модальное окно
                                    }
                                };

                                var table = document.createElement('table');
                                table.className = "table";

                                console.log(data);                                
                                for (const row in data) {
                                    var roww = data[row];
                                    var tr = document.createElement('tr');
                                    var td1 = document.createElement("td");
                                    var td2 = document.createElement("td");

                                    td1.textContent = roww['MessageTime'];
                                    td2.textContent = roww['Message'];

                                    tr.appendChild(td1);
                                    tr.appendChild(td2);
                                    table.appendChild(tr);
                                }

                                modalBody.appendChild(table);
                            });
                    
                        };
                    butto.style.backgroundColor = color_sheet[key];
                    butto.style.border = "1px";
                    butto.style.color = "#fff";

                    main.appendChild(butto);
                })();
                    
                }
            }
            return main;
        }
    }
}