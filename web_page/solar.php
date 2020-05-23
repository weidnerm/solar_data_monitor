<?php

    header('Access-Control-Allow-Origin: *');
    header('Access-Control-Allow-Methods: GET, POST, PATCH, PUT, DELETE, OPTIONS');
    header('Access-Control-Allow-Headers: Origin, Content-Type, X-Auth-Token, X-Requested-With');

    $format='json';
    
    function startsWith ($string, $startString) 
    { 
        $len = strlen($startString); 
        return (substr($string, 0, $len) === $startString); 
    } 
    
    function endsWith($string, $endString) 
    { 
        $len = strlen($endString); 
        if ($len == 0) { 
            return true; 
        } 
        return (substr($string, -$len) === $endString); 
    } 
    
    if(!empty($_GET['day'])){
        $day=$_GET['day'];

        $filename = "/home/pi/proj/solar/solar_data_monitor/solarLog_".$day.".csv";
        $handle = fopen($filename, "r");
        $contents = fread($handle, filesize($filename));
        $contents_array = explode("\n", $contents);
        fclose($handle);
        
        //~ $mydata = array("day" => $day);
        //~ $mydata = [60,20,30,40,50];
        
        //~ $json_results = json_encode($mydata, JSON_FORCE_OBJECT);
        $json_results = json_encode($contents_array);
        //~ $json_results = "[10,20,30,40,50]";
        //~ $json_results = "$contents]";
        
        echo $json_results;
    }

    else if(!empty($_GET['maxDays'])){
        $days=$_GET['maxDays'];

        $dir = "/home/pi/proj/solar/solar_data_monitor";
        
        $contents_array = [];

        //~ get list of filenames in dir.
        if ($handle = opendir($dir)) {

            while (false !== ($entry = readdir($handle))) {

                if ($entry != "." && $entry != ".." ) {
                    if(startsWith($entry, "solarLog_") && endsWith($entry,'.csv')) {
                        $contents_array[] = substr($entry, 9, 10);
                    }
                }
            }

            closedir($handle);
        }
        
        sort($contents_array);
        
        $json_results = json_encode($contents_array);
        
        echo $json_results;
    }

    else if(!empty($_GET['liveSource'])){
        $liveSource=$_GET['liveSource'];
        
        $sock = socket_create(AF_INET, SOCK_DGRAM, 0);

        $msg = 'sub';

        socket_sendto($sock, $msg, strlen($msg), 0, $liveSource, 29551);
        
        $reply = '{"y":1}';
        
        socket_recv($sock, $reply, 2045, MSG_WAITALL);

        socket_close($sock);
        
        //~ $reply = '{"y":"'.strlen($reply).'"}';
         
        echo $reply;
    }

   
    
    

?>
