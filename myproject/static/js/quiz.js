        let words_array = [];
        let position = 0;
        let has_done = false;
        let result_visible = false;

        document.addEventListener('DOMContentLoaded', function() {
            load_words()
        }, false);

        document.addEventListener('keydown', function(event) {

            if (document.getElementById("test").hidden == false){
                if (event.code == 'ArrowRight') {
                    check_result(document.getElementById("right_word_btn"))
                }else if (event.code == 'ArrowLeft') {
                    check_result(document.getElementById("left_word_btn"))
                }
            }
        });

        function load_words(){
            let xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function() {
                if (xhr.readyState != 4) return;
                if (xhr.status != 200) {
                } else {
                    let data = JSON.parse(xhr.responseText);
                    words_array = data.data;
                    make_words_quiz_step_1();
                }
            }
            xhr.open("GET", "/quiz/api/get_random_words?count=30", true);
            xhr.send();
        }

        function make_words_quiz_step_1(){

            if (words_array.length == 0) {
                Alert.alert("Ошибка при загрузке, попробуйте обновить страницу");
                return;
            }

            set_question()

            document.getElementById("loader").hidden = true;
            setTimeout(() => {document.getElementById("test").hidden = false;}, 500);

        }

        function check_result(el){
            text_el = document.getElementById('question_word')
            if (words_array[position-1].left == 1){
                if (el.id=="left_word_btn"){
                    el.classList.add("success")
                    el.classList.remove("info-border")
                    text_el.style.color = "#4cd3e3"
                    words_array[position-1].result = true
                }else{
                    el.classList.add("danger")
                    el.classList.remove("info-border")
                    text_el.style.color = "#f44a40"
                    words_array[position-1].result = false
                }
            }else{
                if (el.id=="left_word_btn"){
                    el.classList.add("danger")
                    el.classList.remove("info-border")
                    text_el.style.color = "#f44a40"
                    words_array[position-1].result = false
                }else{
                    el.classList.add("success")
                    el.classList.remove("info-border")
                    text_el.style.color = "#4cd3e3"
                    words_array[position-1].result = true
                }
            }
            setTimeout(() => {set_question()}, 1000);

        }

        function set_question(){

            if (position >= words_array.length) {
                get_result()
                return
            }

            let curr_question = words_array[position]
            let lft_btn = document.getElementById("right_word_btn")
            let rgt_btn = document.getElementById("left_word_btn")
            let qst_word = document.getElementById("question_word")

            qst_word.innerHTML = curr_question.text;
            qst_word.style.color = "#fff"

            lft_btn.classList.remove("danger")
            lft_btn.classList.remove("success")
            lft_btn.classList.add("info-border")

            rgt_btn.classList.remove("danger")
            rgt_btn.classList.remove("success")
            rgt_btn.classList.add("info-border")

            if (curr_question.left == 1) {
                document.getElementById("left_word").innerHTML = curr_question.translation;
                document.getElementById("right_word").innerHTML = curr_question.wrong_answer;
            }else{
                document.getElementById("right_word").innerHTML = curr_question.translation;
                document.getElementById("left_word").innerHTML = curr_question.wrong_answer;
            }
            document.getElementById("words_count").innerHTML = words_array.length-position;
            position = position+1

        }

        function get_result(){

            if (result_visible) {
                return
            }
            result_visible = true

            document.getElementById("test").hidden = true;
            document.getElementById("result").hidden = false;
            let r_body = document.getElementById("result_body");
            let right_answers = words_array.length;

            for (let i=0; i<words_array.length; i++){
                let el = words_array[i]
                tr = document.createElement("TR");

                if (el.result != true){
                    tr.style.backgroundColor = "#fa8490"
                    right_answers--
                }

                tr.innerHTML = "<th scope='row'>"+
                    (i+1)+"</th><td>"+
                    el.text+"</td><td>"+
                    el.translation+"</td>";
                r_body.appendChild(tr)
            }
            document.getElementById("result_header").innerHTML = "Результат: "
                                            +(right_answers)+"/"+words_array.length;

            set_result(right_answers)
        }

        function set_result(right_answers){

            if (has_done) {
                return
            }
            has_done = true;

            var formData = new FormData();
            formData.append("data", JSON.stringify({right: right_answers, all: words_array.length}));
            formData.append("csrfmiddlewaretoken", document.getElementsByName("csrfmiddlewaretoken")[0].value);

            var xhr = new XMLHttpRequest();
            xhr.open("POST", "/quiz/api/set_words_result", true);
            xhr.send(formData);

        }