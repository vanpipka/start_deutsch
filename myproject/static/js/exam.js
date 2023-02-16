let questions_array = [];
let position = 0;
let has_done = false;
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
        get_end()
        return
    }

    document.getElementById("loader").hidden = false;

    let curr_question = questions_array[position];

    document.getElementById("q_section").innerText = curr_question.section.text;
    document.getElementById("q_numb").innerText = curr_question.section.description;
    document.getElementById("q_img").src = curr_question.image;

    answers = document.getElementById("q_answers")
    answers.innerHTML = '';

    append_button(answers, "<", position == 0 ? "exam_disabled" : "exam_light" , -1)

    for (let i = 0; i < curr_question.answers.length; i++) {
        append_button(answers, curr_question.answers[i], curr_question.answer == i ? "exam_selected": "exam", i, false)
    }
    append_button(answers, ">", position == questions_array.length-1 ? "exam_disabled" : "exam_light", -2)

    document.getElementById("loader").hidden = true;
}

function append_button(parent, text, class_name, index, disable){
    new_button = document.createElement("button");
    new_button.classList.add("select-rounded");
    new_button.classList.add("text-uppercase");
    new_button.classList.add("text-uppercase");
    new_button.classList.add(class_name);
    new_button.classList.add("m-3");
    new_button.onclick = ()=>check_result(index);
    new_button.innerText = text;
    parent.appendChild(new_button);
}

function check_result(index){

    if (index == -1) {
        if (position == 0) {
            return
        }
        position = position-1
    }else if (index == -2) {
        position = position+1
        console.log(position)
    }else if (index == -3) {
        get_result()
    }else{
        questions_array[position].answer = index;
        position = position+1
    }
    setTimeout(() => {set_question()}, 100);
}

function get_end() {
    position = questions_array.length-1
    document.getElementById("q_section").innerText = ""
    document.getElementById("q_numb").innerText = "";
    document.getElementById("q_img").src = "/static/img/bg/TheEnd.png";

    answers = document.getElementById("q_answers")
    answers.innerHTML = '';

    append_button(answers, "Вернуться к вопросам", "exam", -1);
    append_button(answers, "Проверить результат", "exam", -3);
}

function get_result() {

    if (has_done) {
        return
    }
    has_done = true;

    var formData = new FormData();
    formData.append("data", JSON.stringify({"questions": questions_array, "exam": exam_id}));
    formData.append("csrfmiddlewaretoken", document.getElementsByName("csrfmiddlewaretoken")[0].value);

    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState != 4) return;
        if (xhr.status != 200) {
        } else {
            let data = JSON.parse(xhr.responseText);
            document.location = data.url
        }
    }
    xhr.open("POST", "/exam/api/check_result/", true);
    xhr.send(formData);
}