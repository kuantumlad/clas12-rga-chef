import os
import glob


###################################
##
##    By: Brandon Clary
##    05/01/2019
##    Purpose: Create table fror RGA wiki page
##   
##
##
###################################


#str_table = "<html><table><tr><th>Char</th><th>ASCII</th></tr>"

str_table = ' {| class="wikitable" \n |+ Pass Description \n !Pass Items \n !Description \n |- \n'

in_txt_file = open("history_pass0_v0p2.txt","r")
out_file = open("html_table_pass0_v0p2.txt","w")


lines = in_txt_file.readlines()

for x in lines:
    col0 = x.split(' ')[0]
    col1 = x.split(' ')[1][:-1]
    print col0 + " " + col1


    #str_row = "<tr><td>" + col0 + "</td><td>" + col1 + "</td><td>"
    #str_table = str_table + str_row
    str_row='! '+ col0 + '\n| ' +col1 + '\n|- \n'    
    str_table=str_table+str_row
    
#str_table = str_table+"</table></html>"
str_table = str_table+'|}'

out_file.write(str_table)

in_txt_file.close()
out_file.close()


print str_table
