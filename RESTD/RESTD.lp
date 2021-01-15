% Kunal Mukherjee
% RESTD.lp
% 1/15/21
% The project goal is that by using our system RESTD
% the user can detect zero day threats, and get an recommendation
% on how to mitigate the threat by applying a patch or by taking an action.

% process
trusted_process("apt-get").
untrusted_process("winword.exe").
untrusted_process("outlook.exe").
untrusted_process("powershell.exe").
untrusted_process("bash").
untrusted_process("wget").
process(X) :- trusted_process(X).
process(X) :- untrusted_process(X).

% file
file("t1.txt").
file("f1.doc").
file("f2.doc").
file("yy.dat").

% socket
trusted_socket("192.x.x.x").
untrusted_socket("168.x.x.x").
socket(X) :- trusted_socket(X).
socket(X) :- untrusted_socket(X).

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

% trusted system process relation
trusted_system_process_process_relation(X,Y) :- 
	system_process_relation(X,Y), trusted_process(X), trusted_process(Y),nl.

trusted_system_process_file_relation(X,Y) :- system_process_relation(X,Y), trusted_process(X), file(Y),nl.

trusted_system_process_network_relation(X,Y) :- system_process_relation(X,Y), trusted_process(X), trusted_socket(Y),nl.

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

% check a system process relation and provide appropriate message
% a unknown/malicious process found
check_system_event(X,Y):-trusted_system_process_process_relation(X,Y)->message_trusted_process; message_mal_process;message_patch_1;message_patch_2.

% check trusted program and file relation
check_system_event(X,Y):-trusted_system_process_file_relation(X,Y)->message_trusted_file; message_unauth_file; message_patch_3.

% check trusted program and socket relation
check_system_event(X,Y):-trusted_system_process_network_relation(X,Y)->message_trusted_socket; message_network_misuse; message_old_browser.


% query for a trusted process with a trusted socket relation
%?-check_system_event("apt-get", "192.x.x.x").

% query for a trusted process with a untrusted socket relation
%?-check_system_event("apt-get", "168.x.x.x").

% query for a trusted process with a file relation
%?- check_system_event("apt-get", "t1.txt").

% query for a untrusted process with a file relation
%?- check_system_event("wget", "t2.txt").

