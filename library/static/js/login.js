var URL = {
    'login': '{% url "user:login" %}',
};

var g_auth = localStorage.getItem("auth");
if(g_auth == null) {
    g_auth = sessionStorage.getItem("auth");
}

if(g_auth) {
    try {
        g_auth = JSON.parse(g_auth);
    } catch(error) {
        g_auth = null;
    }
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
var initLogin = function() {
    if(g_auth) {
        $('#non-logged-in').hide();
        $('#logged-in').show();
        $('#span-email').html(g_auth.username);
        if(g_auth.remember_me) {
            localStorage.setItem("auth", JSON.stringify(g_auth));
        } else {
            sessionStorage.setItem("auth", JSON.stringify(g_auth));
        }
    } else {
        $('#non-logged-in').show();
        $('#logged-in').hide();
        $('#span-email').html('');
        localStorage.removeItem("auth");
        sessionStorage.removeItem("auth");
    }
    $('#test-auth-response').html("");
};
$('#loginOkButton').click(function() {
    var email= $('#signin-email').val();
    var password = $('#signin-password').val();
    var remember_me = $('#input-local-storage').prop('checked');
    if(email && password) {
        console.log("Will try to login with ", email, password);
        $('#modal-error').addClass('d-invisible');
        $.ajax({
            url: URL.login,
            method: "POST",
            data: {
                email: email,
                password: password,
                csrfmiddlewaretoken: csrftoken
            }
        }).done(function(data) {
            console.log("DONE: ", email, data.key);
            g_auth = {
                email: email,
                key: data.key,
                remember_me: remember_me
            };
            $('#cd-login').removeClass('active');
            initLogin();
            // CAREFUL! csrf token is rotated after login: https://docs.djangoproject.com/en/1.7/releases/1.5.2/#bugfixes
            csrftoken = getCookie('csrftoken');
        }).fail(function(data) {
            console.log("FAIL", data);
            $('#modal-error').removeClass('d-invisible');
        });
    } else {
        $('#modal-error').removeClass('d-invisible');
    }
});
