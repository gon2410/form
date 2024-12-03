const loginForm = document.querySelector("#loginForm");
const username = document.querySelector("#usernameId");
const password = document.querySelector("#passwordId");
const submitButton = document.querySelector("#submitButton");

const errorModal = new bootstrap.Modal(document.querySelector("#errorModal"), {
    keyboard: false
})
const errorModalMessage = document.querySelector("#errorModalMessage");


loginForm.addEventListener("submit", (e) => {
    e.preventDefault();

    submitButton.value = "Cargando..."
    submitButton.disabled = true;

    const formData = new FormData();
    formData.append("username", username.value);
    formData.append("password", password.value);

    fetch("login", {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrftoken,
        }
    })
    .then(async response => {
        if (response.ok) {
            cleanUp();
            window.location.href = "http://127.0.0.1:8000/administracion";
            return response.json();

        } else {
            const data = await response.json();
            throw Error(data.error);
        }
    })
    .catch(error => {
        cleanUp();
        errorModalMessage.innerHTML = error.message;
        errorModal.show();
    })
})

function cleanUp() {
    submitButton.value = "Ingresar"
    submitButton.removeAttribute("disabled");
    username.value = "";
    password.value = "";
}