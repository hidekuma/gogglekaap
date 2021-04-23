/*Reset Searching trigger*/
const $searching = $('#searching');
const $searchBox = $('#searchBox');
$searchBox.find('.cancel').on('click', function(){
  $searching.val('').trigger('change');
});

/*SideMenu*/
const $sidemenu = $('#sidemenu');
const $menu = $('#menu');
$menu.on('click', function (){
  $sidemenu.toggleClass('inactive')
});

/*SideMenu Btns*/
$(document).on('click', '#sidemenu > .sidemenu-btn', function(){
  $sidemenu.removeClass('inactive');
  $(this).addClass('active');
  $(this).siblings().removeClass('active');

  if ($(this).hasClass('sidemenu-btn-memo')) {
    $('#content').removeClass('inactive');
  } else {
    $('#content').addClass('inactive');
  }
});