// 배너슬라이드
function theaterSlid() {
    const slidePrev = document.getElementById('slide_prev');
    const slideNext = document.getElementById('slide_next');
    const slideView = document.getElementById('slideView'); // 화면에 표시되는 영역
    const slidePage = [] // 슬라이드 개수
    for(let i = 0; i < 3; i++) {
        slidePage.push(document.getElementById('slide'+i));
    }
    const slideLen = slidePage.length - 1;

    // 버튼 이벤트
    let nowIndex = 0; // 현재 위치
    let nowWidth = 0; // 현재 width
    slideNext.addEventListener('click', function() {
        if(nowIndex < slideLen) {
            nowWidth = 1200*(nowIndex + 1);
            nowIndex += 1;
            slideView.style.transition = "400ms";
            slideView.style.transform = "translate3d(-" + nowWidth + "px, 0px, 0px";
        } else {
            nowWidth = 0;
            nowIndex = 0;
            slideView.style.transition = "400ms";
            slideView.style.transform = "translate3d(-" + nowWidth + "px, 0px, 0px";
        }
    });
    slidePrev.addEventListener('click', function() {
        if(nowIndex > 0) {
            nowWidth -= 1200;
            nowIndex -= 1;
            slideView.style.transition = "400ms";
            slideView.style.transform = "translate3d(-" + nowWidth + "px, 0px, 0px";
        } else {
            nowWidth = 2400;
            nowIndex = 2;
            slideView.style.transition = "400ms";
            slideView.style.transform = "translate3d(-" + nowWidth + "px, 0px, 0px";
        }
    });
}

// 배우슬라이드
function actorSlid() {
    const actorView = document.getElementsByClassName('actor_view');
    const actorPrev = document.getElementById('actor_prev_btn');
    const actorNext = document.getElementById('actor_next_btn');

    let totalScroll = actorView[0].scrollWidth; // 전체 영역
    let nowScroll = 0;
    let moveScroll = 1100; // 움직일 범위

    // 이동버튼 클릭 이벤트
    actorNext.addEventListener('click', function() {
        if(nowScroll < totalScroll && nowScroll + moveScroll < totalScroll) {
            nowScroll += moveScroll;
            actorView[0].scrollTo(nowScroll,0);
        }
    })
    actorPrev.addEventListener('click', function() {
        if(nowScroll > 0) {
            nowScroll -= moveScroll;
            actorView[0].scrollTo(nowScroll,0);
        }
    })

}

function init() {
    theaterSlid();
    actorSlid();
}
init();