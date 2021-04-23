/*Init Masonry*/
$CONTAINER = $('#container');
const $GRID = $CONTAINER.masonry({
  // 아이템
  itemSelector: '.item',
  columnWidth: '.sizer',
  percentPosition: true,
  // 좌우여백, 상하여백은 CSS로 해줘야함
  gutter: 15,
  // 순서대로 배치
  horizontalOrder: true,
  // CSS로 정의해줘야 버그가 없음, 두번 리로드되는현상
  transitionDuration: 0
  });

/*MEMO */
const MEMO = (function(){
  // 추가 조회 상태
  // 더 조회할 데이터 없음 = false
  let STATUS = true;
  // 조회 페이지
  let PAGE = 0;
  // 검색어
  let NEEDLE = null;
  // 삭제된 메모 검색 여부
  // true = 삭제된 메모, false = 삭제되지 않은 메모
  let IS_DELETED = false;
  // 조회할 라벨
  let LABEL = null;
  // 라벨 데이터 메모리에 저장
  let MEMORY_LABELS = [];

  /* 셀럭터 */
  const $modalEdit = $('#modalEdit');
  const $modalTitle = $modalEdit.find('.modal-title');
  const $modalContent = $modalEdit.find('.modal-content');
  const $modalClose = $modalEdit.find('.modal-close');
  const $modalMedia = $modalEdit.find('.modal-media');
  const $modalFile = $modalEdit.find('.modal-file');
  const $modalModified = $modalEdit.find('.modal-modified');
  const $content = $('#content');
  const $layout = $('.mdl-layout__content');
  const $customActions = $('#customActions');

  /* 검색 파라미터 */
  const _getParams = function(){
    return {
      status: STATUS,
      page: PAGE,
      needle: NEEDLE,
      label: LABEL,
      is_deleted: IS_DELETED
    }
  };

  /* 모든 메모 제거 시, 그리드 비우기 */
  const _removeAllMemos = function(){
    const elems = $GRID.masonry('getItemElements');
    $GRID.masonry('remove', elems);
  };

  /*그리드 다시 재적용*/
  const _resetGridLayout = function (){
    const imageLength = $CONTAINER.find("img").length;
    if (imageLength >= 1) {
      $GRID.imagesLoaded().progress(function(){
        $GRID.masonry('layout');
      });
    } else {
      $GRID.masonry('layout');
    }
    if(typeof componentHandler != 'undefined') {
      // NOTE: MDL 컴포넌트 재활성화
      // 동적생성된 MDL 컴포넌트들이 정상동작 안할경우가 있기 때문
      componentHandler.upgradeDom();
    }
  };

  /* 편집 팝업 필드 초기화 */
  const resetModalFields = function(resetLayout){
    $modalTitle.val('');
    $modalContent.val('');
    $modalFile.val('');
    $modalMedia.html('');
    $modalClose.removeAttr('data-id');
    $modalContent.trigger('keyup');
    $modalModified.val(0);
    if (resetLayout) {
      _resetGridLayout();
    }
  };

  /* 메뉴 라벨 li 태그 생성 */
  const _makeLabelMenuHtml = function(el){
    let labelHtml = '';
    labelHtml += '<li class="item-label-li" onclick="event.stopPropagation();">';
    labelHtml += '<label><input type="checkbox" value="' + el.content + '">' + el.content + '</label>'
    labelHtml += '</li>';
    return labelHtml;
  }

  /* 사이즈 바 메뉴 button 태그 생성 */
  const _makeLabelBtnHtml = function(el){
    let labelHtml = '';
    labelHtml += '<button class="sidemenu-btn mdl-button mdl-js-button" onclick="MEMO.getMemosByLabel(' + el.id + ')">';
    labelHtml += '<span class="sidemenu-icon material-icons-outlined">';
    labelHtml += 'label';
    labelHtml += '</span>';
    labelHtml += '<span class="sidemenu-title">';
    labelHtml += el.content;
    labelHtml += '<span class="sidemenu-label-del-btn material-icons" onclick="MEMO.deleteLabel(event, ' + el.id + ')">';
    labelHtml += 'clear';
    labelHtml += '</span>';
    labelHtml += '</span>';
    labelHtml += '</button>';
    return labelHtml;
  }

  /* 라벨 칩 span 태그 생성 */
  const _makeLabelChipHtml = function(el){
    let labelHtml = '';
    $.each(el.labels, function(_, label){
      labelHtml += '<span class="mdl-chip" data-label-id=' + label.id + '>';
      labelHtml += '<span class="mdl-chip__text">' + label.content + '</span>';
      labelHtml += '</span>';
    });
    return labelHtml;
  }

  /* 가운데 메모 컨텐츠 태그 생성 */
  const _makeMemoHtml = function(el){
    let itemHtml = '';
    itemHtml += '<div id="item' + el.id + '" class="item mdl-card" data-id="' + el.id + '">';
    itemHtml += '<div class="modal-run mdl-card__title">';
    itemHtml += '<h2 class="item-title mdl-card__title-text">' + el.title + '</h2>';
    itemHtml += '</div>';
    itemHtml += '<div class="item-media modal-run mdl-card__media">';
    if (el.linked_image) itemHtml += '<img src="' + el.linked_image + '" alt=""/>';
    itemHtml += '</div>';
    itemHtml += '<div class="item-content modal-run mdl-card__supporting-text">';
    itemHtml += el.content;
    itemHtml += '</div>';
    itemHtml += '<div class="item-chip modal-run">';
    itemHtml += _makeLabelChipHtml(el);
    itemHtml += '</div>';
    itemHtml += '<div class="mdl-card__actions mdl-card--border">';
    itemHtml += '<button id="itemLabelBtn' + el.id + '" class="mdl-button mdl-button--icon mdl-js-button mdl-js-ripple-effect" onclick="MEMO.getLabelsForMenu(event, ' + el.id + ');">';
    itemHtml += '<i class="material-icons-outlined">label</i>';
    itemHtml += '</button>';
    itemHtml += '<ul class="item-labels mdl-menu mdl-menu--top-left mdl-js-menu mdl-js-ripple-effect" data-mdl-for="itemLabelBtn' + el.id + '">';
    itemHtml += '<li class="mdl-menu__item" onclick="MEMO.attachLabels(' + el.id + ');"><b>저장</b></li>';
    itemHtml += '<li class="mdl-menu__item" onclick="">닫기</li>';
    itemHtml += '</ul>';
    itemHtml += '<button class="mdl-button mdl-button--icon mdl-js-button mdl-js-ripple-effect" onclick="MEMO.detachImage(event, ' + el.id + ');">';
    itemHtml += '<i class="material-icons-outlined">layers_clear</i>';
    itemHtml += '</button>';
    itemHtml += '</div>';
    itemHtml += '<div class="mdl-card__menu">';
    if (IS_DELETED){
      itemHtml += '<button class="mdl-button mdl-button--icon mdl-js-button mdl-js-ripple-effect" onclick="MEMO.reviveMemo(event, '+ el.id + ')">';
      itemHtml += '<i class="material-icons-outlined">undo</i>';
      itemHtml += '</button>';
    } else {
      itemHtml += '<button class="mdl-button mdl-button--icon mdl-js-button mdl-js-ripple-effect" onclick="MEMO.deleteMemo(event, '+ el.id + ')">';
      itemHtml += '<i class="material-icons-outlined">clear</i>';
      itemHtml += '</button>';
    }
    itemHtml += '</div>';
    itemHtml += '</div>';
    return itemHtml;
  };

  /*추가 데이터 없음 아이템 태그*/
  const _makeNoMoreItemHtml = function(){
    let html = '';
    html += '<div class="item item-full">';
    html += '<span class="sidemenu-icon material-icons-outlined">';
    html += 'info';
    html += '<span> 추가 로드할 데이터 없음</span>'
    html += '</span>';
    html += '</div>';
    return html;
  }

  /*추가 데이터 로드 아이템 태그*/
  const _makeMoreItemHtml = function(){
    let html = '';
    html += '<div class="item item-full" onclick="MEMO.getMemos(this);">';
    html += '<span class="sidemenu-icon material-icons-outlined">';
    html += 'hourglass_top';
    html += '<span> 추가 로드하기</span>'
    html += '</span>';
    html += '</div>';
    return html;
  }

  /* 메모 생성 */
  const createMemo = function(){
    /* POST /api/memos */

    const form = $modalEdit[0];
    const data = new FormData(form);
    let submitFlag = false;
    for (var [key, value] of data.entries()) {
      if (key == 'title' || key == 'content') {
        if (value) submitFlag = true;
      }
    }
    if (submitFlag) {
      console.log('createMemo');
      // TODO
      // 1) 폼 기반 호출: AJAX -> form, multipart
      // 2) 조회한 메모 데이터 생성: _makeMemoHtml
      // 3) 컨테이너에 추가: prepend to grid
      // 4) 에러 얼럿 노출: error e.responseText
      // 5) 모달 리셋: done - resetModalFields(true)
    }
  };

  /* 메모 복수 조회 */
  const getMemos = function(el){
    /* GET /api/memos */

    if (el) $GRID.masonry('remove', $(el));

    if (STATUS) {
      PAGE += 1;
      data = _getParams();
      console.log('getMemos')
      // TODO
      // 1) 로딩아이콘 토글링: beforeSend - toggle loading icon
      // 2) 조회한 메모 데이터 생성: loop _makeMemoHtml
      // 3) 컨테이너에 추가: append to grid
      // 4) 에러 얼럿 노출 및 추가 조회 스테이터스 업데이트: error e.responseText, set status
      // 5) 에러시 추가데이터 없을경우 인포 아이템 추가: append no more item
      // 6) 완료시, 로딩아이콘 토글링: complete - toggle loading icon with setTimeout
      // 5) 그리드 리셋: done - _resetGridLayout()
    }
  };



  /* 메모 조회 */
  const getMemo = function(id){
    /* GET /api/memos/{id} */

    console.log('getMemo', id);
    // TODO
    // 1) 모달 필드를 리셋해준다: beforeSend - resetModalFields
    // 2) 조회한 데이터로 모달 필드를 반영하고, 텍스트 에리어를 트리거링 한다
  };

  /* 메모 삭제 */
  const deleteMemo = function(e, id){
    /* PUT /api/memos/{id} */

    e.preventDefault();
    console.log('deleteMemo', id);
    // TODO
    // 1) 컨테이너 아이템 삭제
    // 2) 그리드에 반영
    // 3) 에러시 얼럿
    // 4) 그리드 리셋: done - _resetGridLayout or masonry.layout
  };


  /* 메모 업데이트 */
  const updateMemo = function(id){
    /* PUT /api/memos/{id} */

    const form = $modalEdit[0];

    const $item = $('#item' + id);
    const $title = $item.find('.item-title');
    const $content = $item.find('.item-content');
    const $media = $item.find('.item-media');
    const data = new FormData(form);

    console.log('updateMemo');
    if ($modalModified.val() == 1) {
      // TODO
      // 1) AJAX form
      // 2) 업데이트 데이터 전송
      // 3) 리턴값 메모 아이템에 반영
      // 4) 에러 노출
      // 5) 완료시 모달리셋: done - resetModalFields(true)
    }
  };

  /* 메모 되살리기 */
  const reviveMemo = function(e, id){
    /* PUT delete /api/memos/{id} */

    e.preventDefault();

    const data = {
      'is_deleted': false
    }

    console.log('reviveMemo', id);
    // TODO
    // 1) 업데이트 데이터 전송
    // 2) 메모 아이템 화면에서 제거
    // 4) 에러 노출
    // 5) 완료시 그리드 리셋과 추가조회: done - _resetGridLayout()
  };

  /* 이미지 제거 */
  const detachImage = function(e, id){
    /* DELETE /api/memos/{id} */

    e.preventDefault();
    const $media = $('.item[data-id="' + id + '"]').find('.item-media');
    console.log('detachImage', id);
    if (id && $media.find('img').length > 0){
      // TODO
      // 1) 메모 이미지 삭제 요청
      // 2) 메모 아이템에 메모삭제
      // 3) 에러시 얼럿노출
      // 4) 완료시 모달 리셋: resetModalFields(true);
    }
  }

  /* 라벨 복수 조회 */
  const getLabels = function(){
    /*  GET /api/labels */

    console.log('getLabels');
    // TODO
    // 1) 라벨 조회
    // 2) 라벨 버튼 생성: loop _makeLabelBtnHtml
    // 3) (!) 메모 버튼 뒤에 삽입
    // 4) 메모리에 라벨 데이터 저장
    // 5) 에러시 얼럿 노출
  }

  /* 라벨 생성 */
  const addLabel = function(e){
    /* POST /api/labels */

    e.preventDefault();
    $input = $(e.target);
    const val = $input.val();
    if (val != '') {
      console.log('addLabel');
      // TODO
      // 1) 라벨 추가
      // 2) 라벨 버튼 생성: _makeLabelBtnHtml
      // 3) 라벨 추가 버튼 앞에 삽입
      // 4) 인풋 초기화
      // 5) 메모리에 라벨 추가
      // 6) 에러시 얼럿 노출
    }
  }

  /* 라벨 삭제 */
  const deleteLabel = function (e, id){
    /* DELETE /api/labels/{id} */

    e.stopPropagation();
    c = confirm('라벨을 정말 삭제하시겠습니까?')
    if (!c) return false;

    console.log('deleteLabel', id);
    // TODO
    // 1) 라벨 삭제
    // 2) 라벨 메뉴 아이템 삭제
    // 3) 라벨 칩 삭제
    // 4) 메모리 라벨 팝
    // 5) 에러시 얼럿노출
    // 6) 완료시 그리드 리셋: done - _resetGridLayout()
  }

  /* 메모에 라벨 적용 */
  const attachLabels = function(id){
    /* *  PUT /api/memos/{id} * */

    const $item = $('#item' + id);
    const labels = [];
    $item.find('.item-labels').find('input[type="checkbox"]:checked').each(function(_, item){
      labels.push($(item).val());
    });

    console.log('attachLabels', id);
    // TODO
    // 1) 메모 업데이트 호출
    // 2) 라벨 데이터 콤마 스트링처리
    // 3) 라벨 칩 태그 생성 _makeLabelChipHtml
    // 4) 메모 아이템에 라벨 칩 추가
    // 5) 에러시 얼럿 노출
    // 6) 완료 시 그리드 리셋: _resetGridLayout()
  }

  /* 메모 검색 조회 */
  const getMemosByNeedle = function(needle){
    STATUS = true;
    PAGE = 0;
    NEEDLE = needle;
    _removeAllMemos();
    getMemos();
  };

  /* 메모 라벨로 조회 */
  const getMemosByLabel = function(labelId){
    STATUS = true;
    PAGE = 0;
    LABEL = labelId;
    IS_DELETED = false;
    _removeAllMemos();
    getMemos();
  }

  /* 메모 init */
  const init = function (){
    getLabels();
    getMemos();
  };

  /* 삭제된 메모 조회 */
  const getDeletedMemos = function(){
    STATUS = true;
    PAGE = 0;
    IS_DELETED = true;
    LABEL = null;
    _removeAllMemos();
    getMemos();
  }

  /* 기본 메모 조회 */
  const refreshMemos = function(){
    STATUS = true;
    PAGE = 0;
    IS_DELETED = false;
    LABEL = null;
    _removeAllMemos();
    getMemos();
  }

  /* 팝업 라벨 메뉴 */
  const getLabelsForMenu = function(e, memo_id){
    e.preventDefault();
    let html = '';
    $.each(MEMORY_LABELS, function (_, el){
      html += _makeLabelMenuHtml(el);
    });
    $itemLabels = $('#item' + memo_id);
    $itemLabels.find('.item-label-li').remove()
    $itemLabels.find('.item-labels').prepend(html);
  }

  return {
    'getMemo': getMemo,
    'getMemos': getMemos,
    'getMemosByLabel': getMemosByLabel,
    'getLabels': getLabels,
    'getLabelsForMenu': getLabelsForMenu,
    'getDeletedMemos': getDeletedMemos,
    'getMemosByNeedle': getMemosByNeedle,
    'refreshMemos': refreshMemos,
    'deleteMemo': deleteMemo,
    'reviveMemo': reviveMemo,
    'updateMemo': updateMemo,
    'createMemo': createMemo,
    'resetModalFields': resetModalFields,
    'detachImage': detachImage,
    'attachLabels': attachLabels,
    'deleteLabel': deleteLabel,
    'addLabel': addLabel,
    'init': init
  }
})();
