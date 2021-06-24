const clickAll = document.getElementById('filterAll');
const clickAct = document.getElementById('filterAct');
const clickActer = document.getElementById('filterActer');
const clickTheater = document.getElementById('filterTheater');

const view = [];
for(let i = 0; i < 3; i++) {
    view[i] = document.getElementById('view' + i);
}

const title = document.getElementsByClassName('contentTitle');
const hr = document.getElementsByTagName('hr');

function changeAll() {
    view[0].style.display = view[1].style.display = view[2].style.display = 'flex';
    title[0].style.display = title[1].style.display = title[2].style.display = 'flex';
    hr[1].style.display = hr[2].style.display='block';
}
function changeAct() {
    clickAct.checked = true;
    view[1].style.display = view[2].style.display = 'none';
    view[0].style.display = 'flex';
    title[0].style.display = 'flex';
    title[1].style.display = title[2].style.display = 'none';
    hr[1].style.display = hr[2].style.display='none';
}
function changeActer() {
    clickActer.checked = true;
    view[0].style.display = view[2].style.display = 'none';
    view[1].style.display = 'flex';
    title[1].style.display = 'flex';
    title[0].style.display = title[2].style.display = 'none';
    hr[1].style.display = hr[2].style.display='none';
}
function changeTheater() {
    clickTheater.checked = true;
    view[0].style.display = view[1].style.display = 'none';
    view[2].style.display = 'flex';
    title[2].style.display = 'flex';
    title[0].style.display = title[1].style.display = 'none';
    hr[1].style.display = hr[2].style.display='none';
}