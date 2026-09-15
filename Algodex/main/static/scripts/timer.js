const timer_btn = document.querySelector('#timer-btn');

const minute_el = document.querySelector('#minute');
const second_el = document.querySelector('#second');
const milisecond_el = document.querySelector('#milisecond');

let minute = 0;
let second = 0;
let milisecond = 0;

let timer = false;

timer_btn.addEventListener('click', () => {
    if (!timer) {
        timer_btn.innerHTML = 'Stop';
        timer = true;
    } else {
        timer_btn.innerHTML = 'Try again';
        timer = false;

        const solve_time = minute * 60 + second + milisecond / 100;

        minute = 0;
        second = 0;
        milisecond = 0;

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch("/solve/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({
                time: solve_time
            })
        });
    }

    stopWatch();
})

function stopWatch() {
    if (timer) {
        milisecond++;

        if (milisecond == 100) {
            second++;
            milisecond = 0;
        }

        if (second == 60) {
            minute++;
            second = 0;
        }

        let min_string = minute;
        let sec_string = second;
        let milisecond_string = milisecond;

        if (minute < 10) {
            min_string = '0' + min_string;
        }

        if (second < 10) {
            sec_string = '0' + sec_string;
        }

        if (milisecond < 10) {
            milisecond_string = '0' + milisecond_string;
        }

        minute_el.innerHTML = min_string;
        second_el.innerHTML = sec_string;
        milisecond_el.innerHTML = milisecond_string;
        
        setTimeout(stopWatch, 10);
    }
}