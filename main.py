#!/usr/bin/python3
import xlrd
import fixCity
import dbConnect
import sys

def main():
    xlsPath = ['kontratat/Ferizaj/2011.xls', 'kontratat/Ferizaj/2012.xls', 'kontratat/Ferizaj/2013.xls', 'kontratat/Ferizaj/2014.xls', 'kontratat/Gjakove/2011.xls', 'kontratat/Gjakove/2012.xls', 'kontratat/Gjakove/2013.xls', 'kontratat/Gjakove/2014.xls', 'kontratat/Prishtine/2011.xls', 'kontratat/Prishtine/2012.xls', 'kontratat/Prishtine/2013.xls', 'kontratat/Prishtine/2014.xls', 'kontratat/Gjilan/2011.xls', 'kontratat/Gjilan/2012.xls', 'kontratat/Gjilan/2013.xls', 'kontratat/Gjilan/2014.xls', 'kontratat/Viti/2011.xls', 'kontratat/Viti/2012.xls', 'kontratat/Viti/2013.xls']

# Connect to database
    if not dbConnect.connect():
        print("Couldn't connect to database")
        sys.exit()

# Curious to know how many contracts are there
    totalContracts = 0

    for xls in xlsPath:
        print("Current XLS: " + xls)
        firstRow = 1
        firstColumn = 0

        workbook = xlrd.open_workbook(xls)
        worksheet = workbook.sheet_by_index(0)

        # Find worksheet's start row index
        for i in range(1, 50):
            # Check if the current cell is an instance of float so we can find the starting row
            if isinstance(worksheet.cell(i, 2).value, float):
                firstRow = i + 1
                print("First row: " + str(i + 1))
                break

        # Find worksheet's start column index
        for i in range(3, 20):
                # Find the first instance of string (contract name) I hope the string wont be higher than columns 20 lel
            if isinstance(worksheet.cell(firstRow, i).value, str):
                firstColumn = i
                print("First column: " + str(firstColumn))
                break
                print(xls)

        id = 1

        # HARD-CODING all these numbers sucks gotta fix em later
        for i in range(firstRow, 500): # Check till the 500th row, change if there are potentially more
            project = worksheet.cell(i, firstColumn).value
            date = worksheet.cell(i, firstColumn + 1).value
            estimatedCost = worksheet.cell(i, firstColumn + 2).value
            cost = worksheet.cell(i, firstColumn + 3).value
            annexCost = worksheet.cell(i, firstColumn + 4).value
            contractor = worksheet.cell(i, firstColumn + 5).value
            cLocation = worksheet.cell(i, firstColumn + 6).value
            isLocal = worksheet.cell(i, firstColumn + 7).value

            # Viti has different syntax
            if 'Viti/2011.xls' in xls or 'Viti/2012.xls' in xls or 'Viti/2013.xls' in xls or 'Viti/2014.xls' in xls:
                estimatedCost = worksheet.cell(i, firstColumn + 3 + 2).value
                cost = worksheet.cell(i, firstColumn + 3 + 3).value
                annexCost = worksheet.cell(i, firstColumn + 3 + 4).value
                contractor = worksheet.cell(i, firstColumn + 3 + 5).value
                cLocation = worksheet.cell(i, firstColumn + 3 + 6).value
                isLocal = worksheet.cell(i, firstColumn + 3 + 7).value

            # Check if it got at the EOF then break
            if project == '' or project.lower() == "totali :":
                break
            if annexCost == '':
                annexCost = 0.0

                # Fix city
            cLocation = fixCity.fixCityName(cLocation)

            # Formatting
            # Project
            project = project.replace('”', '')
            project = project.replace('“', '')
            project = project.replace('"', '')

            # Contractor
            contractor = contractor.replace('”', '')
            contractor = contractor.replace('“', '')
      
            contractor = contractor.replace('"', '')
            contractor = contractor.replace("'", '')

            #print("Emri i kontrates: " + project)
            #print("Data: " + str(date))
            #print("Vlera e paramenduar: " + str(estimatedCost))
            #print("Vlera e shpenzuar: " + str(cost))
            #print("Vlera e aneks kontrates: " + str(annexCost))
            #print("Punekryesi: " + str(contractor))
            #print("Lokacioni i punekryesit: " + str(cLocation))
            #print("Vendore: " + str(bool(isLocal)) + "\n")

            print("Processing: " + str(xls) + " contract number: " + str(id))
            id = id + 1
            totalContracts = totalContracts + 1
            
            # Will work on these after I fix the database since decided to recreate it

            # This insert statement was used to insert cities (no duplicates) in the database
            # db.insert("""INSERT INTO cities("cityName") SELECT '""" + cLocation + """' WHERE NOT EXISTS (SELECT "cityName" FROM cities WHERE "cityName" = '""" + cLocation + """');""")
            
            # Fetch cities because we need to get the corresponding cityId
                # db.select("""SELECT * FROM cities""")
            # Loop through cities and find the cityId that corresponds to cLocation
            # for row in db.rows:
                #if row[1] == cLocation: # row[0] is cityId, row[1] is cityName so we need to check cityName for equality with cLocation
                    #db.insert("""INSERT INTO contractors("contractorName", "cityId", "isLocal") SELECT '""" + contractor + """', '""" + str(row[0])  + """', '""" + str(bool(isLocal)) + """' WHERE NOT EXISTS (SELECT "contractorName" FROM contractors WHERE "contractorName" = '""" + contractor +  """');""")
                        #print(db.getLastQuery())
                    #db.insert("""INSERT INTO contractors("contractorName", "cityId", "isLocal")  VALUES('""" + contractor + """', '""" + str(row[0]) + """', '""" + str(bool(isLocal)) + """')""")
    print("TOTAL kontrata: " + str(totalContracts))

if __name__=="__main__":
    main()
