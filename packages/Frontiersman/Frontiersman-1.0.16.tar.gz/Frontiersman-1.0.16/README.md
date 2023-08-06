# CSI4930 Frontiersman

A clone of Settlers of CATAN (base game, 1-4 players local multiplayer)
The game rules are included in the Help Doc.pdf

## README Requirements for class

Gitlab Link: [https://gitlab.com/csi4930-frontiersman/csi4930-frontiersman](https://gitlab.com/csi4930-frontiersman/csi4930-frontiersman)

Package Name on PyPI: Frontiersman

Executable Line to Run Server: FMServer 127.0.0.1 1233

Executable Line to Run Clients: FMClient 127.0.0.1 1233 Zander 1

## Notes

FMServer args are host IP and port  

FMClient args are address, port, name, and the number of players 

The client and each server needs to be on a different ubuntu terminal

127.0.0.1 is for the local host IP, and the port number has to be available on your computer, we used 1233

The client's IP must match the server's  

Run the client line for each player, so for one player:  

>FMServer 127.0.0.1 1233  

>FMClient 127.0.0.1 1233 ZanderK 1

For two players:

>FMServer 127.0.0.1 1233  

>FMClient 127.0.0.1 1233 ZanderK 2

>FMClient 127.0.0.1 1233 StephenW 2

For three players:

>FMServer 127.0.0.1 1233 

>FMClient 127.0.0.1 1233 ZanderK 3

>FMClient 127.0.0.1 1233 StephenW 3

>FMClient 127.0.0.1 1233 BrianS 3

For four players:

>FMServer 127.0.0.1 1233 

>FMClient 127.0.0.1 1233 ZanderK 4

>FMClient 127.0.0.1 1233 StephenW 4

>FMClient 127.0.0.1 1233 BrianS 4

>FMClient 127.0.0.1 1233 MichaelH 4