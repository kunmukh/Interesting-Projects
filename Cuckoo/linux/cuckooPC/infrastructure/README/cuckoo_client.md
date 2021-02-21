# Cuckoo Client Set Up Instructions

###  1.Install Ubuntu 18.04
* name: cuckooC1	
* username: cuckooc1
* password: cuckooc
* automatic log in

### 2.fix DNS: 
* edit /etc/resolv.conf and add line `nameserver 8.8.8.8`
* run `/etc/init.d/networking restart`
* `sudo apt-get update`
* `sudo apt-get upgrade`
* follow instruction: https://askubuntu.com/questions/1012641/dns-set-to-systemds-127-0-0-53-how-to-change-permanently
* `sudo apt-get install make perl gcc` 
* install VirtualBox Guest Additions Installation
* `sudo apt-get install python`
* `sudo apt install net-tools`

### 3.Change network adapter: Host-only - vboxnet0

###  4.give static IP: 192.168.56.101: https://graspingtech.com/ubuntu-server-16-04-static-ip/
`auto enp0s3
iface enp0s3 inet static
address 192.168.56.101
netmask 255.255.255.0
gateway 192.168.56.1
dns-nameservers 1.1.1.1 1.0.0.1`

###  5.patch systemtap for Linux: https://askubuntu.com/questions/1173904/is-systemtap-broken-on-5-0-0-kernel
``` shell
$ sudo apt remove systemtap
$ sudo apt install g++ make git libelf-dev libdw-dev

$ git clone git://sourceware.org/git/systemtap.git
$ cd systemtap/
$ ./configure && make         // no errors
$ sudo make install

$ sudo stap -e 'probe begin { printf("Hello, World!\n"); exit() }'
[sudo] password for knudfl: 
Hello, World!
```
###  6.install cuckoo agent.py (http://docs.cuckoosandbox.org/en/2.0.7/installation/guest/linux/)
* Running of agent automatically do this **INSTEAD**
``` shell
$ sudo crontab -e
@reboot /path/to/agent.sh
```
* While installing VM dependencies **do not re-install systemtap**
* No need to do this step **Patch the SystemTap tapset, so that the Cuckoo analyzer can properly parse the output:**
* Test agent is running: 
    * `sudo apt-get install curl` 
    * `curl 192.168.56.101:8000` on **BOTH** host and guest OS
    * should get a reply

``` shell
{"message": "Cuckoo Agent!", "version": "0.10", "features": ["execpy", "pinning", "logs", "largefile", "unicodepath"]}
```

###  7.install asi agent
* Edit /etc/hosts add line `34.74.104.188  asi-sv`
* Connect to UpControl Console with http://asi-sv:56565
* Click `Client Deployment`  under **Auxiliary Information**
* Click the link for your OS
* Test agent is running: 
    * `ps -ef | grep NEC-Agent` 
    * should get a reply

``` shell
cuckooc1@cuckooc1-VirtualBox:~/asiClient$ ps -ef | grep NEC-Agent
root      2860     1  1 21:17 ?        00:00:16 /opt/NECLA/Agent/bin/NEC-Agent
cuckooc1  4809  4647  0 21:41 pts/0    00:00:00 grep --color=auto NEC-Agent

```

###  8.open two terminal and run `python agent.stdout` and  `agent.stderr` for debugging info

###  9.remove password: http://jonmoore.duckdns.org/index.php/linux-articles/58-remove-sudo-password-prompt

###  10.take snapshot: name: cuckooC1s
``` shell
$ VBoxManage snapshot "cuckooC1" take "cuckooC1s" --pause
$ VBoxManage controlvm "cuckooC1" poweroff
$ VBoxManage snapshot "cuckooC1" restorecurrent
```

###  11.update in HOST MACHINE: virtualbox.conf
``` shell
[cuckoo1]
# Specify the label name of the current machine as specified in your
# VirtualBox configuration.
label = cuckooC1

# Specify the operating system platform used by current machine
# [windows/darwin/linux].
platform = linux

# Specify the IP address of the current virtual machine. Make sure that the
# IP address is valid and that the host machine is able to reach it. If not,
# the analysis will fail.
ip = 192.168.56.101

# (Optional) Specify the snapshot name to use. If you do not specify a snapshot
# name, the VirtualBox MachineManager will use the current snapshot.
# Example (Snapshot1 is the snapshot name):
snapshot = cuckooC1s
```
