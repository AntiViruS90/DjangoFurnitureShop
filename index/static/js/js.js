$(document).ready(function () {

    $('#btn-close').click(function () {
        $('alert_div').fadeOut('slow');
    })

    $('#btn_checkout').click(function () {
        const name = document.getElementById('id_name').value
        const surname = document.getElementById('id_surname').value
        const city = document.getElementById('id_city').value
        const street = document.getElementById('id_street').value
        const house_number = document.getElementById('id_house_number').value

        if (name&&surname&&city&&street&&house_number) {
            let url = '/checkout/'
            $.ajax(url, {
                method: 'POST',
                data: {
                    name: name,
                    surname: surname,
                    city: city,
                    street: street,
                    house_number: house_number
                },

                success: function (response) {
                    console.log(response)
                    // window.location.href = '../' # Вариант 1
                    window.location.href = response.link
                    console.log(this.data)
                },
                error: function (response) {
                    console.log(response)
                }
            })

        } else {
            alert('Please enter valid information')
        }
    })

});

// document.getElementById('btn_checkout').onclick=function() {
//         const name = document.getElementById('id_name').value
//         const surname = document.getElementById('id_surname').value
//         const city = document.getElementById('id_city').value
//         const street = document.getElementById('id_street').value
//         const house_number = document.getElementById('id_house_number').value
//         if (name&&surname&&city&&street&&house_number) {
//             let url = '/checkout/'
//             $.ajax(url, {
//                 method: 'POST',
//                 data: {
//                     name: name,
//                     surname: surname,
//                     city: city,
//                     street: street,
//                     house_number: house_number
//                 },
//
//                 success: function (response) {
//                     console.log(response)
//                     // window.location.href = '../' # Вариант 1
//                     window.location.href = response.link
//                     console.log(this.data)
//                 },
//                 error: function (response) {
//                     console.log(response)
//                 }
//             })
//
//         } else {
//             alert('Please enter valid information')
//         }
//     }