# Muddy - Proving Grounds Box

## Recon

I ran `nmap -sS -sV $TARGET`.

![](Pasted%20image%2020260301204358.png)

I added the IP to /etc/hosts for the host `muddy.ugc`. I notice a "Ladon" server is hosted on port 8888.

![](Pasted%20image%2020260301204507.png)

There are some endpoints accepting POST: `xmlrpc`, `jsonrpc10`, `jsonwsp`, etc. Let me do some research on it. Looks like we need to pop an XXE vulnerability.
## Exploit
x

## Guidance

x