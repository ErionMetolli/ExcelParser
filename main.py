#!/usr/bin/python3
import xlrd
import fixCity
import sys
import psycopg2
import datetime

def main():
    cities = ['Gjakove', 'Ferizaj', 'Prishtine', 'Gjilan', 'Viti']
    years = ['2011', '2012', '2013', '2014']
    # Debugging single files
    #xlsPath = ['kontratat/Ferizaj/2013.xls']
    xlsPath = ['kontratat/Ferizaj/2011.xls', 'kontratat/Ferizaj/2012.xls', 'kontratat/Ferizaj/2013.xls', 'kontratat/Ferizaj/2014.xls', 'kontratat/Gjakove/2011.xls', 'kontratat/Gjakove/2012.xls', 'kontratat/Gjakove/2013.xls', 'kontratat/Gjakove/2014.xls', 'kontratat/Prishtine/2011.xls', 'kontratat/Prishtine/2012.xls', 'kontratat/Prishtine/2013.xls', 'kontratat/Prishtine/2014.xls', 'kontratat/Gjilan/2011.xls', 'kontratat/Gjilan/2012.xls', 'kontratat/Gjilan/2013.xls', 'kontratat/Gjilan/2014.xls', 'kontratat/Viti/2011.xls', 'kontratat/Viti/2012.xls', 'kontratat/Viti/2013.xls']

    # Connect to database
    connProperties = "dbname='opendatathon' user='pgsql' host='localhost' password='password'"
    try:
        conn = psycopg2.connect(connProperties)
    except Exception as error:
        print(error)
        sys.exit()
    conn.autocommit = True
    cur = conn.cursor()

    # Curious to know how many contracts are there
    totalContracts = 0

    for xls in xlsPath:
        # Debugging purposes
        #print("Current XLS: " + xls)

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
        #print("First row: " + str(firstRow))

        """
            Starts from first column to the 20th and when it runs on a string
            that means it got to the project name since evey cell before the project is an instance of float
        """
        for i in range(3, 20):
            if isinstance(worksheet.cell(firstRow, i).value, str):
                firstColumn = i
                break
        # Debugging
        #print("First column: " + str(firstColumn))
        
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
            if cLocation == "I pacaktuar":
                cLocation = city

            # If there is no contractor or project name then continue
            if contractor == '' or project == '':
                continue

            # Formatting
            # Project
            project = project.replace('”', '')
            project = project.replace('“', '')
            project = project.replace('"', '')
            project = project.replace("'", '')
            project = project.replace('  ', '')

            # Contractor
            contractor = contractor.replace('”', '')
            contractor = contractor.replace('“', '')
            contractor = contractor.replace('"', '')
            contractor = contractor.replace("'", '')
            contractor = contractor.replace('  ', '')

            # Formatting Date for postgresql support
            if isinstance(date, str):
                if not date == '' and date.count('.') == 2: 
                    if date[0].isdigit():
                        date = date.split('-')[0].replace('.', '/') # Some dates have intervals splitted with - so get the first date only, and then replace . with / so | 01.01.2016-01.02.2016 is formatted to 01/01/2016 also requires mdy (european date format) on postgresql.conf
                    else:
                        continue
                else:
                    continue
            else:
                continue
            # Check if date is out of bounds
            try:
                datetime.datetime(day=int(date.split('/')[0]), month=int(date.split('/')[1]), year=int(date.split('/')[2]))
            except ValueError:
                print("Date out of bounds")
                continue

            # Avoid projects with more than 200 characters
            if len(project) > 200:
                continue

            if sys.argv[1] == 'SHOW':
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
                print("Value error in estimatedCost: " + estimatedCost)
                sys.exit()

            try:
                costSum = costSum + float(cost)
            except ValueError:
                if isinstance(cost, str):
                    continue
                print("Value error in cost: " + cost)
                sys.exit()

            try:
                annexSum = annexSum + float(annexCost)
            except ValueError:
                print("Value error in annexCost: " + annexCost)
                sys.exit()

            print("Processing: " + str(xls) + " contract number: " + str(count) + " row number: " + str(i))
            count = count + 1
            totalContracts = totalContracts + 1
            
            #This insert statement was used to insert cities (no duplicates) in the database
            if sys.argv[1] == 'INSERTCITIES': # INSERT cities, DATABASE cities
                cur.execute("""INSERT INTO cities("name") SELECT '""" + cLocation + """' WHERE NOT EXISTS (SELECT "name" FROM cities WHERE "name" = '""" + cLocation + """');""")

            elif sys.argv[1] == 'INSERTCONTRACTORS':
                # Loop through cities and find the city id that corresponds to cLocation
                cur.execute("""SELECT * FROM cities""")
                rows = cur.fetchall()
                for row in rows:
                    # row[0] is cityId, row[1] is cityName so we need to check cityName for equality with cLocation
                    if row[1] == cLocation:
                        cur.execute("""INSERT INTO contractors("name", "cityid", "islocal") SELECT '""" + contractor + """', '""" + str(row[0]) + """', '""" + str(bool(isLocal)) + """' WHERE NOT EXISTS (SELECT "name" FROM contractors WHERE "name" = '""" + contractor + """');""")

            elif sys.argv[1] == 'INSERTPROJECTS':
                cur.execute("""SELECT id, name FROM contractors""")
                rows = cur.fetchall()
                # First loops through cities, to find the corresponding city to use that city's id in the insert query
                for contractorRow in rows:
                    if contractorRow[1] == contractor:
                        cur.execute("""INSERT INTO projects("name", "date", "city", "year", "estimatedcost", "finalcost", "annexcost", "contractorid") SELECT '""" + project + """', '""" + date + """', '""" + city + """', '""" + str(year) + """', '""" + str(estimatedCost) + """', '""" + str(cost) + """', '""" + str(annexCost) + """', '""" + str(contractorRow[0]) + """' WHERE NOT EXISTS (SELECT "name" FROM projects WHERE "name" = '""" + project + """');""")

    print("Total count of contracts: " + str(totalContracts))
    print("Total Estimated SUM: " + str(estimatedSum))
    print("Total COST: " + str(costSum))
    print("Total Annex COST: " + str(annexSum))
    print("TOTAL: " + str(costSum + annexSum))
    

def help():
    help = """Usage:
        ./main.py [COMMAND]
        
        [COMMAND]
            1. INSERTCITIES      | Inserts every city that it finds in the excel files in cities table;
            2. INSERTPROJECTS    | Inserts every project that it finds in the excel files in projects table;
            3. INSERTCONTRACTORS | Inserts every contractor that is associated with at least one project in contractors table,
            4. SHOW              | Shows every project that it can find and informations about them"""
    print(help)


if __name__=="__main__":
    # Use sys.argv just to check if the first argument was written
    try:
        sys.argv[1]
    except:
        help()
        sys.exit()
    main()
