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

function addGrade() {
    handlecsrf();
    var manageType = document.getElementById("addGradeManage").value;
    var gradeName = document.getElementById("gradeName").value;
    

    var data = {
        'gradeName': gradeName,
        'manageType': manageType
    }

    $(document).ready( function () {

        $("#loadingdiv").css("display", "block");
    
        $(document).ajaxComplete(function () {
            $("#loadingdiv").css("display", "none");
        });
    });

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
                window.location.replace("");
            }
        },
        
    });
}

function addCourse() {
    handlecsrf();
    var manageType = document.getElementById("addCourseManage").value;
    var courseName = document.getElementById("courseName").value;
    var selectedGrade = document.getElementById("selectedGrade").value;
    var selectedInstructor = document.getElementById("selectedInstructor").value;

    var data = {
        'manageType':manageType,
        'name': courseName,
        'grade': selectedGrade,
        'instructor':selectedInstructor,
    }
    $(document).ready( function () {

        $("#loadingdiv").css("display", "block");
    
        $(document).ajaxComplete(function () {
            $("#loadingdiv").css("display", "none");
        });
    });

    $.ajax({
        type: 'POST',
        url: '',
        data: data,
        success: function (data) {
            if(data.type === "error")
            {
                $("#messageDiv2").addClass('alert alert-danger').removeClass('alert alert-success').html(data.message).fadeIn('fast');
                $("#messageDiv2").delay(3500).fadeOut('slow');
            }
            else if (data.type === "success")
            {
                window.location.replace("");
            }
        },
    });    
}

function addInstructor() {
    handlecsrf();
    var manageType = document.getElementById("addInstructorManage").value;
    var instructorName = document.getElementById("instructorName").value;
    var instructorEmail = document.getElementById("instructorEmail").value;
    var instructorPassword = document.getElementById("instructorPassword").value;

    var data = {
        'manageType':manageType,
        'username': instructorName,
        'password': instructorPassword,
        'email':instructorEmail,
    }
    $(document).ready( function () {

        $("#loadingdiv").css("display", "block");
    
        $(document).ajaxComplete(function () {
            $("#loadingdiv").delay(2000).css("display", "none");
        });
    });

    $.ajax({
        type: 'POST',
        url: '',
        data: data,
        success: function (data) {
            if(data.type === "error")
            {
                $("#messageDiv3").addClass('alert alert-danger').removeClass('alert alert-success').html(data.message).fadeIn('fast');
                $("#messageDiv3").delay(3500).fadeOut('slow');
            }
            else if (data.type === "success")
            {
                window.location.replace("");
            }
            
        },
    });    
}

function addStudent() {
    handlecsrf();
    var manageType = document.getElementById("addStudentManage").value;
    var studentName = document.getElementById("studentName").value;
    var studentGrade = document.getElementById("studentGrade").value;
    var studentPhotos = document.getElementById("studentPhotos").value;

    var data = {
        'manageType':manageType,
        'username': studentName,
        'grade': studentGrade,
        'dataUrls':studentPhotos,
    }

    $(document).ready( function () {

        $("#loadingdiv").css("display", "block");
    
        $(document).ajaxComplete(function () {
            $("#loadingdiv").css("display", "none");
        });
    });

    $.ajax({
        type: 'POST',
        url: '',
        data: data,
        success: function (data) {
            if(data.type === "error")
            {
                $("#messageDiv4").addClass('alert alert-danger').removeClass('alert alert-success').html(data.message).fadeIn('fast');
                $("#messageDiv4").delay(3500).fadeOut('slow');
            }
            else if (data.type === "success")
            {
                window.location.replace("");
            }
        },
    });    
}
