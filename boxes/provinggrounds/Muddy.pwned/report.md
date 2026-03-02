# Muddy - Proving Grounds Box

## Recon

I ran `nmap -sS -sV $TARGET`.

![](Pasted%20image%2020260301204358.png)

I added the IP to /etc/hosts for the host `muddy.ugc`. I notice a "Ladon" server is hosted on port 8888.

![](Pasted%20image%2020260301204507.png)

There are some endpoints accepting POST: `xmlrpc`, `jsonrpc10`, `jsonwsp`, etc. Let me do some research on it. Looks like we need to pop an XXE vulnerability.

I also noticed that `gobuster` shows me that WebDAV is enabled. I will likely need to login later with stolen credentials.

![](Pasted%20image%2020260302131339.png)

I searched `exploit-db.com` for Ladon XXE vulnerabilities. Apparently all we need for LFI is a `curl` command with the right payload.

## Exploit

### XML XXE Local File Inclusion
I was able to trigger XML LFI with an HTTP POST:

![](Pasted%20image%2020260302133649.png)

![](Pasted%20image%2020260302133716.png)

The next step is to use this to steal WebDAV credentials so we can upload a webshell.

I then obtained the `passwd.dav` file by targeting `/var/www/html/webdav/passwd.dav`:

![](Pasted%20image%2020260302134324.png)

![](Pasted%20image%2020260302134418.png)
### Cracking WebDAV Credentials

I first need to crack the hashed password for the user `administrant`.

![](Pasted%20image%2020260302135402.png)

Shortly after that, we get `sleepless` as the password:

![](Pasted%20image%2020260302135434.png)

The cred is `administrant:sleepless`.

### Using WebDAV Credentials and uploading a PHP web shell

I prepared a PHP web shell to upload, and started a `nc` listener.

![](Pasted%20image%2020260302150652.png)

![](Pasted%20image%2020260302150748.png)

I then uploaded the reverse shell payload:

![](Pasted%20image%2020260302151036.png)

And then I caused the victim PHP runtime to execute our code:

![](Pasted%20image%2020260302151205.png)

Resulting in a functioning reverse shell running in the php user context, `www-data`:

![](Pasted%20image%2020260302151239.png)

I stabilized my shell with `python3`:

![](Pasted%20image%2020260302151443.png)

### Pivoting: Cron Job Exploitation

![](Pasted%20image%2020260302153022.png)

`/dev/shm` is writeable by us.

Because the command `netstat` gets run every 1 minute by `root` user, we can use this to get a root shell on our victim.

We just need to create an executable named `netstat` within the `/dev/shm` folder to achieve root access.

![](Pasted%20image%2020260302153603.png)

The `s` bit is set on the file `/bin/bash`, meaning we can use `/bin/bash -p` to get a root shell. `p` means "Preserve effective UID", which is `root` in this case.

![](Pasted%20image%2020260302153734.png)

And, we have root access and flag.

![](Pasted%20image%2020260302153838.png)


## Guidance

Do not parse XML External Entities.

Do not expose unnecessary XML parsing services over the network.

Consider disabling WebDAV and SOAP XML APIs unless necessary, or putting them behind a firewall.