import datetime
import pickle 


def find():
    f= open("birthday.dat","rb")
    try:
        while True:
            
            y= pickle.load(f)
            
            c= y[1]
            x= str(datetime.datetime.now().date())
            if c[5:7] == x[5:7]:
                
                if c[-2:] == x[-2:]:
                    print(y)
                    return y[0]
                
                    
           
    except EOFError:
        f.close()   

 

def add_birth():
    f= open("birthday.dat","ab")
    name= input("Enter name:")
    dat= input("Enter Date of Birth")
    l= [name,dat]
    pickle.dump(l,f) 
   
    

    