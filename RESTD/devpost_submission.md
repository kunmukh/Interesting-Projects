## Inspiration

**Traditional defenses** such as _signature-based_ and _network-based_ **FAIL** against stealthy attacks such as **zero-day vulnerability** and **malware mutants**. Recent methods of stealthy  attacks happen by **impersonating or abusing well-trusted programs**, where the malicious behavior is blended with benign behaviors of the targeted program. Signature based defense fail because they have not seen the source code/activity signature before for the zero day attacks and malware mutants. Network based defense fails because firewall and intrusion detection system do not guard well trusted programs as well as user specified exceptions. 

Current on-going work is using an ML technique called **auto-encoders based anomaly detection**. They are first training a model with benign system activity. And then using it to classify system activities with the goal that regular process that have been hijacked by malware will show abnormal system activity that can be identified. There are **three BIG issues** with the ML based threat detection approach that was highlighted by Dr. Gupta during his talk as well, first, the training takes an **huge amount of time as well as resources** and second, the **false positive rates** is moderately high. Thus, a human has to be looped into the deployment pipeline so that they can monitor and release benign processes. The third problem and the most critical issue is that ML based detection is a black-box methodology and we get **no justification** as to why a system event was classified as malicious. But, they can be easily solved it we have some on-ground intelligence as well as using ASP and common sense reasoning. On ground intelligence is well established, and for this project I am using the s(CASP) system to replace the auto-encoder and human intelligence. So, that rather than making a statical decision, we are making a common sense reasoning based decision that has the ability to provide justification. Since, we can get a **justification** as to why some event was classified as benign or malicious, we can **recommend available patches and actions** that the human can take, and if the justification is wrong they can **grant exceptions or modify a rule**. 

**The project goal is that that by using our system RESTD the user in an unfortunate scenario of zero day or new malware mutant attack detection, they will be well RESTED as they will have the justification as to why the event was classified as a threat and will have a list of recommended patches and actions available to them for mitigation.**

## What it does

## How we built it

## Challenges we ran into
* there are lot if entities and relationships in a system. And defining the rules for them will take a long time. So, we used ground truth to select a sub-set of entities and relations, so that we can build a robust and working solution
* how to define good rules based on established ground truth as well as trying to stay away from circular logic
* how to define rules that have priority, so that one rule supersedes another
* implementing the rules that can be used for detection, so that an ML technique auto-encoder can be replaced

## Accomplishments that we are proud of and what we learned
* how we were able to better a ML technique using ASP 
* show statical detection can be bested by common sense reasoning if we are able to define the facts and rules in a proper way
* we learned s(CASP) system as well as prolog
* how common sense answer set programming can be used to cut human from a pipeline and streamline the process
* how ground truths can be used to better establish facts and constants

## What's next for RESTD - Reasoning Engine for Smart Threat Detection
* we want to define more entities and relationships such as virtual network, virtual interface, and virtual broadcast address handling
* host the RESTD engine on AWS so that anyone can use it to classify their system event or use it for detection