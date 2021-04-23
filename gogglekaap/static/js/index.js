/*============= LOAD ==============*/

const $modal = $('#modalEdit');

/*Load Memos*/
MEMO.init()

/*Searching trigger*/
let timer, delay = 500;
$searching.bind('change', function() {
  const $this = $(this);
  clearTimeout(timer);
  timer = setTimeout(
    function() {
      MEMO.getMemosByNeedle($this.val());
    },
    delay
  );
});

/*Dialog Modal*/
const dialog = document.querySelector('.mdl-dialog');
const activeClass = 'item--active'

if (! dialog.showModal) {
  dialogPolyfill.registerDialog(dialog);
}

/*Modal close*/
dialog.querySelector('.modal-close').addEventListener('click', function(e) {
  e.preventDefault();
  $('#container').find('.item.item--active').removeClass(activeClass);

  const id = $modal.find('.modal-close').attr('data-id');

  if (typeof id == undefined) return false;
  else if (id == 'create') MEMO.createMemo();
  else MEMO.updateMemo(id);

  dialog.close();
});

/*Grid item click*/
$(document).on('click', '#container .modal-run', function(e) {
  const $this = $(this);
  const memoId = $(e.target).closest('.item').data('id');
  if (memoId) {
    MEMO.getMemo(memoId);

    $this.parent().toggleClass(activeClass);
    $this.parent().siblings().removeClass(activeClass)

    dialog.showModal();
  }
});

/*Create modal*/
$(document).on('click', '#controller', function() {
  MEMO.resetModalFields();
  $modal.find('.modal-close').attr('data-id', 'create');
  dialog.showModal();
});

/*Modal textarea resizing*/
$("#modalEdit .modal-content").on('focus keydown keyup', function () {
  $(this).height(1).height( $(this).prop('scrollHeight')+12 );	
});

/*Input file Viewer*/
function readInputFile(input) {
  if(input.files && input.files[0]) {
    const reader = new FileReader();
    reader.onload = function (e) {
      const ihtml = '<img src="' + e.target.result + '" alt=""/>';
      $(input).closest('form').find('.modal-media').html(ihtml);
    }
    reader.readAsDataURL(input.files[0]);
  }
}

$('#modalEdit').find('input, textarea').on('keydown change', function(){
  $('#modalEdit').find('.modal-modified').val(1);
});