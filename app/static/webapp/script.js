// Ініціалізація Telegram WebApp
const tg = window.Telegram.WebApp;
tg.expand();

// Отримуємо Telegram WebApp user
const telegramUser = tg.initDataUnsafe?.user;

// Якщо користувач доступний — беремо його id
const telegramId = telegramUser?.id;
if (!telegramId) {
    alert("Cannot retrieve Telegram ID. Try again via Telegram.");
    throw new Error("Telegram ID not found");
}

// === Форма реєстрації (Отримуємо форму з HTML по її id)
const registerForm = document.getElementById("registerForm");

// Коли форму надсилають (натискають "Submit")
if (registerForm) {
    registerForm.addEventListener("submit", async (event) => {
        event.preventDefault(); // скасовує перезавантаження сторінки

        // Отримуємо значення з полів форми і Формуємо дані в JSON-форматі
        // І додаємо до даних telegram ID
        const data = {
            fullname: document.getElementById("fullname").value,
            username: document.getElementById("username").value,
            password: document.getElementById("password").value,
            telegram_id: String(telegramId),
        };

        try {
            // Надсилаємо POST-запит до бекенду (заміни URL на свій)
            const response = await fetch(`${window.INTERVIEW_BASE_URL}/users`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            // Отримуємо відповідь
            const result = await response.json();
            if (response.ok) {
                alert(`User created! ID: ${result.id}`);

                // Надіслати боту команду або повідомлення, щоб той перевірив,
                // що користувач вже зареєстрований — і оновив меню.
                await fetch(`${window.INTERVIEW_BASE_URL}/webapp/telegram/send_start_command/`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        chat_id: telegramId,
                        text: "/start"
                    })
                });

                // Закриваємо мініапку Telegram
                tg.close();
            } else {
                alert(`Error: ${result.detail || "Something went wrong"}`);
            }

        } catch (error) {
            alert("Error: " + error.message);
            console.error(error);
        }
    });
}

// === Форма для інтерв'ю (Обробка вхідних даних (з форми) для інтерв'ю)
const profileForm = document.getElementById("profileForm");

if (profileForm) {
  profileForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const jobPosition = document.getElementById("job_position").value;
    const experience = parseFloat(document.getElementById("experience").value);
    const techStack = document.getElementById("tech_stack").value;
    const telegramId = telegramUser?.id;

    const response = await fetch(`${window.INTERVIEW_BASE_URL}/interviews`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        job_position: jobPosition,
        experience: experience,
        tech_stack: techStack,
        telegram_id: String(telegramId),
      })
    });

    const result = await response.json();
    if (response.ok) {
      alert("Interview created! Let's go");
      tg.close();
    } else {
      alert("Error: " + result.detail);
    }
  });
}

