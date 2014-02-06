#!/usr/bin/env python

gameNumber = open("gameNumber.txt", "rU")
num = int(gameNumber.readline())
gameNumber.close()

tableString = "htmlTables/table" + str(num) + ".html"
tableFile = open(tableString, "rU")
tableHTML = [line for line in tableFile]
tableFile.close()

print "Content-type: text/html"
print
print "<title>X-League Stats</title>"
for line in tableHTML:
    print line