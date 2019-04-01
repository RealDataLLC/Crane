def returnMatches(worksheet, searchEntry):
    matches = worksheet.findall(searchEntry)
    if matches:
        # return values of matched cells
        for cell in matches:
            print("Found something at R%sC%s" % (cell.row, cell.col))

            print("Here's the other information")
            # select all values in the same row, then print each cell
            row = worksheet.row_values(cell.row)
            row = [x.encode('ascii', errors='ignore') for x in row]
            print(row)
    else:
        print("Nothing was found")