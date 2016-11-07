#!/usr/bin/python3
import xlrd
import fixCity
import dbConnect
import sys

def main():
    cities = ['Gjakove', 'Ferizaj', 'Prishtine', 'Gjilan', 'Viti']
    years = ['2011', '2012', '2013', '2014']
    # Debugging single files
    #xlsPath = ['kontratat/Ferizaj/2013.xls']
    xlsPath = ['kontratat/Ferizaj/2011.xls', 'kontratat/Ferizaj/2012.xls', 'kontratat/Ferizaj/2013.xls', 'kontratat/Ferizaj/2014.xls', 'kontratat/Gjakove/2011.xls', 'kontratat/Gjakove/2012.xls', 'kontratat/Gjakove/2013.xls', 'kontratat/Gjakove/2014.xls', 'kontratat/Prishtine/2011.xls', 'kontratat/Prishtine/2012.xls', 'kontratat/Prishtine/2013.xls', 'kontratat/Prishtine/2014.xls', 'kontratat/Gjilan/2011.xls', 'kontratat/Gjilan/2012.xls', 'kontratat/Gjilan/2013.xls', 'kontratat/Gjilan/2014.xls', 'kontratat/Viti/2011.xls', 'kontratat/Viti/2012.xls', 'kontratat/Viti/2013.xls']

    # Connect to database
    if not dbConnect.connect():
        print("Couldn't connect to database")
        sys.exit()

    # Curious to know how many contracts are there
    totalContracts = 0

    for xls in xlsPath:
        # Debugging purposes
        print("Current XLS: " + xls)

        firstRow = 0
        firstColumn = 0

        workbook = xlrd.open_workbook(xls, formatting_info=True)
        worksheet = workbook.sheet_by_index(0)

        rd_xf = workbook.xf_list[worksheet.cell_xf_index(26, 2)]
        print(str(rd_xf.background.pattern_colour_index)) # 22 - gray, 9 - black
        #print(workbook.colour_map[rd_xf.background.pattern_colour_index]) # RGB Format
        """
            Starts from row 50, and go down until the current cell isn't gray and adds one
            which means it got to the first row.
        """
        for i in range(50, 1, -1):
            rd_xf = workbook.xf_list[worksheet.cell_xf_index(i, 1)]
            if not isinstance(worksheet.cell(i, 1).value, float):
                firstRow = i + 2
                break

            if rd_xf.background.pattern_colour_index == 22:
                firstRow = i + 1
                break

        # Debugging
        print("First row: " + str(firstRow))

        """
            Starts from first column to the 20th and when it runs on a string
            that means it got to the project name since evey cell before the project is an instance of float
        """
        for i in range(3, 20):
            if isinstance(worksheet.cell(firstRow, i).value, str):
                firstColumn = i
                break
        # Debugging
        print("First column: " + str(firstColumn))
        
        # If the first column is empty that means there is a gap between columns so add one index to the firstColumn
        if worksheet.cell(firstRow, firstColumn).value == "":
            firstColumn += 1

        count = 0
        estimatedSum = 0
        costSum = 0
        annexSum = 0

        # HARD-CODING all these numbers sucks gotta fix em later
        for i in range(firstRow, 500): # Check till the 500th row, change if there are potentially more
            for tempCity in cities:
                if tempCity in xls:
                    city = tempCity
            for tempYear in years:
                if tempYear in xls:
                    year = tempYear

            project = worksheet.cell(i, firstColumn).value
            # firstColumn + 1 = date because project name is at firstColumn index, date is one column after it
            # the same works for the other properties
            date = worksheet.cell(i, firstColumn + 1).value
            estimatedCost = worksheet.cell(i, firstColumn + 2).value
            cost = worksheet.cell(i, firstColumn + 3).value
            annexCost = worksheet.cell(i, firstColumn + 4).value
            contractor = worksheet.cell(i, firstColumn + 5).value
            cLocation = worksheet.cell(i, firstColumn + 6).value
            isLocal = worksheet.cell(i, firstColumn + 7).value

            # Viti has different syntax, so I need to add different indexes to the firstColumn
            if 'Viti/2011.xls' in xls or 'Viti/2012.xls' in xls or 'Viti/2013.xls' in xls or 'Viti/2014.xls' in xls:
                estimatedCost = worksheet.cell(i, firstColumn + 3 + 2).value
                cost = worksheet.cell(i, firstColumn + 3 + 3).value
                annexCost = worksheet.cell(i, firstColumn + 3 + 4).value
                contractor = worksheet.cell(i, firstColumn + 3 + 5).value
                cLocation = worksheet.cell(i, firstColumn + 3 + 6).value
                isLocal = worksheet.cell(i, firstColumn + 3 + 7).value

            # Some contracts have a blank line sometimes so to be on the safe side
            # Check the one after the current one before deciding it's over
            projectPlusOne = worksheet.cell(i + 1, firstColumn).value
            # Check if it got at the EOF then break
            if (project == '' and projectPlusOne == '') or (project.lower() == 'totali :' or projectPlusOne.lower() == 'totali :'):
                print("Current contract list contains: " + str(count) + " contracts.")
                count = 1
                break

            # If they contain no value, give them 0 because we need to cast to float later to sum them
            if annexCost == '' or not isinstance(annexCost, float):
                annexCost = 0.0
            if estimatedCost == '' or not isinstance(estimatedCost, float):
                estimatedCost = 0.0
            if cost == '' or not isinstance(costSum, float):
                cost = 0.0

            # Some costs contain ’ instead of , and that throws an error when I try to cast float to cost
            if isinstance(cost, str):
                if '’' in cost or '€' in cost or ',' in cost:
                    cost = cost.replace('’', '')
                    cost = cost.replace('€', '')
                    cost = cost.replace(',', '')
            
            if isinstance(estimatedCost, str):
                if '’' in estimatedCost or '€' in estimatedCost or ',' in estimatedCost:
                    estimatedCost = estimatedCost.replace('’', '')
                    estimatedCost = estimatedCost.replace('€', '')
                    estimatedCost = estimatedCost.replace(',', '')

            if isinstance(annexCost, str):
                if '’' in annexCost or '€' in annexCost or ',' in annexCost:
                    annexCost = annexCost .replace('’', '')
                    annexCost = annexCost .replace('€', '')
                    annexCost = annexCost .replace(',', '')

            # If it contains more than two dots (decimal points), split the value on decimal points and format it the right way
            if str(estimatedCost).count('.') >= 2:
                estimatedCost = str(estimatedCost).split('.')[0] + str(estimatedCost).split('.')[1]

            if str(estimatedCost).count(',') >= 2:
                    estimatedCost = str(estimatedCost).split(',')[0] + str(estimatedCost).split(',')[1]

            if str(cost).count('.') == 2:
                cost = str(cost).split('.')[0] + str(cost).split('.')[1]

            if str(cost).count(',') == 2:
                cost = str(cost).split(',')[0] + str(cost).split(',')[1]

            # Fix city name
            cLocation = fixCity.fixCityName(cLocation)

            # Formatting
            # Project
            project = project.replace('”', '')
            project = project.replace('“', '')
            project = project.replace('"', '')
            project = project.replace("'", '')

            # Contractor
            contractor = contractor.replace('”', '')
            contractor = contractor.replace('“', '')
            contractor = contractor.replace('"', '')
            contractor = contractor.replace("'", '')

            print("Qyteti: " + city)
            print("Viti: " + year)
            print("Emri i kontrates: " + project)
            print("Data: " + str(date))
            print("Vlera e paramenduar: " + str(estimatedCost))
            print("Vlera e shpenzuar: " + str(cost))
            print("Vlera e aneks kontrates: " + str(annexCost))
            print("Punekryesi: " + str(contractor))
            print("Lokacioni i punekryesit: " + str(cLocation))
            print("Vendore: " + str(bool(isLocal)) + "\n")

            try:
                estimatedSum = estimatedSum + float(estimatedCost)
            except ValueError:
                print(estimatedSum)
                print("Value error in estimatedCost: " + estimatedCost)
                print(project)
                sys.exit()

            try:
                costSum = costSum + float(cost)
            except ValueError:
                if isinstance(cost, str):
                    continue
                print(cost)
                print("Value error in cost: " + cost)
                sys.exit()

            try:
                annexSum = annexSum + float(annexCost)
            except ValueError:
                print(annexCost)
                print("Value error in annexCost: " + annexCost)
                print("Current: " + str(project))
                sys.exit()

            #print("Processing: " + str(xls) + " contract number: " + str(count) + " row number: " + str(i))
            count = count + 1
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
    print("Total Estimated SUM: " + str(estimatedSum))
    print("Total COST: " + str(costSum))
    print("Total Annex COST: " + str(annexSum))
    print("TOTAL: " + str(costSum + annexSum))
    
if __name__=="__main__":
    main()
