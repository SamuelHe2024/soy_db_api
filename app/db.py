import psycopg2
import os
DATABASE_URL = "postgres://tbptunbssokuks:df66dff65cf6af8223a6696a4aa8a0f22aaefbe8ef3dc6accd643a5e64d9abd7@ec2-3-223-213-207.compute-1.amazonaws.com:5432/da38dpv7bfap34"
############################ DRY WEIGHT FUNCTIONS ############################
#INPUTS:
#solution: string
#dry_weight: float
def insert_dry_weight(solution,dry_weight):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO dry_weight (solution, dry_weight)" +
                   " VALUES(%s,%s)",
                   (solution,dry_weight))

    conn.commit()
    count = cursor.rowcount

    print(count, "Record inserted successfully into table")
    cursor.close()
    conn.close()

def get_dry_weight():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    

    cursor.execute("SELECT * FROM dry_weight")
    
    conn.commit()

    values = cursor.fetchall()
    cursor.close()
    conn.close
    return values

############################ WATER UPTAKE FUNCTIONS ############################
#INPUTS:
#solution: string (varchar)
#uptake_amount: float
#uptake_date: date     date format: yyyy-mm-dd
def insert_water_uptake(solution,uptake_amount,uptake_date):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO water_uptake (solution, uptake_amount, uptake_date)" +
                   " VALUES(%s,%s,%s)",
                   (solution,uptake_amount,uptake_date))

    conn.commit()
    count = cursor.rowcount

    print(count, "Record inserted successfully into table")
    cursor.close()
    conn.close()

def get_water_uptake():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    

    cursor.execute("SELECT * FROM water_uptake")
    
    conn.commit()

    values = cursor.fetchall()
    cursor.close()
    conn.close
    return values


############################ IMAGE DATA FUNCTIONS ############################
#INPUTS:
#image_name: string (varchar)
#solution: string (varchar)
#day_prediction: string (varchar)
#image_url: string (varchar)
#segmented_image_url: string (varchar)
def insert_image_data(image_name,day_prediction,image_url,segmented_image_url, accuracy):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO image_data (image_name, day_prediction, image_url, segmented_image_url, accuracy)" +
                   " VALUES(%s,%s,%s,%s,%s)",
                   (image_name,day_prediction,image_url,segmented_image_url, accuracy))

    conn.commit()
    count = cursor.rowcount

    print(count, "Record inserted successfully into table")
    cursor.close()
    conn.close()

def get_image_data():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    

    cursor.execute("SELECT * FROM image_data")
    
    conn.commit()

    temp = cursor.fetchall()
    cursor.close()
    conn.close
    return temp

def get_image(image_id):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM image_data WHERE id = '" + image_id + "'")
    conn.commit()
    temp = cursor.fetchall()
    values = [temp[0][0], temp[0][1], temp[0][2], temp[0][3], temp[0][4], temp[0][5], temp[0][6]]

    print(temp)
    return values

############################ SOLUTION DATA FUNCTIONS ############################
#INPUTS:
#A LOT
def insert_solution_data(solution, Calcium, Magnesium, Sodium, Potassium, Boron, CO_3, HCO_3, SO_4, 
                         Chlorine, NO3_n, Phosphorus, pH, Conductivity, SAR, Iron, Zinc, Copper, Manganese, Arsenic, 
                         Barium, Nickel, Cadmium, Lead, Chromium, Fluorine, Cb):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO solution_data (solution, calcium, magnesium, sodium, potassium, boron, co_3, hco_3, so_4," +
                   "chlorine, no3_n, phosphorus, ph, conductivity, sar, iron, zinc, copper, manganese, arsenic,"+
                   "barium, nickel, cadmium, lead, chromium, fluorine, cb)"+
                   " VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                   (solution, Calcium, Magnesium, Sodium, Potassium, Boron, CO_3, HCO_3, SO_4, 
                         Chlorine, NO3_n, Phosphorus, pH, Conductivity, SAR, Iron, Zinc, Copper, Manganese, Arsenic, 
                         Barium, Nickel, Cadmium, Lead, Chromium, Fluorine, Cb))

    conn.commit()
    count = cursor.rowcount

    print(count, "Record inserted successfully into table")
    cursor.close()
    conn.close()

def get_solution_data():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    

    cursor.execute("SELECT * FROM solution_data")
    
    conn.commit()

    values = cursor.fetchall()
    cursor.close()
    conn.close
    return values