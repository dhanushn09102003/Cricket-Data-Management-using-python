import mysql.connector as sql
con=sql.connect(host="localhost",user="root",password="sqladmin123*")
cur=con.cursor(buffered=True)
cur.execute("create database if not exists T20Wc")
cur.execute("use T20WC")

while True:
    print("=="*40)
    print()
    print("1.Add new scorecard")
    print("2.View old scorecard")
    print("3.Stats")
    print("4.Exit")
    print("=="*40)
    print("\n"*2)
    c=int(input("Enter operation to perform:"))
    print()


    def strikerate(r,b):
        if b!=0:
            sr=round(r/b*100,2)
        else:
            sr=0
        return sr
    
    def economy(r,o):
        o=float(o)
        b=(int(o)*6)+((o-int(o))*10)
        if b!=0:
            eco=round(int(r)/b*6,1)
        else:
            eco=0
        return eco
    
    
    def addnew():
        cur.execute("create table if not exists batrecords (Name varchar(25),Team varchar(20),Runs int,Matches int)")
        cur.execute("create table if not exists bowlrecords(Name varchar(25),Team varchar(20),Wickets int,Matches int)")
        
        t1name=input("Enter first team name:")
        t2name=input("Enter second team name:")
        print("\n"*2)
        print("=="*40)

        match=t1name+"_vs_"+t2name

        f=open("database.txt","a+")
        f.write(match+"\n")
        f.flush()
        f.close()


        def t1names():
            print("ENTER PLAYER NAMES OF",t1name)
            print()
            for i in range (1,12):
                n=input("Player "+str(i)+" :")
                t1bat.append([n])
                t1bowl.append([n])
        

        def t2names():
            print("ENTER PLAYER NAMES OF",t2name)
            print()
            for i in range (1,12):
                n=input("Player "+str(i)+" :")  
                t2bat.append([n])
                t2bowl.append([n])


        def details(team1name,team2name,batlist,bowllist,tg):
            print("Enter runs scored and balls faced by each batsman with a single space")
            print()
            for i in range(11):
                n=batlist[i][0]
                r,b=input(n+":").split()
                r,b=int(r),int(b)
                sr=strikerate(r,b)
                batlist[i].extend([r,b,sr])

            tname=match+team1name+"bat"
            cur.execute("create table if not exists {} (Name varchar(25),Runs int,Balls int,Strike_rate float)".format(tname))

            for i in range(11):
                n,r,b,sr=batlist[i][0],batlist[i][1],batlist[i][2],batlist[i][3]
                cur.execute("insert into {} values ('{}',{},{},{})".format(tname,n,r,b,sr))
                con.commit()
                        
            print()
            extras=int(input("Extras:"))
            cur.execute("insert into {} (Name,Runs) values('EXTRAS',{})".format(tname,extras))
  

            cur.execute("Select Name from batrecords")
            d=cur.fetchall()
            storednames=[]
            for names in d:
                storednames.append(names)

            if team1name=="t1":
                namet1=t1name
                namet2=t2name
            else:
                namet1=t2name
                namet2=t1name

                
            for i in range(11):##
                n,r=batlist[i][0],batlist[i][1]
                tn=(n,)
                if tn not in storednames:
                    cur.execute("insert into batrecords values('{}','{}',{},1)".format(n,namet1,r))
                    con.commit()
        
 
                else:
                    cur.execute("update batrecords set runs=runs+{},matches=matches+1 where name='{}'".format(r,n))
                    con.commit()

            print("Enter runs conceded,overs bowled,wickets taken by each bowler with single space") 
            print()
            for i in range(11):
                rg,ob,wt=input(bowllist[i][0]+":").split()
                eco=economy(rg,ob)
                bowllist[i].extend([ob,rg,wt,eco])
        
            tname=match+team2name+"bowl"
            cur.execute("create table if not exists {} (Name varchar(25),Overs float,Runs int,Wickets int,Economy float)".format(tname))

            for i in range(11):
                n,ob,rg,wt,eco=bowllist[i][0],bowllist[i][1],bowllist[i][2],bowllist[i][3],bowllist[i][4]
                cur.execute("insert into {} values ('{}',{},{},{},{})".format(tname,n,ob,rg,wt,eco))
                con.commit()

            print()
            runouts=int(input("Enter no. of runouts:"))
            cur.execute("insert into {} (Name,Wickets ) values('RUNOUTS',{})".format(tname,runouts))
            con.commit()

            cur.execute("Select Name from bowlrecords")
            d=cur.fetchall()
            storednames=[]
            for names in d:
                storednames.append(names)


            for i in range(11):##
                n,w=bowllist[i][0],bowllist[i][3]
                tn=(n,)
                if tn not in storednames:
                    cur.execute("insert into bowlrecords values('{}','{}',{},1)".format(n,namet2,w))
                    con.commit()

                else:
                    cur.execute("update bowlrecords set wickets=wickets+{},matches=matches+1 where name='{}'".format(w,n))
                    con.commit()
            


            #rpo
            r=0
            print("\n"*2)
            for i in range(1,21):
                x=int(input("Enter runs scored in over: "+str(i)+":"))
                r+=x
                tg.append(r)

            print("\n"*2)              

        t1bat,t2bat=[],[]
        t1bowl,t2bowl=[],[]
        t1g,t2g=[],[]

        t1names()
        print("=="*40)
        print()
        t2names()
        print("=="*40)
        print()


        toss=input("Toss Won by:")
        choice=input("Opted to(bat/bowl):")
        print()
        
        f=open(match+".txt","w")
        f.write(t1name+"\n")
        f.write(t2name+"\n")
        f.write(toss+"\n")
        f.write(choice)
        f.close()


        if (toss==t1name and choice=="bat") or (toss==t2name and choice=="bowl"):
            print("="*34,"1st INNINGS","="*34)
            details("t1","t2",t1bat,t2bowl,t1g)
            print("="*34,"2nd INNINGS","="*34)
            details("t2","t1",t2bat,t1bowl,t2g)
    


        elif (toss==t1name and choice=="bowl") or (toss==t2name and choice=="bat"):
            print("="*34,"1st INNINGS","="*34)
            details("t2", "t1",t2bat,t1bowl,t2g)
            print("="*34,"2nd INNINGS","="*34)
            details("t1","t2",t1bat,t2bowl,t1g)

        else:
            print("Invalid input")


        listg=[t1g,t2g]
        import pickle
        fg=open(match+".dat","wb")
        pickle.dump(listg,fg)
        f.close()

        print("Scorecard successfully added")
        print("=="*40)
        print("\n"*2)
    


    if c==1:
        addnew()

    if c==2:
        print()
        print("Stored match details")
        print()
        f=open("database.txt","r")
        matches=f.read()
        print(matches)
        mat=input("Enter match name to view details(as mentioned above):")
        print()
        while True:
            print("1.View scorecard")
            print("2.View over rate graph")
            print("3.Top performers")
            print("4.Main menu")
            print()
        
            c2=int(input("Enter operation to perform:"))
            print("\n"*2)

            f1=open(mat+".txt","r")#Hometeam,Awayteam,Toss,Choice
            import pickle
            fg=open(mat+".dat","rb+")#Over wise run data
            t1name=f1.readline().strip()
            t2name=f1.readline().strip()
            toss=f1.readline().strip()
            choice=f1.readline().strip()

            
            def battingtable(data):
                c=1
                for l in data:
                    print(l[0].ljust(20)+str(l[1]).ljust(8)+str(l[2]).ljust(8)+str(l[3]))
                    if c==1:
                        print("="*60)
                    c+=1
                      

            def bowlingtable(data):
                c=1
                for l in data:
                    print(l[0].ljust(20)+str(l[1]).ljust(8)+str(l[2]).ljust(8)+str(l[3]).ljust(8)+str(l[4]))
                    if c==1:
                        print("="*60)
                    c+=1            

            def scorecard(t1name,t2name):
                print()
                cur.execute("select sum(Runs) from {}".format(mat+t1name+"bat"))
                score=cur.fetchall()
                for i in score:
                    totscorelist=i
                    for i in totscorelist:
                        totscore=int(i)
                        break            

                cur.execute("select sum(wickets) from {}".format(mat+t2name+"bowl"))
                wickets=cur.fetchall()
                for i in wickets:
                    totwicketslist=i
                    for i in totwicketslist:
                        totwickets=int(i)
                        break

                cur.execute("select * from {}".format(mat+t1name+"bat"))
                batscorecard=cur.fetchall()

                tab=[("Batter","R","B","SR")]
                for row in batscorecard:
                    tab.append(list(row) )

                tab[-1][2],tab[-1][3]="",""

                battingtable(tab)

                print("Total:",totscore,"-",totwickets)
                scores.extend([totscore,totwickets])
                print("__"*30)
                print("\n"*2)           

            
                cur.execute("select * from {} where overs<>0".format(mat+t2name+"bowl"))
                bowlscorecard=cur.fetchall()
            
                tab=[("Bowler","O","R","W","ER")]
                for row in bowlscorecard:
                    tab.append(list(row))            


                bowlingtable(tab)

                print("__"*30)
                print("\n"*2)
                
            
            def result(l):#####
                if (toss==t1name and choice=="bat") or (toss==t2name and choice=="bowl"):
                    if l[0]>l[2]:
                        print("RESULT:",t1name,"won by",l[0]-l[2],"runs")
                    else:
                        print("RESULT:",t2name,"won by",10-l[3],"wickets")
                else:
                    if l[0]>l[2]:
                        print("RESULT:",t2name,"won by",l[0]-l[2],"runs")
                    else:
                        print("RESULT:",t1name,"won by",10-l[3],"wickets")
            

            if c2==1:
                print("Toss won by",toss,"and choosed to",choice,"first")######
                print()
                scores=[]#Innings 1-total,wickets,  innings 2-total,wickets
                if (toss==t1name and choice=="bat") or (toss==t2name and choice=="bowl"):
                    print("Innings 1")
                    print()
                    print(t1name)
                    scorecard("t1","t2")
                    print("\n"*5)
                    
                    
                    print("Innings2")
                    print()
                    print(t2name)
                    scorecard("t2","t1")

                elif (toss==t1name and choice=="bowl") or (toss==t2name and choice=="bat"):
                    print("Innings 1")
                    print()
                    print(t2name)
                    scorecard("t2","t1")
                    print("\n"*5)
                    
                    print("Innings2")
                    print()
                    print(t1name)
                    scorecard("t1","t2")            
            
                result(scores)
                print("\n"*2)            

            if c2==2:
                import matplotlib.pyplot as m
                data=pickle.load(fg)

                overs=list(range(1,21))
                t1or=data[0]
                t2or=data[1]
                m.plot(overs,t1or,label=t1name,linewidth=5)
                m.plot(overs,t2or,label=t2name,linewidth=5)


                m.legend()
                m.xlabel('Overs')
                m.ylabel('Runs')
                m.title('Over Rate Graph')
                m.show()

                print("\n"*3)


            if c2==3:
                def topperformers(tname):
                    print("Batting")
                    print()
                
                    cur.execute("select * from {} where balls<>0 order by runs desc,balls".format(mat+tname+"bat"))
                    batting=cur.fetchmany(3)
                    topscorers=[("Batter","R","B","SR")]
                    for i in batting:
                        topscorers.append(i)

                    battingtable(topscorers)
                    print("\n"*2)
                    
                    print("Bowling")
                    print()
                
                    cur.execute("select * from {} where name<>'runouts' order by wickets desc,economy".format(mat+tname+"bowl"))
                    bowling=cur.fetchmany(3)
                    topwickettakers=[("Bowler","O","R","W","ER")]
                    for i in bowling:###
                        topwickettakers.append(i)
                    bowlingtable(topwickettakers)


                    print("\n"*3)

                print(t1name)
                topperformers("t1")
                print("__"*40)
                print()
                print(t2name)
                topperformers("t2")

                

            
            if c2==4:
                break

    if c==3:
        while True:
            print("1.Most Runs")
            print("2.Most Wickets")
            print("3.Main Menu")
            print()

            c3=int(input("Enter operation to perform:"))
            print("\n"*2)

            def table(data):
                c=1
                for l in data:
                    print(l[0].ljust(20)+str(l[1]).ljust(15)+str(l[2]).ljust(12)+str(l[3]))
                    if c==1:
                        print("="*60)
                        c+=1
                print("__"*35)
                print()
                    
            if c3==1:
                print("-"*25+"TOP RUN SCORERS"+"-"*25)
                print("\n"*2)

                cur.execute("select * from batrecords order by runs desc")
                batting=cur.fetchmany(10)
                topscorers=[("Batter","Team","Runs","Matches")]
                for i in batting:
                    topscorers.append(i)

                table(topscorers)
            
            if c3==2:
                print("-"*25+"TOP WICKET TAKERS"+"-"*25)
                print("\n"*2)
                cur.execute("select * from bowlrecords order by wickets desc")
                bowling=cur.fetchmany(10)
                topwickettakers=[("Bowler","Team","Wickets","Matches")]
                for i in bowling:
                    topwickettakers.append(i)

                table(topwickettakers)
                
            if c3==3:
                break
            
        
                
    if c==4:
        print("Thank You")
        break
 
