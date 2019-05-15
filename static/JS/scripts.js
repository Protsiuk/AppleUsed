/**
 * add to favorite.
 */
$(document).ready(function () {
    var favorite_obj = $('.favorite-item');
    favorite_obj.on('click', function (e){
        e.preventDefault();
        var obj_data = $('#favorite');
        var favoriteUrl = obj_data.attr('data-href-template');

        // var data = {};
        // var csrf_token = $('csrf_getting_form[name="csrfmiddlewatoken"]').val();

        $.ajax({
            url:favoriteUrl,
            method:'GET',
            // data:{pk:ad_id},
            dataType: 'json',
            // cache:'True',
            success:function (data){
                var url_favorite = data.url_favorite_icon;
                var img = $('#favorite').find('img');
                img.attr('src', url_favorite);
                var set_url = img.attr('src', url_favorite);
                // console.log(set_url);
                console.log('ok');
            }
        });

    });

});



 // $.ajax({
 //                type: 'GET',
 //                async: true,
 //                url: '/ajax/',
 //                data: "param1=value1&param2=value2;",
 //                success: function(data) {
 //                    $("#more-text-here1").append(data['first-text']);
 //                    $("#more-text-here2").append(data['second-text']);
 //
 //                },
 //                dataType: 'json',

$(document).ready(function () {
    var favorite_obj = $('.favorite-item');
    favorite_obj.on('click', function (e){
        e.preventDefault();
        var obj_data = $('#favorite');
        var favoriteUrl = obj_data.attr('data-href-template');

        // var data = {};
        // var csrf_token = $('csrf_getting_form[name="csrfmiddlewatoken"]').val();

        $.ajax({
            url:favoriteUrl,
            method:'GET',
            // data:{pk:ad_id},
            dataType: 'json',
            // cache:'True',
            success:function (data){
                var url_favorite = data.url_favorite_icon;
                var img = $('#favorite').find('img');
                img.attr('src', url_favorite);
                var set_url = img.attr('src', url_favorite);
                // console.log(set_url);
                console.log('ok');
            }
        });

    });

});