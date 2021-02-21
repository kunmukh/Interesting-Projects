# Cuckoo Host Set Up and related Issues and solution

## Cuckoo Set-Up Resources
0. https://arnaudloos.com/2019/cuckoo-sandbox-installation/
1. https://tech-zealots.com/malware-analysis/cuckoo-sandbox-host-installation-part-1/
2. https://tech-zealots.com/threat-lab/cuckoo-sandbox-guest-installation-part-2/
3. http://docs.cuckoosandbox.org/en/2.0.7/installation/guest/linux/
4. https://www.proteansec.com/linux/installing-using-cuckoo-malware-analysis-sandbox/
5. https://readthedocs.org/projects/cuckoo/downloads/pdf/latest/

## OS related
* Cuckoo is geared towards analysis of windows guest VM and malware analysis
* Cuckoo modules are not fully supported for Ubuntu VM - having to manually adjust VM settings
* Ubuntu 18.04 dns-nameserver issue: https://graspingtech.com/ubuntu-server-16-04-static-ip/ and https://askubuntu.com/questions/1012641/dns-set-to-systemds-127-0-0-53-how-to-change-permanently

## Network related
* Firewall causing issue for guest to connect: `sudo ufw disable`


## Volatility
* Distorm3 3.5 breaks Cuckoo: https://github.com/volatilityfoundation/volatility/issues/719
* Ubuntu profile have to manually download: https://github.com/volatilityfoundation/profiles/blob/1e8d567b7797379072a7ab498737b6b310ee9f4b/Linux/Ubuntu/x64/Ubuntu18043.zip
* Adding ubuntu profile issue: https://www.andreafortuna.org/2019/08/22/how-to-generate-a-volatility-profile-for-a-linux-system/
* volatility module not running: https://github.com/cuckoosandbox/cuckoo/issues/2823
* volatility analysis not running - UNRESOLVED