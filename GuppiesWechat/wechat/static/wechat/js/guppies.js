$(function(){

    // 图片预览
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $('#blah').attr('src', e.target.result);
            };

            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#imgInp").change(function(){
        readURL(this);
        $('.alertBox1').show();
        $('body').css('overflow','hidden');
        // qiniu_upload(this);
    });

    // 确认开晒
    $(document).on('click','#imgCut1',function(){

        $('.alertBox1').hide();
        $('.alertBox2').show();
        $('body').css('overflow','hidden');

    });

    $(document).on('click','#imgCut2',function(){

        $('.alertBox2').hide();
        $('body').css('overflow','auto');

    });

    var is_positioned = sessionStorage.getItem('is_positioned');
    console.log('is_positioned:', is_positioned);
    if(!is_positioned) {
        console.log('start to get position');
        navigator.geolocation.getCurrentPosition(function(position) {
            console.log('location:', position);
            var data = {
                latitude: position.coords.latitude,
                longitude: position.coords.longitude
            };
            $.ajax({
                method: 'post',
                url: '/wechat/api/position',
                contentType: 'application/json',
                data: JSON.stringify(data),
                success: function (data) {
                    sessionStorage.setItem('is_positioned', true);
                    console.log('position success:', data);
                }
            });
        }, function (err) {
            console.warn('ERROR(' + err.code + '): ' + err.message);
        });
    }

    // 点击截图，跳转下一个页面
    $('.modal .button').click(function(){

        $(this).parents(".modal").hide();

        $(".imgSure").show();

        var imgSrc = $('#currentUploadImage').attr('src');

        console.log(imgSrc);

        $("#lastDiv").before('<div class="imgNum"><img src="' + imgSrc +  '"></div>');

        var imgNum = $(".imgNum").length;

        if(imgNum == 4){
            $('#lastDiv').hide();
        }

    });
    //
    $(".classInput").change(function(){
        var success = function (url) {
            console.log('upload success:', url);
            $('#currentUploadImage').attr('src', url + '?imageView2/1/w/750/h/750');
            $(".imgSure").hide();
            $(".modal").show();
        };

        qiniu_upload(this, success, function () {
            console.log('取消上传');
            $(".container").show();
        });
        $(".container").hide();
    });

    $("#imgSureButton").click(function () {
        var text = $("#imgSureText").val();
        var url = [];
        $('.imgNum img').each(function() {
            url.push($(this).attr('src'));
        });

        var data = {
            'description': text,
            'url': url
        };

        $.ajax({
            method: 'POST',
            contentType: 'application/json',
            url: '/wechat/api/photos',
            data: JSON.stringify(data),
            success: function (data) {
                console.log('success', data);
            },
            error: function (data) {
                alert('提交失败' + data);
            }
        });
    });


    //// 获取头像
    //$.ajax({
    //    method:'get',
    //    url:'/wechat/api/photos',
    //    success:function(data){
    //        console.log(data);
    //        for(var i = 0; i < data.results.length; i++) {
    //            var imgUrl = data.results[i].user.avatar_url;
    //            var uerName = data.results[i].user.nickname;
    //            var imgInfo = data.results[i].description;
    //            var fishImg = data.results[i].url;
    //            var getWatch = data.results[i].n_total_watched;
    //            var getGood = data.results[i].n_account_vote;
    //            var getScore = data.results[i].n_total_mark ;
    //
    //            var html = $('<div class="user">' +
    //                '    <a href="#">' +
    //                '        <div class="borderColor"></div>' +
    //                '        <div class="userInfo">' +
    //                '            <div class="userImg"><img src="' + imgUrl + '"/></div>' +
    //                '            <span class="userName">' + uerName + '</span>' +
    //                '            <span class="userTime">1分钟前</span>' +
    //                '            <div class="userText">' + imgInfo + '</div>' +
    //                '        </div>' +
    //                '        <div class="guppiesImg">' +
    //                '            <img src="' + fishImg + '"/>' +
    //                '        </div>' +
    //                '        <div class="score">' +
    //                '            <span>查看&nbsp;<em>' + getWatch + '</em></span>' +
    //                '            <span>点赞&nbsp;<em>' + getGood + '</em></span>' +
    //                '            <span>评分&nbsp;<em class="fontColor">' + getScore + '</em></span>' +
    //                '        </div>' +
    //                '    </a>' +
    //                '</div>');
    //
    //            $('.doc').append(html);
    //        }
    //
    //    }
    //
    //});

});
