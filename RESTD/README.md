# RESTD - Reasoning Engine for Smart Threat Detection
## created by- RSTDED

## Member of RSTDED:Reason based Smart Threat Detection Engine Developers

* Kunal Mukherjee

## How we built it

* first we defined our chosen system entity and relation

```
% entities
system_entity(process).
system_entity(file).
system_entity(socket).

% relation
system_relation(write).
system_relation(read).
system_relation(execute).
system_relation(start).
system_relation(end).

% process and entity relation definition
system_process_relation(X,Y) :- process(X), process(Y).
system_process_relation(X,Y) :- process(X), file(Y). 
system_process_relation(X,Y) :- process(X), socket(Y).
``` 

* we used ground intelligence to code some facts such as what is a secure socket and process

```
trusted_process("apt-get").
untrusted_process("winword.exe").
trusted_socket("192.x.x.x").
untrusted_socket("168.x.x.x").
```

* then we quantized our ground recommendation and justification

```
% message as to why secure
message_trusted_process:-write('Trusted process is in a relation with a trusted process'),nl,fail.
message_trusted_file:-write('Trusted process is in a relation with a file'),nl,fail.
message_trusted_socket:-write('Trusted process is in a relation with a trusted socket'),nl,fail.

% message as to why insecure 
message_mal_process:-write('Unknown process found!'),nl,fail.
message_unauth_file:-write('Unauthorized file access!'),nl,fail.
message_unauth_network:-write('Unauthorized network access!'),nl,fail.

% message for different actions
message_old_browser:-write('Update your browser!'),nl,fail.
message_old_signature_db:-write('Update your signature database!'),nl,fail.
message_network_misuse:-write('Network interface needs to be closed down!'),nl,fail.

% message for different patches
message_patch_1:-write('use patch KB4462137'),nl,fail.
message_patch_2:-write('use patch KB4474419'),nl,fail.
message_patch_3:-write('use patch KB4508433'),nl,fail.
```

* then we added the rules as to when can we consider a system event safe

```
% trusted system process relation
trusted_system_process_process_relation(X,Y) :- 
	system_process_relation(X,Y), trusted_process(X), trusted_process(Y),nl.

trusted_system_process_file_relation(X,Y) :- system_process_relation(X,Y), trusted_process(X), file(Y),nl.

trusted_system_process_network_relation(X,Y) :- system_process_relation(X,Y), trusted_process(X), trusted_socket(Y),nl.
```

* then finally we put the checking predicate and print out the appropriate reasoning and the recommendation

```
% check a system process relation and provide appropriate message
% a unknown/malicious process found
check_system_event(X,Y):-trusted_system_process_process_relation(X,Y)->message_trusted_process; message_mal_process;message_patch_1;message_patch_2.

% check trusted program and file relation
check_system_event(X,Y):-trusted_system_process_file_relation(X,Y)->message_trusted_file; message_unauth_file; message_patch_3.

% check trusted program and socket relation
check_system_event(X,Y):-trusted_system_process_network_relation(X,Y)->message_trusted_socket; message_network_misuse; message_old_browser.
```

##  query and output

```
?- check_system_event("apt-get", "apt-get").

Trusted process is in a relation with a trusted process
false.

?- check_system_event("apt-get", "yy.dat").

Trusted process is in a relation with a file
false.

?- check_system_event("apt-get", "192.x.x.x").

Trusted process is in a relation with a trusted socket
false.

?- check_system_event("apt-get", "bash").
Unknown process found!
use patch KB4462137
use patch KB4474419
false.

?- check_system_event("apt-get", "241.x.x.x").
Network interface needs to be closed down!
Update your browser!
false.

?- check_system_event("curl", "t1.txt").
Unauthorized file access!
use patch KB4508433
false.
```

## Why we built it

**Traditional defenses** such as _signature-based_ and _network-based_ **FAIL** against stealthy attacks such as **zero-day vulnerability** and **malware mutants**. Recent methods of stealthy  attacks happen by **impersonating or abusing well-trusted programs**, where the malicious behavior is blended with benign behaviors of the targeted program. Signature based defenses fail because they have not seen the source code/activity signature before for the zero day attacks and malware mutants. Network based defense fails because firewall and intrusion detection system do not guard well trusted programs as well as user specified exceptions. 

Current on-going work is using an ML technique called **auto-encoders based anomaly detection**. They are first training a model with benign system activity and then uses it to classify system activities with the goal that regular process that have been hijacked by malware will show abnormal system activity that can be identified. There are **three BIG issues** with the ML based threat detection approach that was highlighted by Dr. Gupta during his talk as well, first, the training takes an **huge amount of time as well as resources** and second, the **false positive rates** is moderately high. Thus, a human has to be looped into the deployment pipeline so that they can monitor and release benign processes. But, they can be easily solved if we have some on-ground intelligence as well as using ASP and common sense reasoning. On ground intelligence is well established, and for this project I am using the s(CASP) system to replace the auto-encoder and human intelligence. So, that rather than making a statical decision, we are making a common sense reasoning based decision that has the ability to provide justification. Since, we can get a **justification** as to why some event was classified as benign or malicious, we can **recommend available patches and actions** that the human can take, and if the justification is wrong they can simply **grant exceptions or modify a rule**. Since, there is no need to re-train a NN model(Auto-encoder), they are **saving huge amount of time, energy, and resources (such as money and human intelligence)**. 

The third problem and the most critical issue is that ML based detection is a **black-box methodology** and we get **no justification** as to why a system event was classified as malicious. Since, we get no justification we **cannot** recommend an action: to patch the vulnerability or to mitigate the threat. Also, we have to rely on the human intelligence to decipher why the system event was marked as malicious and in a false positive scenario, either we will have to tune an hyperparameter or re-train the model. In either case, we are **demanding huge time, energy and resources** in terms of processing power, memory, money and additional human intelligence from a different domain (ML). 

**Security domain specific aspect** regarding the third problem  is that when one vulnerability is detected, there is a possibility that there exists **another or multiple similar kind of vulnerability** that is already being or can be **exploited**. Since, we get no justification regarding the detection a security researcher has to **manually hunt them down** and patch it. Even then, there is **no guarantee** that he has tracked down all the similar vulnerability.

**The project goal is that by using our system RESTD the user will be well RESTED in an unfortunate scenario of zero day threat (new malware mutant attack), as they will have the industry certified recommendation(patches and actions) on how to mitigate the threat. Since, a justification is provided, the job of finding similar vulnerabilities is made simpler and a patch can be added to all of them. Thus, we are stopping future exploits and making the system secure and robust.**