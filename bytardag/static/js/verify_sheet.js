"use strict";

let csrf;
let rows;
let submit;


document.addEventListener("DOMContentLoaded", function () {
    console.log('DOM Ready...');

    csrf = document.getElementById('csrf_token').value;
    rows = document.querySelectorAll('.row-verify');
    submit = document.getElementById('submit');

    for (const row of rows) {
        row.addEventListener('click', toggleVerified);
    }
});


function toggleVerified(evt) {
    let allChecked = true;
    let target = evt.target;

    while (!target.classList.contains('row-verify')) {
        target = target.parentNode;
    }


    if (target.getAttribute('checked') === null) {
        target.setAttribute('checked', 'checked');

        for (const row of rows) {
            if (row.getAttribute('checked') === null) {
                allChecked = false;
                break;
            }
        }
    } else {
        target.removeAttribute('checked');
        allChecked = false;
    }

    if (allChecked) {
        console.log('All checked! Enable verify button.');
        submit.disabled = false;
    } else {
        console.log('Some are still missing. Verify button disable.');
        submit.disabled = true;
    }
}