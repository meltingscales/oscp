# Offensive Security - Levram

Henry Post
## Recon

An `nmap` scan shows two ports open: 22 and 8000.

![](Pasted%20image%2020260304095131.png)

Port 8000 is running a server that I can log in with the `admin:admin` credential.

![](Pasted%20image%2020260304095251.png)

I notice that `gerapy 0.9.7` is a version of this web portal.

![](Pasted%20image%2020260304095351.png)

So I searched for it in `exploit-db.com` and found an exploit.

![](Pasted%20image%2020260304095434.png)

## Exploit

Running the exploit initially fails. I am guessing due to an empty Projects list.

![](Pasted%20image%2020260304100137.png)

So I create a "project" in gerapy.

![](Pasted%20image%2020260304100213.png)

Then, I run it again, and it works! We have non-root shell.

![](Pasted%20image%2020260304100316.png)

I searched for `setuid` permissions by using `getcap -r / 2>/dev/null`.

![](Pasted%20image%2020260304100357.png)

In Linux, `setuid` means that an executable file can be run as the owner, so if the user called `root` owns a binary, we can run it as that user.

I then run `/usr/bin/python3.10 -c 'import os; os.setuid(0); os.system("/bin/bash")'` to get a shell as root.

And we can steal the root flag.

![](Pasted%20image%2020260304100540.png)

## Recommendations

Upgrade gerapy immediately to the latest version.

Do not use default credentials.