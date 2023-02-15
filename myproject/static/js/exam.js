let questions_array = [];
let position = 0;
let has_done = false;
let result_visible = false;
let exam_id = document.getElementById("exam_id").value;

document.addEventListener('DOMContentLoaded', function() {
    load_questions()
}, false);

function load_questions(){
    let xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState != 4) return;
        if (xhr.status != 200) {
        } else {
            let data = JSON.parse(xhr.responseText);
            questions_array = data.data;
            console.log(questions_array)
            make_exam_step_1();
        }
    }
    xhr.open("GET", "/exam/api/get_questions/?id="+exam_id, true);
    xhr.send();
}

function make_exam_step_1(){

    if (questions_array.length == 0) {
        Alert.alert("Ошибка при загрузке, попробуйте обновить страницу");
        return;
    }

    set_question();
    setTimeout(() => {document.getElementById("test").hidden = false;}, 500);

}

function set_question(){

    if (position >= questions_array.length) {
        get_result()
        return
    }

    document.getElementById("loader").hidden = false;

    let curr_question = questions_array[position];

    document.getElementById("q_section").innerText = curr_question.section.text;
    document.getElementById("q_numb").innerText = curr_question.section.description;
    document.getElementById("q_img").src = curr_question.image;

    answers = document.getElementById("q_answers")
    answers.innerHTML = '';

    for (let i = 0; i < curr_question.answers.length; i++) {
        new_button = document.createElement("button");
        new_button.classList.add("select-rounded");
        new_button.classList.add("text-uppercase");
        new_button.classList.add("exam");
        new_button.classList.add("m-3");
        new_button.onclick = ()=>check_result(i);
        new_button.innerText = curr_question.answers[i];
        answers.appendChild(new_button);
    }
    document.getElementById("loader").hidden = true;
}

function check_result(index){

    questions_array[position].answer = index;
    position = position+1
    setTimeout(() => {set_question()}, 500);

}

function get_result() {
    console.log("result is here")
}