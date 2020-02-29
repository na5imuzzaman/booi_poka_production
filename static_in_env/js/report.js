$('.accordian-body').on('show.bs.collapse',
    function () {
        $(this).closest("table")
            .find(".collapse.in")
            .not(this)
            .collapse('toggle')
    });


$(function () {
    $('#myTab li:last-child a').tab('show')
});
