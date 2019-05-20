/**
 * add to favorite.
 */
$(document).ready(function () {
    var favorite_obj = $('.favorite-item');
    favorite_obj.on('click', function (e){
        e.preventDefault();
        var obj_data = $('#favorite');
        var favoriteUrl = obj_data.attr('data-href-template');
        $.ajax({
            url:favoriteUrl,
            method:'GET',
            // data:{pk:ad_id},
            dataType: 'json',
            // cache:'True',ok
            success:function (data){
                var url_favorite = data.url_favorite_icon;
                var img = $('#favorite').find('img');
                img.attr('src', url_favorite);
                var set_url = img.attr('src', url_favorite);
                console.log('ok');
            }
        });

    });

});
