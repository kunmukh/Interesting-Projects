# Network Separation and DNSMASQ Setup
### Main changes:
1. 2 new interfaces created: vbox0 and vbox1
2. vbox0: IP: 10.0.3.1, vbox1: IP: 10.0.2.1
3. vbox0: network for cuckoo server and clients, vbox1: network for infrastructural service

* Current Station pic attached
* TODO: 
    1. DNSMASQ Setup
    2. VPN Setup

## Network Separation

## Script: Tested and Working

### vbox1 setup: Infrastructure related network

* Creation of hostonly network

	* "vboxnet1" and "10.0.2.1" will be modified according to user requirmeent

 `sudo vboxmanage hostonlyif create`
 `sudo vboxmanage hostonlyif ipconfig vboxnet1 --ip 10.0.2.1`
 `VBoxManage hostonlyif ipconfig vboxnet1 --ip 10.0.2.1 --netmask 255.255.255.0`

* Change VM setting to hostonly network

	* "asi-sv" and "vboxnet1" will be modified according to user requirment

`vboxmanage modifyvm asi-sv --hostonlyadapter1 vboxnet1`
`vboxmanage modifyvm asi-sv --nic1 hostonly`


* IP Table update
	* "wlx1cbfce02985a" and "vboxnet1" will be modified according to user requirment

`sudo iptables -A FORWARD -o wlx1cbfce02985a -i vboxnet1 -s 10.0.2.0/24 -m conntrack --ctstate NEW -j ACCEPT`
`sudo iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT`
`sudo iptables -A POSTROUTING -t nat -j MASQUERADE`
`sudo su`
`echo 1 > /proc/sys/net/ipv4/ip_forward`

* Save IP rules

`sudo dpkg-reconfigure iptables-persistent`

### vbox1 connection setup: ASI and DNSMASQ SetUp

* ASI-SV Config

```
auto enp0s3
iface enp0s3 inet static
address 10.0.2.2
netmask 255.255.255.0
gateway 10.0.2.1
dns-nameservers 1.1.1.1 1.0.0.1

```
* (TODO) DNSMASQ Config

``` shell
auto enp0s3
iface enp0s3 inet static
address 10.0.2.53
netmask 255.255.255.0
gateway 10.0.2.1
dns-nameservers 1.1.1.1 1.0.0.1
```

### vbox0 setup: Cuckoo related network

* Creation of hostonly network

	* "vboxnet0" and "10.0.3.1" will be modified according to user requirmeent

`sudo vboxmanage hostonlyif create`
`sudo vboxmanage hostonlyif ipconfig vboxnet0 --ip 10.0.3.1`
`VBoxManage hostonlyif ipconfig vboxnet0 --ip 10.0.3.1 --netmask 255.255.255.0`

* Change VM setting to hostonly network

	* "cuckooC1" and "vboxnet0" will be modified according to user requirment

`vboxmanage modifyvm cuckooC1 --hostonlyadapter1 vboxnet0`
`vboxmanage modifyvm cuckooC1 --nic1 hostonly`

* IP Table update
	* "wlx1cbfce02985a" and "vboxnet0" will be modified according to user requirment

`sudo iptables -A FORWARD -o wlx1cbfce02985a -i vboxnet0 -s 10.0.3.0/24 -m conntrack --ctstate NEW -j ACCEPT`
`sudo iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT`
`sudo iptables -A POSTROUTING -t nat -j MASQUERADE`
`sudo su`
`echo 1 > /proc/sys/net/ipv4/ip_forward`

* Save IP rules

`sudo dpkg-reconfigure iptables-persistent`

### vbox0 connection setup: Cuckoo SetUp

* cuckooC1 Config

```
auto enp0s3
iface enp0s3 inet static
address 10.0.3.101
netmask 255.255.255.0
gateway 10.0.3.1
dns-nameservers 1.1.1.1 1.0.0.1
```

* edit $CUCKOO/conf/virtualbox.conf

    * change 'ip' and 'interface'

