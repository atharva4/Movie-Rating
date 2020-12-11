# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 12:14:53 2020

@author: Atharva
"""


#First add movie to the database using Admin-LOGIN
#label1.config(text=roomtype)
        #label2.config(text=roomNo)

import mysql.connector as mysqLtor
import tkinter.messagebox
import pandas as pd
import matplotlib.pyplot as plt

mycon=mysqLtor.connect(user='root',passwd='',host='localhost',charset='utf8',use_pure=True)#
cursor=mycon.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS movierating")
cursor.execute("USE movierating")
cursor.execute("CREATE TABLE IF NOT EXISTS user(user_name VARCHAR(20),user_email VARCHAR(30),user_pass INT(10))")
cursor.execute("CREATE TABLE IF NOT EXISTS movie(movie_id INT(3) UNIQUE,movie_name VARCHAR(40))")
cursor.execute("CREATE TABLE IF NOT EXISTS rate(movie_name VARCHAR(40),total_users_rated INT(10),avg_ratings FLOAT(2))")

f=0

while(True):
    if f==0:
        
        print("\t\t\t*******MOVIE RATINGS**********")
        print("")
        print("================================================================ ")
        print("\t\t __                  __   __  __")
        print("\t\t __  __          __       __     __")
        print("\t\t         __  __           __  __")
        print("\t\t __                  __   __     __")
        print("\t\t __                  __   __       __")
        print("\t\t __                  __   __         _")
        print("================================================================ ")
        print("\t\t")
        print("")
        print("\t\t 1.REGISTER YOURSELF")
        print("\t\t 2.LOG IN AND RATE MOVIE")
        print("\t\t 3.MOVIE RATINGS")
        print("\t\t 4.RATINGS GRAPH")
        print("\t\t 5.ADMIN-LOGIN")#to add new movie
        print("\t\t 6.ABOUT US")
        print("\t\t 7.Exit")
        
        num=int(input("ENTER YOUR CHOICE :"))
        
    if(num==1):
        
        print("Fill all information")
        name=input("Enter Name:")
        email=input("Enter E-mail:")
        pwd=int(input("Enter Password(Only in Numerics:)"))
        pwd1=int(input("Re-Enter Password:"))
         
        if pwd==pwd1:
            cursor.execute("INSERT INTO user(user_name,user_email,user_pass) VALUES('{}','{}',{})".format(name,email,pwd))
        else:
            #print("Password Do Not Match. Please Press 1 and Create Account Again")
            tkinter.messagebox.showwarning("Warning","Password Do Not Match")
            
        mycon.commit()
        
        print("Account Succesfully Made")
        
    if(num==2):
        
        email=input("Enter Email:")
        pwd2=int(input("Enter Password:"))
        cursor.execute("SELECT * FROM user WHERE user_email='{}' and user_pass={}".format(email,pwd2))
        d1=cursor.fetchall()
        a1=cursor.rowcount
        
        if a1>0:

            #try:
                
                movieName=input("Enter Movie Name You Want To Rate:")
                
                
                cursor.execute("SELECT movie_name FROM movie")
                f=cursor.fetchall()#fetches all the movie_name from table movie and stores it in f
                
                l=[]
                for k in range(len(f)):
                    print(f[k])  # Can also try this for fetching values
                l=f[k]
                print(l)
                    
                if movieName not in a:# if you try fetching using for loop replace f with k
                    print(movieName,"not in",f)
                    
                                    
                ratings=float(input("Enter Rating(Values Between 1 to 10):"))
    
                cursor.execute("SELECT total_users_rated FROM rate WHERE movie_name='{}'".format(movieName))
                b=cursor.fetchone()
                
                #avg_rating=ratings by all users/total users 
                
                current_count=0
                current_rating=0
                
                for current_count in b:
                    count=current_count+1 #increasing the count of total users to calculate the ne avg. rating
                    #print("total users:",count)
                
                cursor.execute("SELECT avg_ratings FROM rate WHERE movie_name='{}'".format(movieName))
                e=cursor.fetchone()
                
                for current_rating in e:
                    current_rating
                    #print("current rating:",current_rating)
                
                avgRate= current_rating + ((ratings-current_rating)/count)#Calculating New rating after every new input
                
                print("New Rating: %1.1f"%avgRate)
                
                cursor.execute("UPDATE rate SET total_users_rated={} WHERE movie_name='{}'".format(count,movieName))
                cursor.execute("UPDATE rate SET avg_ratings={:.1f} WHERE movie_name='{}'".format(avgRate,movieName))
                mycon.commit()
                print("Thanks For Rating!")
                
            #except:
                print("Sorry! Movie is not in the Database")
            
        else:
            #print("Incorrect Password")
            tkinter.messagebox.showwarning("Warning","Incorrect Password Or E-mail")
            
            break
            
    if(num==3):
        
        try:

            movieName2=input('Enter Movie Name:')
            cursor.execute("SELECT avg_ratings FROM rate WHERE movie_name='{}'".format(movieName2))
            showRate=cursor.fetchone()
            for i2 in showRate:
                print("Ratings:",i2)
                
        except:
            print("Sorry! Movie is not in the Database")
            
    if(num==4):
        cursor.execute("SELECT movie_name,avg_ratings FROM rate")
        f3=cursor.fetchall()
        df=pd.DataFrame(f3,columns=['movie_name','ratings'])
        moviename= df['movie_name'].tolist()
        movierating= df['ratings'].tolist()
        plt.bar(moviename,movierating)
        plt.xlabel('Movie Names')
        plt.ylabel('Ratings')
        plt.title('Movie Ratings')
        plt.xticks(rotation=90)
        plt.ylim(0,10)
        plt.show()
    
    if(num==5):
        
        print("\t\t\t Admin-LOGIN")
        ADMINId=int(input("Enter Your Admin-Id:"))
        pname=input("Enter Name:")
        PASS=int(input("Enter Your Password:"))
        pname1="movie"
        PASS1=121
        if pname==pname1 and PASS==PASS1:
            #Admin can only add and delete movie here
            cursor.execute("SELECT * FROM movie")
            f=cursor.fetchall()
            rcount2=cursor.rowcount
            
            ch2=input("Do you want to ADD or DELETE a movie? Press A to ADD and D to Delete:")
            
            if ch2=='A':
                num_add=int(input("How many movie you want to add:"))
                i=0
                
                while i<num_add:
                    
                    add_id=int(input("Enter Movie Id:"))
                    add_name=input("Enter Movie Name:")
                    add_rating=float(input("Enter Movie Rating:"))
                    
                    cursor.execute("INSERT into rate(movie_name,total_users_rated,avg_ratings) VALUES('{}',{},{})".format(add_name,1,add_rating))
                    cursor.execute("INSERT into movie(movie_id,movie_name) VALUES({},'{}')".format(add_id,add_name))
                    rcount2=rcount2+1
                    mycon.commit()
                    print("New Movie Added")
                    i+=1
                    
                break
                
            if ch2=='D':
                num_del=int(input("How many movie you want to Delete:"))
                j=0
                
                while j<num_del:
                    
                    del_name=input("Enter Movie Name You Want to Delete:")
                    cursor.execute("DELETE FROM movie WHERE movie_name='{}'".format(del_name))
                    cursor.execute("DELETE FROM rate WHERE movie_name='{}'".format(del_name))
                    rcount2=rcount2-1
                    mycon.commit()
                    j+=1
                    
                break    
                           
        else:
            #print("Wrong Name or Password ")
            tkinter.messagebox.showwarning("Warning","Wrong Name or Password")
                
    if(num==6):
        
        print("Made By : Atharva Dattatreya")
        print("Sun Computers: BATCH 2019-20")
        
    if(num==7):
        break
    
    


               
       
            
        
        
        
            
        
            
            
    
