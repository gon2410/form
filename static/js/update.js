const editButtons = document.querySelectorAll(".edit");
const id = document.querySelector("#id");
const first_name = document.querySelector("#first_name");
const last_name = document.querySelector("#last_name");
const menu = document.querySelector("#menu");
const group = document.querySelector("#group");
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
            console.log(data)
            id.value = data.data.id
            first_name.value = data.data.first_name
            last_name.value = data.data.last_name
            menu.value = data.data.menu
            group.value = data.data.group.mail
        })
        .catch(error => {
            console.log(error)
        })
        
    })
});