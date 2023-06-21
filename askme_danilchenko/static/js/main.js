function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');


$(".like_question").on('click', function (ev){

    const request = new Request(
        'http://127.0.0.1:8000/like/question',
        {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            },
            body: 'question_id='+ $(this).attr('data-id'),
        }
    )
    fetch(request).then(
        response_raw => response_raw.json().then(
            response_parsed => $(this).children('span').first().text(response_parsed.likes_count)
        )
    );
})


$(".like_answer").on('click', function (ev){
    const request = new Request(
        'http://127.0.0.1:8000/like/answer',
        {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            },
            body: 'answer_id='+ $(this).attr('data-id'),
        }
    )
    fetch(request).then(
        response_raw => response_raw.json().then(
            response_parsed => $(this).children('span').first().text(response_parsed.likes_count)
        )
    );
})


$(".correct_answer").on('click', function (ev){
    console.log(($(this).attr('data-id')))
    const request = new Request(
        'http://127.0.0.1:8000/answer/correct',
        {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            },
            body: 'answer_id='+ $(this).attr('data-id'),
        }
    )

   fetch(request).then(
        response_raw => response_raw.json().then(response_parsed =>  {
            if (response_parsed.solution === 'True'){
                $(this).attr('checked')
                const target = document.getElementById($(this).attr('data-id').toString())
                //target.removeAttribute('hidden')
            } else {
                $(this).removeAttr('checked')
                const target = document.getElementById($(this).attr('data-id').toString())
                //target.setAttribute("hidden", "hidden")
            }
        })
   );
})