import psycopg2
# import os
#DATABASE_URL = os.environ('DATABASE_URL')
DATABASE_URL = 'postgres://tbptunbssokuks:df66dff65cf6af8223a6696a4aa8a0f22aaefbe8ef3dc6accd643a5e64d9abd7@ec2-3-223-213-207.compute-1.amazonaws.com:5432/da38dpv7bfap34'

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

    for row in values:
        print("solution = " + row[1])
    cursor.close()
    conn.close
    return values

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

#INPUTS:
#image_name: string (varchar)
#solution: string (varchar)
#day_prediction: string (varchar)
#image_data: bytea
#segmented_image: bytea
def insert_water_uptake(image_name,solution,day_prediction,image_data,segmented_image):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO water_uptake (image_name, day_prediction, image_data, segmented_image, solution)" +
                   " VALUES(%s,%s,%s,%s,%s)",
                   (image_name,day_prediction,image_data,segmented_image,solution))

    conn.commit()
    count = cursor.rowcount

    print(count, "Record inserted successfully into table")
    cursor.close()
    conn.close()

get_dry_weight()