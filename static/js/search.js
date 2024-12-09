const buttons = document.querySelectorAll(".searchInfo");
const displayDiv = document.querySelector("#displayInfo");

buttons.forEach(element => {
    element.addEventListener("click", () => {
        displayDiv.innerHTML = ""
        fetch(`get/group/${element.name}`, {
            method: 'GET',
            headers: {
                'X-CSRFToken': csrftoken,
            }
        })
        .then(response => {
            return response.json();
        })
        .then(data => {
            data.forEach(element => {
                console.log(element)
                displayDiv.innerHTML += `<tr>
                                            <td>${element.last_name} ${element.first_name}</td>
                                            <td>${element.menu}</td>
                                        </tr>`
            })
        })
    })
});