const editButtons = document.querySelectorAll(".edit");
const id = document.querySelector("#id");
const first_name = document.querySelector("#first_name");
const last_name = document.querySelector("#last_name");
const menu = document.querySelector("#menu");
const submitButton = document.querySelector("#submitButton");

editButtons.forEach(element => {
    element.addEventListener("click", () => {
        fetch(`get/${element.name}`, {
            method: 'GET',
            headers: {
                'X-CSRFToken': csrftoken,
            }
        })
        .then(response => {
            return response.json();
        })
        .then(data => {
            data.data.forEach(element => {
                id.value = element.pk
                first_name.value = element.fields.first_name;
                last_name.value = element.fields.last_name;
                menu.value = element.fields.menu
            });
        })
        .catch(error => {
            console.log(error)
        })
        
    })
});