import sqlite3 as slt
import numpy as np
import io

def adapt_array(arr):
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return slt.Binary(out.read())
def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)


# Converts np.array to TEXT when inserting
slt.register_adapter(np.ndarray, adapt_array)

# Converts TEXT to np.array when selecting"
slt.register_converter("array", convert_array)



##Add a plotting script
def PlotFrequencies(Frequencies, FitData,target):
    import numpy as np
    import matplotlib.pyplot as plt
    ##add title, increase font sizes
    ## label axes
    plt.figure(figsize=(10,10))
    plt.plot(Frequencies, FitData)
    plt.title('%s'%target, fontsize=18)
    plt.xlabel('Frequencies',fontsize=14)
    plt.ylabel('Y-Yfit', fontsize=14)
    plt.axhline(y=0,ls='--',linewidth=2,c='k')
    plt.show()
        

        
        
        
        


#Loading Data from files you have on YOUR DESKTOP.   
def B1LoadTargetData(target):
    import numpy as np
    print("Loading data for %s Board 1..." %target)
    try:
        destination=target+'/Board1ReducedData.txt'
        print(destination)
        full_data1=np.loadtxt(destination)
        Frequencies1=full_data1[:,0]
        AvgYData1=full_data1[:,1]
        SmoothedData1=full_data1[:,2]
        Velocities1=full_data1[:,3]
        print("Data successfully loaded!")
        print()
    except IOError:
        print("File does not exist")
    return full_data1, Frequencies1, AvgYData1, SmoothedData1, Velocities1

def B2LoadTargetData(target):
    import numpy as np
    print("Loading data for %s Board 2..." %target)
    try:
        destination=target+'/Board2ReducedData.txt'
        print(destination)
        full_data2=np.loadtxt(destination)
        Frequencies2=full_data2[:,0]
        AvgYData2=full_data2[:,1]
        SmoothedData2=full_data2[:,2]
        Velocities2=full_data2[:,3]
        print("Data successfully loaded!")
        print()
    except IOError:
        print("File does not exist")
    return full_data2, Frequencies2, AvgYData2, SmoothedData2, Velocities2

           
        
        
        
#Connection and Checking the db       
        
def connect(database):
    ## When using ConnectDB you MUST format it as cur=ConnectDB
    con = None
    try:
        con= slt.connect("%s"%database, detect_types=slt.PARSE_DECLTYPES)
        cur = con.cursor()
    except Error as e:
        print(e)
    return cur
def TableChecker(cur):
    #This checks to see what tables exist in the database, they are returned as a 
    cur.execute("select name from sqlite_master where type='table'")
    print("The tables present are: \n" , *cur.fetchall(), sep="\n")

    

#Writing data to the database ONLY WORKS IF TABLE DOES NOT ALREADY EXIST  
def AddReducedData(cur, target):
    #Check for table already exists
    full_data1, Frequencies1, AvgYData1, SmoothedData1, Velocities1 = B1LoadTargetData(target)
    full_data2, Frequencies2, AvgYData2, SmoothedData2, Velocities2 = B2LoadTargetData(target)
    try:
        print('Connected to database, will now upload data to specified table...')
        tablename=target+"_ReducedDataBoard1"
        cur.execute("create table "+ tablename +" (freq array, avgY array, smo array, vel array)")
        cur.execute("insert into " + tablename + " (freq, avgY, smo, vel) values (?,?,?,?)" ,
                    (Frequencies1, AvgYData1, SmoothedData1, Velocities1)) #data inserted
        print("Board 1 has been added to database, moving to board 2...")
        print()
        #now we do board2
        tablename2=target+"_ReducedDataBoard2"
        cur.execute("create table "+ tablename2 +" (freq array, avgY array, smo array, vel array)")
        cur.execute("insert into " + tablename2 + " (freq, avgY, smo, vel) values (?,?,?,?)" ,
                    (Frequencies2, AvgYData2, SmoothedData2, Velocities2)) #data inserted
        print('Board 2 has been added to database.')
        print("AddReducedData is complete, committing the changes to db...")
        print()
        cur.connection.commit()
    except slt.Error as error:
        print(error)    
    
    
    
    
    
    
    
### Getting Data from the database   
def GrabReducedData(cur, target, board):
    try:
        print('Connected to database, will now grab data...')
        tablename=target+"_ReducedDataBoard"+"%s"%board
        cur.execute("SELECT * FROM " + "%s"%tablename )##call our data from the database 
        data=cur.fetchone()
        data=np.transpose(data)
        print('data loaded...')
    except slt.Error as error:
        print( error)
        
    return data        
            
    
    
    
#DOING THINGS WITH THE DATA
def QuickFreqPlot(cur,target,board):
    try:
        print('Connected to database, will now grab data...')
        tablename=target+"_ReducedDataBoard"+board
        cur.execute("select * from '%s' "%tablename)##call our data from the database 
        data=cur.fetchone()
        data=np.transpose(data)
        PlotFrequencies(data[0],data[1],'%s'%target)
        print('data loaded...')
    except slt.Error as error:
        print(error)
    