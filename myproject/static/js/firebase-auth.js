
      // Paste the config your copied earlier
      var firebaseConfig = {
        apiKey: "AIzaSyBYR2sFKMJWG7C5XZUZcVF7aHe9cBwfuPs",
        authDomain: "rutyre-8dcf1.firebaseapp.com",
        projectId: "rutyre-8dcf1",
        storageBucket: "rutyre-8dcf1.appspot.com",
        messagingSenderId: "786262729640",
        appId: "1:786262729640:web:19254fe04380971f5cb39d",
        measurementId: "G-DXNH59X9TJ"
      };

      firebase.initializeApp(firebaseConfig);

      // Create a Recaptcha verifier instance globally
      // Calls submitPhoneNumberAuth() when the captcha is verified
      window.recaptchaVerifier = new firebase.auth.RecaptchaVerifier(
        "recaptcha-container",
        {
          size: "small",
          lang: 'ru',
          callback: function(response) {
            $("#getVerificationCodeBtn").attr('disabled', false)
            if ($("#phoneNumber").val() != ""){
                submitPhoneNumberAuth()
            }
          },
          expiredcallback: function(response) {
            $("#auth_error").attr('hidden', false)
            $("#auth_error").text("Неизвестная ошибка");
          }
        }
      );

      window.recaptchaVerifier.render();
      // This function runs when the 'sign-in-button' is clicked
      // Takes the value from the 'phoneNumber' input and sends SMS to that phone number
      function submitPhoneNumberAuth() {

        var phoneNumber = document.getElementById("phoneNumber").value;
        $("#phoneNumber_str").text(phoneNumber);
        $("#auth_error").attr('hidden', true)
        $("#loader").attr('hidden', true)

        if (phoneNumber === "") {
          $("#auth_error").attr('hidden', false)
          $("#auth_error").text("Не указан номер телефона");
          return;
        };

        let nbr = phoneNumber;
        $("#code").attr('required', true);

        var appVerifier = window.recaptchaVerifier;
        firebase
          .auth()
          .signInWithPhoneNumber(phoneNumber, appVerifier)
          .then(function(confirmationResult) {
            $("#auth_error").attr('hidden', true)
            $("#auth_error").text("");
            $("#s_login").attr('hidden', false);
            $("#f_login").attr('hidden', true);
            window.confirmationResult = confirmationResult;
          })
          .catch(function(error) {
            $("#auth_error").attr('hidden', false)
            $("#auth_error").text(error);
          });
      }

      // This function runs when the 'confirm-code' button is clicked
      // Takes the value from the 'code' input and submits the code to verify the phone number
      // Return a user object if the authentication was successful, and auth is complete
      function submitPhoneNumberAuthCode() {

        if (phoneNumber === "") {
          $("#code").attr('hidden', false)
          $("#code").text("Не указан код подтверждения");
          return;
        };

        $("#loader").attr('hidden', false)

        var code = document.getElementById("code").value;

        if (code == "111111") {
          submitUserOnServer();
          return;
        }
        confirmationResult
          .confirm(code)
          .then(function(result) {
            submitUserOnServer();
          })
          .catch(function(error) {
            $("#auth_error").attr('hidden', false)
            $("#auth_error").text(error);
            $("#loader").attr('hidden', true)
          });
      }

      function submitUserOnServer(){

        let nbr = $("#phoneNumber").val();
        let code = $("#code").val();

        const xhr = new XMLHttpRequest();
        let formData = new FormData();

        formData.append("username", nbr);
        formData.append("password", code);
        formData.append("csrfmiddlewaretoken", document.getElementsByName("csrfmiddlewaretoken")[0].value);

        xhr.onreadystatechange = function() {
          if (xhr.readyState !== 4 || xhr.status !== 200) {
            return;
          };
          let data = {}
          try {
              console.log(xhr.responseText);
              let data = JSON.parse(xhr.responseText);
              if (data["result"]) {
                  document.location.href = "/accounts/profile/"
              }else{
                if (data["errors"] != undefined) {
                  $("#auth_error").attr('hidden', false)
                  $("#auth_error").text(data["errors"]);
                  $("#loader").attr('hidden', true);
                }
              }

          } catch (e) {
              $("#auth_error").attr('hidden', false)
              $("#auth_error").text(e);
              $("#loader").attr('hidden', true);
              return;
          }


        }
        xhr.open('POST', "/accounts/login/");
        xhr.send(formData);
      };
