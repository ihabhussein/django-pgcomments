'use strict';

window.addEventListener('load', () => {
    let overlay = document.querySelector('#overlay');
    let form_path = document.querySelector('#form-path');
    let form_text = document.querySelector('#form-text');

    document.querySelectorAll('a.add-comment').forEach(a => {
        a.addEventListener('click', ev => {
            ev.preventDefault();
            form_path.value = a.dataset['path'];
            overlay.style.display = 'flex';
            form_text.focus();
        })
    });

    document.querySelector('#btn-cancel').addEventListener('click', () => {
        overlay.style.display = 'none'
    });
});
