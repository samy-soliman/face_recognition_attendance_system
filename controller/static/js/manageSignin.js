function handlecsrf() {

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
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

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

}



function signInCompany() {
    handlecsrf();
    var companyEmail = document.getElementById("companyEmail").value;
    var companyPassword = document.getElementById("companyPassword").value;

    var data = {
        'email': companyEmail,
        'password': companyPassword,
    }

    $.ajax({
        type: 'POST',
        url: '',
        data: data,
        success: function (data) {
            if(data.type === "error")
            {
                $("#messageDiv1").addClass('alert alert-danger').removeClass('alert alert-success').html(data.message).fadeIn('fast');
                $("#messageDiv1").delay(3500).fadeOut('slow');
            }
            else if (data.type === "success")
            {
                window.location.replace("/");
            }

            
        },
    });    
}