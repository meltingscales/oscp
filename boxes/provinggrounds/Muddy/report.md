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
### Using WebDAV Credentials

tbd.

## Guidance

Do not parse XML External Entities.

Do not expose unnecessary XML parsing services over the network.

Consider disabling WebDAV and SOAP XML APIs unless necessary, or putting them behind a firewall.