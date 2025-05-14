document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const submit = document.querySelector("button");

    const inputs = form.querySelectorAll("input");

    submit.addEventListener("click", () => {
        let json = {id: inputs[0].value, questions: {}}

        inputs.forEach(input => {
            console.log(input)
            if (!input.classList.contains("hidden")) {
                json["questions"][input.dataset.id] = input.checked;
            }
        })

        fetch("/vote", {
            method: "POST",
            body: JSON.stringify(json),
            headers: {
                "Content-Type": "application/json"
            }
        }).then(response => {
            if (response.ok) {
                window.location.replace(`/view_poll?id=${inputs[0].value}`);
            }
        })
    })
})