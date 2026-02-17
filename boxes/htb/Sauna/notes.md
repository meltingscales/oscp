this time, to not waste time, I am going to go through a walkthrough of sauna.

https://0xdf.gitlab.io/2020/07/18/htb-sauna.html

"Kerberoast brute force on usernames". okay.

let's make a username list.

`./generated_usernames.txt`

ask z.ai ` sauna htb box - kerberoast brute force - how do I do this?`

following guide...

step 1: find user accounts that have an "SPN" assigned. What is an SPN?
> SPN= "Service Principal Name" is a unique identifier for a service instance in an "Active Directory environment"

okay.

> EGOTISTICAL-BANK.LOCAL

is this a SPN?
yes. cool. let's keep going and use our `SPN` to kerberoast.

`impacket-GetUserSPNs` is our tool.

    impacket-GetUserSPNs
