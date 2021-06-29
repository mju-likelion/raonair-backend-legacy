// 배너슬라이드
function theaterSlid() {
    const slideWrap = document.getElementById('slideWrap');
    const slidePrev = document.getElementById('slide_prev');
    const slideNext = document.getElementById('slide_next');
    const slideView = document.getElementById('slideView');
    const slidePage = []
    for(let i = 0; i < 3; i++) {
        slidePage.push(document.getElementById('slide'+i));
    }
    const slideLen = slidePage.length - 1;

    // 버튼 이벤트
    let nowIndex = 0;
    slideNext.addEventListener('click', function() {
        if(nowIndex <= slideLen) {
            slideView.style.transition = "400ms";
            slideView.style.transform = "translate3d(-" + (1200 * (nowIndex + 1)) + "px, 0px, 0px";
        } else {

        }
        nowSlid = slidePage[++nowIndex];
    })
}

// 배우슬라이드
function acterSlid() {
    console.log('실행');
    const acterView = document.getElementsByClassName('acter_view');
    const acterPrev = document.getElementById('acter_prev_btn');
    const acterNext = document.getElementById('acter_next_btn');

    let totalScroll = acterView[0].scrollWidth;
    let nowScroll = 0;
    let moveScroll = 1100;

    // 이동버튼 클릭 이벤트
    acterNext.addEventListener('click', function() {
        if(nowScroll < totalScroll && nowScroll + moveScroll < totalScroll) {
            nowScroll += moveScroll;
            acterView[0].scrollTo(nowScroll,0);
        }
    })
    acterPrev.addEventListener('click', function() {
        if(nowScroll > 0) {
            nowScroll -= moveScroll;
            acterView[0].scrollTo(nowScroll,0);
        }
    })

}

function init() {
    theaterSlid();
    acterSlid();
}
init();