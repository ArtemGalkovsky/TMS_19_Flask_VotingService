document.addEventListener("DOMContentLoaded", e => {
    const questionsContainer = document.querySelector(".questions_container");
    const questionDefault = document.querySelector(".question_default");
    const questionAddButton = document.querySelector(".add_question");

    addQuestion(questionsContainer, questionDefault);

    questionAddButton.addEventListener("click", e => {
        e.preventDefault();
        addQuestion(questionsContainer, questionDefault);
    })
})

function addQuestion(questionsContainer, default_question) {
    const newQuestion = default_question.cloneNode(true);
    newQuestion.hidden = false;
    newQuestion.classList.remove("question_default")
    newQuestion.classList.add("question");

    questionsContainer.appendChild(newQuestion);

    newQuestion.querySelector(".delete_question").addEventListener("click", e => {
        e.preventDefault();
        questionsContainer.removeChild(newQuestion);
    })
}