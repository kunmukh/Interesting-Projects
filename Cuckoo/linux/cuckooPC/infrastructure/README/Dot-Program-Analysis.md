# SplitBrain: Malware ProvGraph Evaluation

## RPi Available:
username/password: pi/splitbrain

methods of connection: ssh and vncviewer

RPi 3B- 10.176.150.45 
RPi 4B- 10.176.150.46 
RPi 4B- 10.176.150.48 


## ProvGraph dataset
[Result Zip Link](https://cometmail-my.sharepoint.com/:u:/g/personal/kxm180046_utdallas_edu/Eebx176iwRlCsmOehspgXHMBnr47vCyior3mBoboZSbbQQ?e=qQbduB)

## Example provenance graph
[Non-interesting provenance graph](https://cometmail-my.sharepoint.com/:i:/g/personal/kxm180046_utdallas_edu/ERut_mlHzZpCoeQVKgEpsMcBEBo6w0DvbRK6mX2dNwsQmg?e=4FP6C5)

[Interesting provenance graph](https://cometmail-my.sharepoint.com/:i:/g/personal/kxm180046_utdallas_edu/EZtxE-J__fBMmMoRoFyxnJgBYlNbnxVgA4oKmGSa3QyXTA?e=881T6j)

## Example VirusTotal report
[9990527d78700a55d788bd4b3fcbb16b3852027ea722540a00d43544df378053](https://cometmail-my.sharepoint.com/:u:/g/personal/kxm180046_utdallas_edu/EUl6FmubR15CpzFCceY4WPwBqBE6uwNXmlv4w2krsL5pYg?e=yqwC5T)

## Instruction

1. log into any one of the RPi's that you want to use
2. create a new directory in RPi ~/Documents/provGraph/
3. copy and unzip the result_10_20_20.zip to RPi directory ``~/Documents/provGraph/``
    * command in host e.g `scp -r ~/Downloads/result_10_20_20.zip pi@10.176.150.46:~/Documents/provGraph/`
    * unzip in RPi e.g.g `unzip ~/Documents/provGraph/result_10_20_20.zip` 

4. Go inside the results_10_20_20 directory
    * `cd ~/Documents/provGraph/result_10_20_20`

5. for each dir e.g. `busybox`, `chmod`, `rm`, `dash`...
    * open a dir e.g. `cd busybox`
    * create a dir where you will place the provenance graphs (.png) 
        * e.g. `mkdir provGraphs` 
    * create a provenance graph (.png) for each .call file using xdot
        * can do it manually e.g. `xdot -Tpng InputFile.call -o provGraphs/OutputFile.png`
        * or use this script
        ```
        #!/bin/sh

        for file in *.call
        do
          xdot -Tpng "$file" -o "provGraphs/$file.png"
        done
        ```
    * sort the provenance graph (.png) by largest size
        * `cd provGraphs`
        * `ls -lS > provlist.txt`
    * for each provenence graph in the list 
        * open the provenance graph png
        * try to determine it is it interesting. "many nodes and many edges" (see example)
            * try to determine the malware name. The malware name will be inside a node [square share] with the string inside `vt_kunal_{amd/intel}_{1,2,intel32}_malwarehash`
                * You only need the `malwarehash`
                * for non-intersting provGraph malware incomplete hash is `9990527d78700a55d788`
                    * need to find the complete hash from these two files , just search for the string `9990527d78700a55d788`
                        * [malware_listA.txt](https://cometmail-my.sharepoint.com/:t:/g/personal/kxm180046_utdallas_edu/EdN9axzay7VBnhsmqRojR3MBdhvbhAdoFq_e4xcpkfjfZw?e=LqDa58)
                        * [malware_listB.txt](https://cometmail-my.sharepoint.com/:t:/g/personal/kxm180046_utdallas_edu/Eb5FsBAVgOJNsRCN0SDhf1kBq7mcg2ekbCfkZi7gF2QlOA?e=wer3lh)
                        ```
                         $ cat malware_list{A/B}.txt | awk '/9990527d78700a55d788/{print $1}'
                        ```
        * if the provGraph is interesting note the following information: "[dir_name, file_name, malware_name]"
            * Non-interesting ProvGraph example (because easier to understand but you want to do it for the interesting ProvGraph)
                * directory name: e.g. `busybox`
                * file_name: e.g. `61066-processletevent-eventdb_2020_10_08+-747172168.call`
                * malware_name: e.g. `9990527d78700a55d788bd4b3fcbb16b3852027ea722540a00d43544df378053`
    * return to step 5 until all directory inside `results_10_20_20` have been processed

6. VirusTotal analysis
    * BEFORE GOING TO THIS STEP TALK TO DR.JEE or ME
    * downlaod report of interesting malware detected
    ```
    curl -v --request POST \
      --url 'https://www.virustotal.com/vtapi/v2/file/report' \
      -d apikey=$your-api-key \
      -d 'resource=$malware-h' | json_pp > sample.json
      ```
      example:
      ```
      curl -v --request POST \
      --url 'https://www.virustotal.com/vtapi/v2/file/report' \
      -d apikey=<kunal_key> \
      -d 'resource=9990527d78700a55d788bd4b3fcbb16b3852027ea722540a00d43544df378053' | json_pp > sample.json
      ```
    * [reference on how to handle the request](https://www.tines.io/blog/virustotal-api-security-automation?utm_term=&utm_campaign=GO-DTN-ATN-NBR-NBR-EN-ALL-2l-EM-AUT-TOO&utm_source=adwords&utm_medium=ppc&hsa_acc=8712474542&hsa_cam=9814488463&hsa_grp=108440396535&hsa_ad=461474909420&hsa_src=g&hsa_tgt=dsa-947796356153&hsa_kw=&hsa_mt=b&hsa_net=adwords&hsa_ver=3&gclid=CjwKCAjwlbr8BRA0EiwAnt4MTrP-0H5UvFzAPi6DCjQ32lrimiJRxGKthl7woMh-MT7CuhGO5O5A6hoC1OgQAvD_BwE)

###### tags: `arm`,`kunal`,`malware`

`splitbrain`, `malware`, `rpi`