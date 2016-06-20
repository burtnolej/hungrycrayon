
<?php

/*
 * based on https://github.com/abrahamvegh/simplenote-php/blob/master/simplenoteapi.php
 *
 */
class simplenoteapi
{
    private $email;
    private $token;

    private function curl_request($url_append, $curl_options = array())
    {
        $curl_options[CURLOPT_URL] = 'https://simple-note.appspot.com/' . $url_append;
        $curl_options[CURLOPT_HEADER] = true;
        $curl_options[CURLOPT_RETURNTRANSFER] = true;
        $ch = curl_init();

        curl_setopt_array($ch,$curl_options);

        $result = curl_exec($ch);
        $stats = curl_getinfo($ch);
        $result = explode("\n",$result);
        $headers = array();
        $break = false;
        unset($result[0]);

        foreach ($result as $index => $value)
        {
            if (!$break)
            {
                if (trim($value) == '')
                {
                    unset($result[$index]);
                    $break = true;
                }
                else
                {
                    $line = explode(':',$value,2);
                    $headers[$line[0]] = $line[1];

                    unset($result[$index]);
                }
            }
        }

        $result = implode("\n",$result);

        curl_close($ch);

        $result = array(
            'stats'=>$stats,
            'headers'=>$headers,
            'body'=>$result
        );

        return $result;
    }

    private function api_get($method,$parameters = '')
    {
        if (is_array($parameters)) {

            foreach ($parameters as $key => $value)
            {
                unset($parameters[$key]);
                $parameters[] = urlencode($key) . '=' . urlencode($value);
            }
            $parameters = implode('&', $parameters);
        }
        !empty($parameters) ? $parameters = '?' . $parameters : false;

        return $this->curl_request($method . $parameters);
    }

    private function api_post($method,$body,$parameters = '')
    {
        $curl_options = array(
            CURLOPT_POST => true,
            CURLOPT_POSTFIELDS => $body
        );

        if (is_array($parameters)) {
            foreach ($parameters as $key => $value)
            {
                unset($parameters[$key]);
                $parameters[] = urlencode($key) . '=' . urlencode($value);
            }
            $parameters = implode('&', $parameters);
        }
        !empty($parameters) ? $parameters = '?' . $parameters : false;

        return $this->curl_request($method . $parameters, $curl_options);
    }

    public function login($email,$password)
    {
        /*$body = 'email=' . urlencode($email) . '&password=' . urlencode($password);
        $body = 'email=' . $email . '&password=' . $password;

        $body = base64_encode("email=burtnolejusa@gmail.com&password=g0ldm@n1");*/

        $body = 'ZW1haWw9YnVydG5vbGVqdXNhQGdtYWlsLmNvbSZwYXNzd29yZD1nMGxkbUBuMQo=';
        /*$body = base64_encode('email=' . urlencode($email) . '&password=' . urlencode($password));*/
        $response = $this->api_post('api/login',$body);

        if ($response['stats']['http_code'] == 200)
        {
            $this->email = $email;
            $this->token = $response['body'];

            return true;
        }
        else
        {
            return false;

        }
    }

    public function index()
    {
        $response = $this->api_get(
            'index',
            array(
                'auth' => $this->token,
                'email' => $this->email
            )
        );
        if ($response['stats']['http_code'] == 200)
        {
            $response = json_decode($response['body']);
            return $response;
        }
        else
        {
            return false;
        }
    }
}

$api = new simplenoteapi;
$api->login('burtnolejusa@gmail.com','g0ldm@n1');
print_r($api->index());

