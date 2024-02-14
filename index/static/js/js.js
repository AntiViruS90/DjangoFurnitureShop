$(document).ready(function () {

    $('#btn-close').on('click', function() {
        $('#alert_div').hide();
    });

    $('#btn_subscribe').submit(function(event) {
        event.preventDefault();

        const emailInput = $('input[type="email"]');

        if (emailInput.val().trim() === '') {
            alert('Please enter valid data');
        } else {
            alert('Thank you for subscribing');
            // Здесь можно добавить отправку данных на сервер или другие действия при успешной подписке
            emailInput.val(''); // сбросить значение поля email после успешной подписки
        }
    });


});
