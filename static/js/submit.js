const form = document.querySelector("#form");
const email = document.querySelector("#email");

const firstNameOne = document.querySelector("#first_name_one");
const lastNameOne = document.querySelector("#last_name_one");
const menuOne = document.querySelector("#menu_one");

const firstNameTwo = document.querySelector("#first_name_two");
const lastNameTwo = document.querySelector("#last_name_two");
const menuTwo = document.querySelector("#menu_two");

const note = document.querySelector("#note");

const successModal = new bootstrap.Modal(document.querySelector("#successModal"), {
    keyboard: false
})

const errorModal = new bootstrap.Modal(document.querySelector("#errorModal"), {
    keyboard: false
})

const successModalMessage = document.querySelector("#successModalMessage");
const errorModalMessage = document.querySelector("#errorModalMessage");


function cleanUp() {
    email.value = "";

    firstNameOne.value = "";
    firstNameTwo.value = "";

    lastNameOne.value = "";
    lastNameTwo.value = "";
    
    menuOne.value = "Menú";
    menuTwo.value = "Menú";

    note.value = "";

    submitBtn.removeAttribute("disabled");
    submitBtn.value = "Confirmar";
}


form.addEventListener("submit", function(e){
    e.preventDefault();
    
    const formData = new FormData();

    let first_invite = {
        firstname: firstNameOne.value,
        lastname: lastNameOne.value,
        menu: menuOne.value
    }

    let second_invite = {
        firstname: firstNameTwo.value,
        lastname: lastNameTwo.value,
        menu: menuTwo.value
    }

    let invites = {
        first_invite: first_invite,
        second_invite: second_invite
    }

    formData.append('invites', JSON.stringify(invites));

    formData.append('mail', email.value);
    formData.append('note', note.value);
    submitBtn.disabled = true;
    submitBtn.value = "Cargando..."

    fetch("creategroup", {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrftoken,
        }
    })
    .then(async response => {
        if (response.ok) {
            return response.json();
        } else {
            const data = await response.json();
            throw Error(data.error);
        }
    })
    .then(data => {
        if (data.success) {
            successModalMessage.innerHTML = data.success;
            successModal.show();
        } else {
            errorModalMessage.innerHTML = data.error;
            errorModal.show();
        }
    })
    .catch(error => {
        errorModalMessage.innerHTML = error.message;
        errorModal.show();
    })
    cleanUp();
});