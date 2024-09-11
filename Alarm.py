import datetime
import winsound

def alarm(timing):
    t= str(datetime.datetime.now().strptime(timing,"%I:%M %p"))
    t = t[11:16]
    
    hreal= t[:2]
    
    minreal= t[3:5]
   
    
    print(f"Done, alarm is set for {timing}")
    
    while True:
        time= str(datetime.datetime.now().time())
        
        if  hreal == (time[0:2]):
            if minreal== (time[3:5]):
                print("alarm is running")
                winsound.PlaySound('abc',winsound.SND_LOOP)
            elif minreal < (time[3:5]):
                break;
                
             
        