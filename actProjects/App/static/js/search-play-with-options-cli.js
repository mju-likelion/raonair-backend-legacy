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