/**
 * Created by zhuzhengyang on 2019/6/1.
 */

accessid = ''
accesskey = ''
host = ''
policyBase64 = ''
signature = ''
callbackbody = ''
filename = ''
key = ''
expire = 0
g_object_name = ''
g_object_name_type = 'local_name'
now = timestamp = Date.parse(new Date()) / 1000;

function send_request()
{
    var xmlhttp = null;
    if (window.XMLHttpRequest)
    {
        xmlhttp=new XMLHttpRequest();
    }
    else if (window.ActiveXObject)
    {
        xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }

    if (xmlhttp!=null)
    {
        serverUrl = '/common/aliyun'
        xmlhttp.open( "GET", serverUrl, false );
        xmlhttp.send( null );
        return xmlhttp.responseText
    }
    else
    {
        alert("Your browser does not support XMLHTTP.");
    }
};



function get_signature()
{
    //可以判断当前expire是否超过了当前时间,如果超过了当前时间,就重新取一下.3s 做为缓冲
    now = timestamp = Date.parse(new Date()) / 1000;
    if (expire < now + 3)
    {
        body = send_request()
        var obj = eval ("(" + body + ")");
        host = obj['host']
        policyBase64 = obj['policy']
        accessid = obj['accessid']
        signature = obj['signature']
        expire = parseInt(obj['expire'])
        callbackbody = obj['callback']
        key = obj['dir']
        return true;
    }
    return false;
};

function random_string(len) {
　　len = len || 32;
　　var chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678';
　　var maxPos = chars.length;
　　var pwd = '';
　　for (i = 0; i < len; i++) {
    　　pwd += chars.charAt(Math.floor(Math.random() * maxPos));
    }
    return pwd;
}

function get_suffix(filename) {
    pos = filename.lastIndexOf('.')
    suffix = ''
    if (pos != -1) {
        suffix = filename.substring(pos)
    }
    return suffix;
}

function calculate_object_name(filename)
{
    if (g_object_name_type == 'local_name')
    {
        g_object_name += "${filename}"
    }
    else if (g_object_name_type == 'random_name')
    {
        suffix = get_suffix(filename)
        g_object_name = key + random_string(10) + suffix
    }
    return ''
}

function get_uploaded_object_name(filename)
{
    if (g_object_name_type == 'local_name')
    {
        tmp_name = g_object_name
        tmp_name = tmp_name.replace("${filename}", filename);
        return tmp_name
    }
    else if(g_object_name_type == 'random_name')
    {
        return g_object_name
    }
}

function set_upload_param(up, filename, ret)
{
    if (ret == false)
    {
        ret = get_signature()
    }
    g_object_name = key;
    if (filename != '') {
        suffix = get_suffix(filename)
        calculate_object_name(filename)
    }
    new_multipart_params = {
        'key' : g_object_name,
        'policy': policyBase64,
        'OSSAccessKeyId': accessid,
        'success_action_status' : '200', //让服务端返回200,不然，默认会返回204
        'callback' : callbackbody,
        'signature': signature,
    };

    up.setOption({
        'url': host,
        'multipart_params': new_multipart_params
    });

    up.start();
}

var uploader = new plupload.Uploader({
	runtimes : 'html5,flash,silverlight,html4',
	browse_button : 'selectfiles',
    //multi_selection: false,
	container: document.getElementById('container'),
    url : 'http://oss.aliyuncs.com',

    filters: {
        mime_types : [ //只允许上传图片
        { title : "Image files", extensions : "jpg,gif,png,bmp" }
        ],
        max_file_size : '5mb', //最大只能上传5mb的文件
        prevent_duplicates : false //允许选取重复文件
    },

	init: {
		PostInit: function() {
			document.getElementById('ossfile').innerHTML = '';
			document.getElementById('postfiles').onclick = function() {
            set_upload_param(uploader, '', false);
            return false;
			};
		},

		FilesAdded: function(up, files) {
			plupload.each(files, function(file) {
				document.getElementById('ossfile').innerHTML = '<b></b>';
				document.getElementsByClassName('progress-bar')[0].style.width = "0%";
				document.getElementById('img-url').value = file.name + ' (' + plupload.formatSize(file.size) + ')';
			});
		},

		BeforeUpload: function(up, file) {
            set_upload_param(up, file.name, true);
        },

		UploadProgress: function(up, file) {
			var d = document.getElementById('ossfile');
			d.getElementsByTagName('b')[0].innerHTML = '<span>' + file.percent + "%</span>";
            var prog = document.getElementsByClassName('progress')[0];
			var progBar = prog.getElementsByTagName('span')[0]
			progBar.style.width= file.percent+'%';
			progBar.setAttribute('aria-valuenow', file.percent);
		},

		FileUploaded: function(up, file, info) {
            if (info.status == 200)
            {
                document.getElementById('ossfile').getElementsByTagName('b')[0].getElementsByTagName('span')[0].innerHTML = '图片上传成功:' + get_uploaded_object_name(file.name);
                document.getElementById('img-url').value = "https://flaskdemo.oss-cn-hangzhou.aliyuncs.com/" + get_uploaded_object_name(file.name) + "?x-oss-process=style/format_size";
            }
            else
            {
                document.getElementById('ossfile').getElementsByTagName('b')[0].innerHTML = info.response;
            }
		},

		Error: function(up, err) {
            if (err.code == -600) {
                document.getElementById('ossfile').innerHTML = "选择的图片不能超过5M";
            }
            else if (err.code == -601) {
                document.getElementById('ossfile').innerHTML = "选择的图片后缀不对,支持格式(jpg,gif,png,bmp)";
            }
            else if (err.code == -602) {
                document.getElementById('ossfile').innerHTML = "这个图片已经上传过了";
            }
            else
            {
                document.getElementById('ossfile').innerHTML = "Error xml:" + err.response;
            }
		}
	}
});

uploader.init();
