///**
// * Populate tree using json representation of the directory hierarchy
// * (variable 'uuid' is provided as global variable)
// */
//function show(id, value) {
//    document.getElementById(id).style.display = value ? 'block' : 'none';
//}
//(function(){
//    $.ajax({
//        url: "/earkweb/sip2aip/get_directory_json",
//        type: "POST",
//        data: "uuid="+uuid,
//    }).success(function(dir_as_json){
//        $('#directorytree')
//        .on('changed.jstree', function (e, data) {
//            if(data.node.data) {
//                ip_work_dir_sub_path = data.node.data.path
//                mimetype = data.node.data.mimetype
//                show('loadingpreview', true);
//                $.ajax({
//                  url: "/earkweb/earkcore/read_ipfc/" + ip_work_dir_sub_path,
//                  context: document.body
//                }).success(function(data) {
//                    bootbox.dialog({
//                        message: "<div id='XmlPreview' class='xmlview'></div>",
//                        title: "File preview (" + mimetype + ")",
//                        className: "modal70"
//                    });
//                    switch (mimetype) {
//                        case 'application/xml':
//                            LoadXMLString('XmlPreview',data);
//                            break;
//                        case 'image/jpeg':
//                             $('#XmlPreview').html("<p>JPEG viewer is not  implemented</p>")
//                            break;
//                        case 'image/tiff':
//                             $('#XmlPreview').html("<p>TIFF viewer is not  implemented</p>")
//                            break;
//                        case 'image/png':
//                             $('#XmlPreview').html('<p><img src="" id="displayimage" style="max-width: 1000px;" /></p>')
//                             document.getElementById("displayimage").src = data;
//                            break;
//                        case 'application/pdf':
//                             $('#XmlPreview').html("<p>PDF viewer is not implemented</p>")
//                            break;
//                        case 'text/plain':
//                             $('#XmlPreview').html("<pre>"+data+"</pre>")
//                            break;
//                        default:
//                            $('#XmlPreview').html("<pre>"+mimetype+"</pre>")
//                            break;
//                    }
//                    show('loadingpreview', false);
//                }).error(function(err, message, status_text) {
//                    bootbox.dialog({
//                      message: err.responseText,
//                      title: "Error "+err.status+ "(" + status_text + ")",
//                      buttons: {
//                        success: {
//                          label: "OK!",
//                          className: "btn-default"
//                        }
//                      }
//                    });
//                });
//            }
//         }).on('open_node.jstree', function (e, data) {
//            $('#directorytree').jstree(true).set_icon(data.node.id, 'glyphicon glyphicon-folder-open');
//         }).on('close_node.jstree', function (e, data) {
//            $('#directorytree').jstree(true).set_icon(data.node.id, 'glyphicon glyphicon-folder-close');
//         }).jstree({ 'core' : dir_as_json });
//    });
//})();
