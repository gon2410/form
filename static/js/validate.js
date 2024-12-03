const validatedFields = document.querySelectorAll(".validate-input")
const submitBtn = document.querySelector("#submit");

validatedFields.forEach(element => {
    element.addEventListener("keyup", (e) => {
        e.preventDefault();

        const value = e.target.value;
        element.classList.remove("is-invalid");
        submitBtn.removeAttribute("disabled");
        if (value.length > 0) {
            fetch("validate", {
                method: "POST",
                body: JSON.stringify({ value: value }),
                headers: {
                    'X-CSRFToken':csrftoken,
                }
            })
            .then((response) => {
                return response.json()
            })
            .then((data) => {
                if (data.error) {
                    element.classList.add("is-invalid");
                    submitBtn.disabled = true;
                }
            })
            .catch((error) => {
                console.log(error)
            })
        }
    })
});

