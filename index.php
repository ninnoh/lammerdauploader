<?php 

$redis = new Redis();
$redis->connect('127.0.0.1', 6379);

if(isset($_GET['dl'])){
    header('Content-Description: File Transfer');

    header('Expires: Sun, 01 Jan 2014 00:00:00 GMT');
    header('Cache-Control: no-store, no-cache, must-revalidate');
    header('Cache-Control: post-check=0, pre-check=0', FALSE);
    header('Pragma: no-cache');
    
    $roba = $redis->get($_GET['dl']);
    $res = json_decode($roba, true);
    header('Content-Type: '.$res["update"][$res["type"]]["mime_type"]);
    header('Content-Length: '.$res["update"][$res["type"]]["file_size"]);

    if (strpos($res["update"][$res["type"]]["mime_type"], "text") === 0){
        header('Content-Type: application/octet-stream');
        header('Content-Disposition: attachment; filename="'.$res["update"][$res["type"]]["file_name"].'"');
        header('Content-Transfer-Encoding: binary');        
    }
    if(in_array($res["update"][$res["type"]]["mime_type"], ["application/json", "text/plain", "text/xml", "text/css", "text/javascript", "application/atom+xml", "application/rss+xml", ""])){
        header('Content-Type: application/octet-stream');
        header('Content-Disposition: attachment; filename="'.$res["update"][$res["type"]]["file_name"].'"');
        header('Content-Transfer-Encoding: binary');
    }
    if(isset($_GET['force']) and $_GET['force'] == True){
        header('Content-Type: application/octet-stream');
        header('Content-Disposition: attachment; filename="'.$res["update"][$res["type"]]["file_name"].'"');
        header('Content-Transfer-Encoding: binary');       
    }
    readfile($res['url_internal']);
}else{
    echo "FALSE";
}
