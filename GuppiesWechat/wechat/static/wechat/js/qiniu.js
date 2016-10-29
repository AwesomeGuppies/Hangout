/*
 *   本示例演示七牛云存储表单上传
 *
 *   按照以下的步骤运行示例：
 *
 *   1. 填写token。需要您不知道如何生成token，可以点击右侧的链接生成，然后将结果复制粘贴过来。
 *   2. 填写key。如果您在生成token的过程中指定了key，则将其输入至此。否则留空。
 *   3. 姓名是一个自定义的变量，如果生成token的过程中指定了returnUrl和returnBody，
 *      并且returnBody中指定了期望返回此字段，则七牛会将其返回给returnUrl对应的业务服务器。
 *      callbackBody亦然。
 *   4. 选择任意一张照片，然后点击提交即可
 *
 *   实际开发中，您可以通过后端开发语言动态生成这个表单，将token的hidden属性设置为true并对其进行赋值。
 *
 *  **********************************************************************************
 *  * 贡献代码：
 *  * 1. git clone git@github.com:icattlecoder/jsfiddle
 *  * 2. push代码到您的github库
 *  * 3. 测试效果，访问 http://jsfiddle.net/gh/get/jquery/1.9.1/<Your GitHub Name>/jsfiddle/tree/master/ajaxupload
 *  * 4. 提pr
 *   **********************************************************************************
 */
var Qiniu_UploadUrl = "http://up.qiniu.com";

var qiniu_upload = function (img_input) {
    //普通上传
    var Qiniu_upload = function (f, token, key, success_callback) {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', Qiniu_UploadUrl, true);
        var formData, startDate;
        formData = new FormData();
        if (key !== null && key !== undefined) formData.append('key', key);
        formData.append('token', token);
        formData.append('file', f);

        xhr.onreadystatechange = function (response) {
            if (xhr.readyState == 4 && xhr.status == 200 && xhr.responseText != "") {
                var blkRet = JSON.parse(xhr.responseText);
                console && console.log(blkRet);
                success_callback();
            } else if (xhr.status != 200 && xhr.responseText) {
                alert('上传图片失败!');
            }
        };
        startDate = new Date().getTime();
        $("#progressbar").show();
        xhr.send(formData);
    };

    $.ajax({
        method: 'POST',
        url: '/wechat/api/uploader',
        success: function (data) {
            var token = data.token;
            var files = img_input.files;
            var key = data.key;
            var url = data.url;

            if (files.length > 0) {
                Qiniu_upload(files[0], token, key, function () {
                    console.log('upload success');
                    $('#photo_url').val(url);
                });

            } else {
                alert('请选择图片!');
            }
        }
    });

};
