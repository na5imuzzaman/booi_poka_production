// $(document).on('submit', '#reportbookform', function (e) {
//     console.alert('console alert')
//     e.preventDefault();
//
//
//     $.ajax({
//         type: 'POST',
//         url: $('reportbookform').attr('action'),
//         data: {
//             action: 'hahaha',//$('#reportbook').val(),
//             csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
//         },
//         // dataType: 'json',
//         success: function () {
//             alert('token');
//         },
//         fail: function (xhr, textStatus, errorThrown) {
//             alert('request failed');
//         }
//     });
// });

$('#all_book').click(function () {
    $('input[name="filter"]').val('all-book');
    $('#search').submit();
});

$('#my_books').click(function () {
    $('input[name="filter"]').val('my-books');
    $('#search').submit();
});

$('#pending-books').click(function () {
    $('input[name="filter"]').val('pending-books');
    $('#search').submit();
});
$('#deactive-books').click(function () {
    $('input[name="filter"]').val('deactivated-books');
    $('#search').submit();
});

// search by category

$('#academic').click(function () {
    $('input[name="filter"]').val('academic');
    $('#search').submit();
});

$('#biography').click(function () {
    $('input[name="filter"]').val('biography');
    $('#search').submit();
});

$('#inspiration').click(function () {
    $('input[name="filter"]').val('inspiration');
    $('#search').submit();
});

$('#islamic').click(function () {
    $('input[name="filter"]').val('islamic');
    $('#search').submit();
});

$('#magazine').click(function () {
    $('input[name="filter"]').val('magazine');
    $('#search').submit();
});

$('#mathematics').click(function () {
    $('input[name="filter"]').val('mathematics');
    $('#search').submit();
});

$('#novel').click(function () {
    $('input[name="filter"]').val('novel');
    $('#search').submit();
});

$('#poem').click(function () {
    $('input[name="filter"]').val('poem');
    $('#search').submit();
});

$('#programming').click(function () {
    $('input[name="filter"]').val('programming');
    $('#search').submit();
});

$('#science_fiction').click(function () {
    $('input[name="filter"]').val('science_fiction');
    $('#search').submit();
});

$('#foreign').click(function () {
    $('input[name="filter"]').val('foreign');
    $('#search').submit();
});

$('#translation').click(function () {
    $('input[name="filter"]').val('translation');
    $('#search').submit();
});

$('#all-notification').click(function () {
    $('#clear_notification_form').submit();
});


$('#academic_side').click(function () {
    $('input[name="filter"]').val('academic');
    $('#search_side').submit();
});

$('#biography_side').click(function () {
    $('input[name="filter"]').val('biography');
    $('#search_side').submit();
});

$('#inspiration_side').click(function () {
    $('input[name="filter"]').val('inspiration');
    $('#search_side').submit();
});

$('#islamic_side').click(function () {
    $('input[name="filter"]').val('islamic');
    $('#search_side').submit();
});

$('#magazine_side').click(function () {
    $('input[name="filter"]').val('magazine');
    $('#search_side').submit();
});

$('#mathematics_side').click(function () {
    $('input[name="filter"]').val('mathematics');
    $('#search_side').submit();
});

$('#novel_side').click(function () {
    $('input[name="filter"]').val('novel');
    $('#search_side').submit();
});

$('#poem_side').click(function () {
    $('input[name="filter"]').val('poem');
    $('#search_side').submit();
});

$('#programming_side').click(function () {
    $('input[name="filter"]').val('programming');
    $('#search_side').submit();
});

$('#science_fiction_side').click(function () {
    $('input[name="filter"]').val('science_fiction');
    $('#search_side').submit();
});

$('#foreign_side').click(function () {
    $('input[name="filter"]').val('foreign');
    $('#search').submit();
});

$('#translation_side').click(function () {
    $('input[name="filter"]').val('translation');
    $('#search').submit();
});


$('#review-pending-books').click(function () {
    $('input[name="filter"]').val('review-pending-books');
    $('#admin-panel').submit()
});

$('#review-delete-request').click(function () {
    $('input[name="filter"]').val('review-delete-request');
    $('#admin-panel').submit()
});

$('#search_btn').click(function () {
    $('#search_mini_form').submit()
});


// $('#all_book_phn').bind('touchstart', function () {
//     $('input[name="filter"]').val('all-book');
//     $('#searchphn').submit();
// });
//
// $('#my_books_phn').bind('touchstart', function () {
//     $('input[name="filter"]').val('my-books');
//     $('#searchphn').submit();
// });
//
// $('#borrowed_by_me_phn').bind('touchstart', function () {
//     $('input[name="filter"]').val('borrowed-by-me');
//     $('#searchphn').submit();
// });

// $('#all_book_phn').ontouchstart(function () {
//     $('input[name="filter"]').val('all-book');
//     $('#searchphn').submit();
// });
//
// $('#my_books_phn').ontouchstart(function () {
//     $('input[name="filter"]').val('my-books');
//     $('#searchphn').submit();
// });
//
// $('#borrowed_by_me_phn').ontouchstart(function () {
//     $('input[name="filter"]').val('borrowed-by-me');
//     $('#searchphn').submit();
// });
