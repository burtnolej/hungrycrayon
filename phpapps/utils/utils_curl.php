<?php

$email = 'burtnolejusa@gmail.com';
$pass = 'g0ldm@n1';
$data = base64_encode('email='.$email.'&password='.$pass);
$url='https://simple-note.appspot.com/api/login';
$curl = curl_init($url);

curl_setopt($curl, CURLOPT_POST,true);
curl_setopt($curl, CURLOPT_VERBOSE,1);
curl_setopt($curl, CURLOPT_POSTFIELDS,$data);
curl_setopt($curl, CURLOPT_RETURNTRANSFER,true);
curl_setopt($curl, CURLOPT_HTTPHEADER, array("User-Agent: Test"));
curl_setopt($curl, CURLOPT_HEADER,false);

$token = curl_exec($curl);
$http_status = curl_getinfo($curl, CURLINFO_HTTP_CODE);
$stats = curl_getinfo($curl);

curl_close($curl);

echo '{ "token": "'.$token.'" }';

foreach ($stats as $key => $value) {
    echo $key, $value;
}
exit();
?>