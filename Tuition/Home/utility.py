from .models import *
import csv

def Insertpincode():
    csv_file_path = '../../pincode.csv'
    with open('pincodes.csv', mode ='r')as file:
        print("file found")
        csvFile = csv.reader(file)
        print("Inserting data")
        for lines in csvFile: 
            pin = int(lines[0])
            Devision = lines[1]
            Region = lines[2]
            Circle = lines[3]
            Taluk = lines[4]
            District = lines[5]
            State = lines[6]
            try:    
                pincodes.objects.create(Pincode=pin,Devision=Devision,Region=Region,Circle=Circle,Taluk=Taluk,District=District,State=State)
            except:
                pass
    print("Data inserted")


