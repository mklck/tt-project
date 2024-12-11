from clientTCP import ClientTCP 
import time


if __name__== "__main__":
    client = ClientTCP();
    client.connectServer();

    while 1:
        if(client.turn == 0):
            client.clientRead();
        
        if(client.turn == 1 ): ## and... tu mozesz dodaj jakas swoja flage ktora zapalasz eventem w GUI...## 
            send_data = input("Podaj wiadomosc:");
            client.clientSend(send_data.encode());
            

        ### twoje GUI....
        
        time.sleep(0.1);        
