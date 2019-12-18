
$('.permission-area .parent').click(function () {

 // fa-caret-right
    $(this).find('.xx').toggleClass('fa-caret-right');
    $(this).nextUntil('.parent').toggleClass('hidden');

});











