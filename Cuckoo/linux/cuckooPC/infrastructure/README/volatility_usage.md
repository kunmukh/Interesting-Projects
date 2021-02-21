ref1: how to create a profile (https://www.andreafortuna.org/2019/08/22/how-to-generate-a-volatility-profile-for-a-linux-system/)

ref2: how to run volatility (https://www.howtoforge.com/tutorial/how-to-install-and-use-volatility-memory-forensic-tool/)

* memory-dmp-file: vboxserv@syssec10:/home/vboxserv/Documents/kunal-volatility-files/dmp-files/
* Ubuntu volatility profile: vboxserv@syssec10:/home/vboxserv/Documents/kunal-volatility-files/profiles/

Step 1a: Get Volatility (skip if you are on syssec10)

> $ `git clone https://github.com/volatilityfoundation/volatility.git`
> $ `cd volatility`

Step 1b: Ubuntu Profile Set Up (skip if you are on syssec10)

> $`unzip Ubuntu-Profile.zip`
> put the Ubuntu18043.zip, Ubuntu1804.zip and Ubuntu1805.zip into `volatility/volatility/plugins/overlays/linux` (ref1)
> $ `./vol.py --info | grep Ubuntu `
NOTE: make sure you see this output
```
LinuxUbuntu18043x64   - A Profile for Linux Ubuntu18043 x64
LinuxUbuntu1804x64    - A Profile for Linux Ubuntu1804 x64
LinuxUbuntu1805x64    - A Profile for Linux Ubuntu1805 x64
```

Step3: Getting started with volatility

> dump file: memory-malware-dmp.zip 
> unzip the file to access .dmp file
> To see everything you can do with a linux dump: $ `./vol.py --info | grep linux` 
> e.g. to be able to see pslist (ref2) $ `./vol.py --profile=LinuxUbuntu1805x64 linux_pslist -f {dump_location}/{1,2,3,4}/memory.dmp`
> syssec10 specific example `vboxserv@syssec10:~/Documents/kunal-volatility-files/volatility$ ./vol.py --profile=LinuxUbuntu1805x64 linux_pslist -f ../dmp-files/1/memory.dmp`
