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
trusted_system_process_relation(X,Y) :- system_process_relation(X,Y), trusted_process(X), trusted_process(Y).
trusted_system_process_relation(X,Y) :- system_process_relation(X,Y), trusted_process(X), file(Y).
trusted_system_process_relation(X,Y) :- system_process_relation(X,Y), trusted_process(X), trusted_socket(Y).

% recommendation for different threat detected


% query a relation and if false give recommendation
?- trusted_system_process_relation("apt-get", "t1.txt").
