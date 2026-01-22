nmap, what flags for initial scan?

```
export HTBIP=10.129.6.180
nmap -sC -sV -oN nmap.txt $HTBIP

# this is annoying. rustscan is probably faster. let's try it!

rustscan -a $HTBIP -r 1-65535 -- -sC -sV -oN rustscan.txt

smbclient -L //$HTBIP -N
```

well. i feel like SMB is involved.

https://chat.z.ai/c/6acc9269-b28c-4eb4-b1ae-2c6022f108cf

well, china AI agrees. giving me pretty good advice.


so.

crackmapexec is a swiss army knife,

netexec seems to be a replacement since it's a "hostile fork", meaning the original author was unable to maintain the original. 

netexec is a better replacement.

```sh
export HTBIP=10.129.6.180
netexec smb $HTBIP
# also, look at wireshark to see how SMB works.
# 
# reply:

┌──(henrypost㉿kali-toughwolf)-[~/Git/NetExec]
└─$ export HTBIP=10.129.6.180
netexec smb $HTBIP

    SMB         10.129.6.180    445    SECNOTES         [*] Windows 10 Enterprise 17134 (name:SECNOTES) (domain:SECNOTES) (signing:False) (SMBv1:True) (Null Auth:True)


smbclient -L //$HTBIP -N

```

okay. it has a web ui, it's just a PHP notes app.

I'm thinking i should try some php code injection.

maybe it stores the notes as plaintext files in `/var/www/html/notes/my_note_1.txt`, and I can do LFI...

yeah, it just sends HTTP POST thusly,

```
curl 'http://10.129.6.180/submit_note.php' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -b 'PHPSESSID=m9tflr14dkbut99pqajvn77h4j' \
  -H 'Origin: http://10.129.6.180' \
  -H 'Referer: http://10.129.6.180/submit_note.php' \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36' \
  --data-raw 'title=asdfasdf&note=asfasdfasdfasdf%0D%0A&submit=Save' \
  --insecure
```


another clue, there's a "contact us" page...

```
Contact Us
Please enter your message

To: tyler@secnotes.htb
Message:
```

maybe I can login as `tyler` in smb.

```
smbclient -L //$HTBIP -U tyler

                                                                                
┌──(henrypost㉿kali-toughwolf)-[~]
└─$ smbclient -L //$HTBIP -U tyler

Password for [WORKGROUP\tyler]:
session setup failed: NT_STATUS_LOGON_FAILURE
                                                                                

```

useful. `tyler` exists as a user.

okay.

the guided mode seems to focus on `/change_pass.php` and HTTP methods.

it makes me think that it's vulnerable to ...well. spoofing the username? i don't know.

so...POST /change_pass.php and GET /change_pass.php both work. it seems like the victim doesn't care about what verb we use. but changing the verb and the HTTP body doesn't do anything.

okay. so I just learned that `tyler`...is...well, the HTB box wants us to pretend like tyler is actually a physical person. So, we're meant to trigger a CSRF attack against `tyler` by sending a malicious request that comes from `tyler`'s browser, because they clicked a link we sent them in the login form.

this ONLY WORKS because GET is an allowed verb. if it wasn't, we couldn't embed the GET body in the url.

```payload
Hello! Your password has expired. Please click this link to reset it.

http://10.129.6.180/change_pass.php?user=tyler&password=password&confirm_password=password&submit=submit
```

i need to not use `zed`'s autocomplete, because it populated the wrong values for the GET url fragments.


sweet, we logged in as `tyler`. see `tylernotes.txt`

I bet `92g!mA8BGjOirkL%OG*&` is the password to log in via SMB...
