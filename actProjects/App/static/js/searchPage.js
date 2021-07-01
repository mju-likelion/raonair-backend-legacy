const clickAll = document.getElementById('filterAll');
const clickAct = document.getElementById('filterAct');
const clickActor = document.getElementById('filterActor');
const clickTheater = document.getElementById('filterTheater');

const view = [];
for(let i = 0; i < 3; i++) {
    view.push(document.getElementById('view' + i));
}

const title = document.getElementsByClassName('contentText');
const hr = document.getElementsByTagName('hr');
let cntAct = 0;
let cntActor = 0;

function changeAll() {
    // 임시로 전체 버튼을 클릭하면 새로 추가된 요소 삭제를 위함
    window.location.reload();
}
function changeAct() {
    clickAct.checked = true;
    view[1].style.display = view[2].style.display = 'none';
    view[0].style.display = 'flex';
    title[0].style.display = 'flex';
    title[1].style.display = title[2].style.display = 'none';
    hr[1].style.display = hr[2].style.display='none';
    cntAct += 1;
    if(cntAct <= 1)
        addMoreAct();
}
function changeActor() {
    clickActor.checked = true;
    view[0].style.display = view[2].style.display = 'none';
    view[1].style.display = 'flex';
    title[1].style.display = 'flex';
    title[0].style.display = title[2].style.display = 'none';
    hr[1].style.display = hr[2].style.display='none';
    cntActor += 1;
    if(cntActor <= 1)
        addMoreActor();
}
function changeTheater() {
    clickTheater.checked = true;
    view[0].style.display = view[1].style.display = 'none';
    view[2].style.display = 'flex';
    title[2].style.display = 'flex';
    title[0].style.display = title[1].style.display = 'none';
    hr[1].style.display = hr[2].style.display='none';
}
function addMoreAct() {
    const imgsrc = [
        'http://tkfile.yes24.com/upload2/PerfBlog/202106/20210614/20210614-39335.jpg',
        'http://tkfile.yes24.com/upload2/PerfBlog/202103/20210316/20210316-38572.jpg',
        'http://tkfile.yes24.com/upload2/PerfBlog/202106/20210615/20210615-39354.jpg',
        'http://tkfile.yes24.com/upload2/PerfBlog/202104/20210427/20210427-38965.jpg'
    ];
    const actName = ['일리아드','연극라면','토지','거룩한 직업'];

    for(let i = 0; i < 4; i++) {
        const posterEle = document.createElement('div');
        posterEle.className = 'poster';
        const imgInnerEle = document.createElement('a');
        imgInnerEle.className = 'imgInner';

        const imgEle = document.createElement('img');
        imgEle.className = 'actImg';
        imgEle.src = imgsrc[i];
        imgInnerEle.appendChild(imgEle);

        const posterBtnEle = document.createElement('div');
        posterBtnEle.className = 'posterBtn';
        posterBtnEle.innerHTML = '<p>' + actName[i] + '</p>';

        const posterBtn1 = document.createElement('button');
        posterBtn1.className = 'detailBtn';
        posterBtn1.innerText = '자세히';
        const posterBtn2 = document.createElement('button');
        posterBtn2.className = 'detailBtn';
        posterBtn2.innerText = '극단 보기';

        posterBtnEle.appendChild(posterBtn1);
        posterBtnEle.appendChild(posterBtn2);
        posterEle.appendChild(imgInnerEle);
        posterEle.appendChild(posterBtnEle);

        view[0].appendChild(posterEle);
    }
}
function addMoreActor() {
    const actorName = ['설유진','김수진','이달','전국향','이주승'];
    for(let i = 0; i < 5; i++) {
        const posterEle = document.createElement('div');
        posterEle.className = 'poster';
        const imgInnerEle = document.createElement('a');
        imgInnerEle.className = 'imgInner';

        const imgEle = document.createElement('img');
        imgEle.className = 'actorImg';
        imgEle.src = `http://127.0.0.1:8000/static/img/actor${i + 6}.jpg`; // Template literal
        imgInnerEle.appendChild(imgEle);

        const posterBtnEle = document.createElement('div');
        posterBtnEle.className = 'posterBtn';
        posterBtnEle.style = 'text-align:center;'
        posterBtnEle.innerHTML = '<p>'+ actorName[i] +'</p>';

        posterEle.appendChild(imgInnerEle);
        posterEle.appendChild(posterBtnEle);

        view[1].appendChild(posterEle);
    }
}