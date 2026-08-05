https://www.youtube.com/watch?v=ey_GeabfQpg&list=PLM1644RoigJvm0L7RcK-64aVTp1vZkDv5

	netexec smb 1.2.3.4/24 
	# this checks if smb is accessible

```sh
cat <<EOF
1.2.3.4
1.2.3.5
1.2.3.7
EOF > ips.txt
```

```sh
netexec smb ips.txt

nmap -p- -Pn -iL ips.txt -v --min-rate 1000 --max-retries 5 -oN nmap_ports.txt --open
```

then get bloodhound running...

```sh

curl -L https://ghst.ly/getbhce -o docker-compose.yml

docker-compose pull && docker-compose up -d

docker-compose logs bloodhound | grep -i passwd
```

then pull data into bloodhound

```sh

netexec ldap $target -u SQLService -p 'mypassword123!' --bloodhound --collection All --dns-server 10.0.2.4
```