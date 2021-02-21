# interfaces(5) file used by ifup(8) and ifdown(8)
auto lo
iface lo inet loopback

auto enp0s3
iface enp0s3 inet static
address 192.168.56.101
netmask 255.255.255.0
gateway 192.168.56.1
dns-nameservers 1.1.1.1 1.0.0.1

VBoxManage snapshot "cuckooC1" take "cuckooC1s" --pause
VBoxManage controlvm "cuckooC1" poweroff
VBoxManage snapshot "cuckooC1" restorecurrent

sudo iptables -t nat -A POSTROUTING -o wlx1cbfce02985a -s 192.168.56.0/24 -j MASQUERADE
sudo iptables -P FORWARD DROP
sudo iptables -A FORWARD -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -s 192.168.56.0/24 -j ACCEPT
sudo iptables -A FORWARD -s 192.168.56.0/24 -d 192.168.56.0/24 -j ACCEPT
sudo iptables -A FORWARD -j LOG

sudo netfilter-persistent save

echo 1 | sudo tee -a /proc/sys/net/ipv4/ip_forward
sudo sysctl -w net.ipv4.ip_forward=1


cuckoo clean
cuckoo -f
cuckoo web runserver 

python vol.py --profile=LinuxUbuntu1804x64 linux_pslist -f memory.dmp
python vol.py -f 09af9958262de0066faabfc844a42137 imageinfo
python vol.py imageinfo -f 09af9958262de0066faabfc844a42137


