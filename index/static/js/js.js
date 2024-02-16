$(document).ready(function () {

    $('#btn-close').on('click', function() {
        $('#alert_div').hide();
    });

    $('#btn_subscribe').on('click', function(event) {
        event.preventDefault();

        const emailInput = $('input[type="email"]');
        const emailValue = emailInput.val().trim();

        // Регулярное выражение для проверки формата email
        const emailFormat = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (emailValue === '' || !emailFormat.test(emailValue)) {
            alert('Please enter a valid email address');
        } else {
            alert('Thank you for subscribing');
            // Здесь можно добавить отправку данных на сервер или другие действия при успешной подписке
            emailInput.val(''); // сбросить значение поля email после успешной подписки
        }
    });



});
