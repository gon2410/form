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
            .then(async response => {
                if (response.ok) {
                    return response.json()
                } else {
                    const data = await response.json();
                    throw Error(data.error);
                }
            })
            .catch(() => {
                element.classList.add("is-invalid");
                submitBtn.disabled = true;
            })
        }
    })
});

