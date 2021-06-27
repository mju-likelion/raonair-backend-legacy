//'yyyy-mm-dd' 형식으로 날짜를 설정하기 위해 날짜 포맷 수정
const correctDateFormat = (date) => {
    return date < 10 ? '0' + date : date;
}

//현재 날짜와 최대 날짜는 세팅한다
const setDate = (node, now, max) => {
    node.setAttribute('value', now);
    node.setAttribute('max', max);
}

//현재 날짜를 가져온다, month, date의 경우 그냥 가져오면 9이하는 앞에 0이 안붙는다
const date = new Date();
const year = date.getFullYear();
//월이 1~12가 아닌 0~11로 반환된다
const month = correctDateFormat(date.getMonth() + 1);
const day = correctDateFormat(date.getDate());
//현재 날짜와 선택 가능한 최대 날자
const now_date = `${year}-${month}-${day}`;
const max_date = `${date.getFullYear() + 1}-${month}-${day}`;

const date_from = document.getElementById('date-from__input');
const date_to = document.getElementById('date-to__input');
setDate(date_from, now_date, max_date);//검색 범위에서 '언제부터'에 해당하는 부분 세팅
setDate(date_to, now_date, max_date);////검색 범위에서 '언제까지'에 해당하는 부분 세팅


//옵션을 충족하는지 검사한다.
const satisfyOptions = (ele) => {
    const url = ele.children[0].currentSrc;
    //진짜 검색이 되는것 처럼 하기 위해 랜덤요소 사용.
    const options = ['home', 'theme', 'month'];
    const op_idx = Math.floor(Math.random() * options.length);
    return url.includes(options[op_idx]);
}

//공연 포스터가 들어가는 공간
const plays_image = document.querySelectorAll('.plays');
const search_btn = document.getElementById('input__submit-btn');
search_btn.addEventListener('click', () => {
    //옵션을 충족하는 것만 배열로 받고
    const search_result = Array.prototype.slice.call(plays_image).filter(satisfyOptions);
    //기존에 포스터들을 다 지우고
    const plays = document.getElementById('main__plays');
    while(plays.hasChildNodes()){
        plays.removeChild(plays.firstChild);
    } 
    //옵션을 충족하는 것들만 다시 넣는다.
    search_result.forEach(ele => {
        plays.appendChild(ele);
    });
});