* edit $CUCKOO/conf/cuckoo.conf

    * change resultserver ip

### DNSMASQ Setup - 1

### Pre-Set up

* Create a new VM

	1. VM Name: mal-dnsmasq
	2. username: dnsmasq-admin
	3. password: dnsmasqvmpass20

* fix DNS: 
* edit /etc/resolv.conf and add line `nameserver 8.8.8.8`
* run `/etc/init.d/networking restart`
* `sudo apt-get update`
* `sudo apt-get upgrade`

* follow instruction: https://askubuntu.com/questions/1012641/dns-set-to-systemds-127-0-0-53-how-to-change-permanently

* `sudo apt-get install make perl gcc` 
* install VirtualBox Guest Additions Installation
* `sudo apt-get install python`
* `sudo apt install net-tools`

* Change network adapter: Host-only - vboxnet1

* give static IP: 10.0.2.53: https://graspingtech.com/ubuntu-server-16-04-static-ip/
`auto enp0s3
iface enp0s3 inet static
address 10.0.2.53
netmask 255.255.255.0
gateway 10.0.2.1
dns-nameservers 1.1.1.1 1.0.0.1`

* Change VM setting to hostonly network

`vboxmanage modifyvm mal-dnsmasq --hostonlyadapter1 vboxnet1`
`vboxmanage modifyvm mal-dnsmasq --nic1 hostonly`

## DNSMASQ Setup - 2

### DNSMASQ Installation 

* To stop the systemd-resolved service
`sudo systemctl stop systemd-resolved`

* To disable the systemd-resolved service
`sudo systemctl disable systemd-resolved`

* remove the /etc/resolv.conf link with the following command
`sudo rm -v /etc/resolv.conf`

*  create a new /etc/resolv.conf file and set the google DNS server as the default DNS server
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf

* update /etc/resolvconf/resolv.conf.d/tail
remove everything from the file
modify the line `# nameserver 8.8.8.8` 

* update the APT package and install dnsmasq
`sudo apt update`
`sudo apt install dnsmasq`

### DNSMASQ Configuration

* saving the backup dnsmasq conf file
`sudo mv -v /etc/dnsmasq.conf /etc/dnsmasq.conf.bk`

* create the configuration file /etc/dnsmasq.conf
`sudo nano /etc/dnsmasq.conf`

```
# DNS configuration
port=53
 
domain-needed
bogus-priv
strict-order
 
expand-hosts
#domain=example.com

# Set Liste address
listen-address=127.0.0.1 # Set to Server IP for network responses
listen-address=10.0.2.53
```

* restart dnsmasq service
`sudo systemctl restart dnsmasq`

* set 10.0.2.53 as the default DNS server address in the /etc/resolv.conf
add `nameserver 10.0.2.53` before `nameserver 8.8.8.8`

* do a complete restart
`init 6`

* do a sanity check
run `dig google.com`

In the result look at SERVER IP, should be 127.0.0.1
```
;; ANSWER SECTION:
google.com.		104	IN	A	172.217.14.174

;; Query time: 0 msec
;; SERVER: 127.0.0.1#53(127.0.0.1)
;; WHEN: Sat Jul 18 20:33:38 CDT 2020
;; MSG SIZE  rcvd: 55

```

### DNSMASQ Client Setup
* on each client change the file '/etc/network/interfaces'
add `dns-nameservers 10.0.2.53`

* edit /etc/resolv.conf and add line `nameserver 10.0.2.53`
run `/etc/init.d/networking restart`

* do a complete restart
`init 6`

* do a sanity check
run `dig google.com`
In the result look at SERVER IP, should be 10.0.2.53
```
;; ANSWER SECTION:
google.com.		104	IN	A	172.217.14.174

;; Query time: 0 msec
;; SERVER: 10.0.2.53#53(10.0.2.53)
;; WHEN: Sat Jul 18 20:33:38 CDT 2020
;; MSG SIZE  rcvd: 55

```
