// 1. Ініціалізація Telegram WebApp
const tg = window.Telegram.WebApp;
tg.expand(); // розгортає мініапку на весь екран

// 2. Отримуємо форму з HTML по її id
const form = document.getElementById("registerForm");

// 3. Коли форму надсилають (натискають "Submit")
form.addEventListener("submit", async (event) => {
    event.preventDefault(); // скасовує перезавантаження сторінки

    // 4. Отримуємо значення з полів форми і Формуємо дані в JSON-форматі
    const data = {
        fullname: document.getElementById("fullname").value,
        username: document.getElementById("username").value,
        password: document.getElementById("password").value,
    };

    try {
        // 6. Надсилаємо POST-запит до бекенду (заміни URL на свій)
        const response = await fetch(`${window.INTERVIEW_BASE_URL}/users`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        // 7. Отримуємо відповідь
        const result = await response.json();
        if (response.ok) {
            alert(`User created! ID: ${result.id}`);
        } else {
            alert(`Error: ${result.detail || "Something went wrong"}`);
        }

        // 8. Закриваємо мініапку Telegram
        tg.close();

    } catch (error) {
        alert("Error: " + error.message);
        console.error(error);
    }
});
