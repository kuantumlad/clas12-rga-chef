import os
import glob
import pandas as pd

print " >> Updating workflow "

run_sheet = pd.read_csv('productionRunSheetCurrent.csv')
test_sheet = pd.read_csv('newProductionSheet.csv')

#print run_sheet.iloc[2:, 0]

print 'Concatenate new DF and old DF'

df = pd.concat([run_sheet,test_sheet])
df = df.reset_index(drop=True)

# group by
df_gpby = df.groupby(list(df.columns))

# get unique index of records
idx = [x[0] for x in df_gpby.groups.values() if len(x) == 1 ]

# filter the index of records
df = df.reindex(idx)

# resort the new dataframe which now contains only the new runs
sorted_runs = df.sort_values(df.columns[0],ascending=True)

#print sorted_runs.iloc[:,0]

if len(sorted_runs) == 0:
    print ' No new runs added to Google Spreadsheet. Will not update lists. Exiting'
    updated_run_list = open("/w/hallb-scifs17exp/clas12/rg-a/software/updatedRunList.txt","w")
    exit()

updated_run_list = open("/w/hallb-scifs17exp/clas12/rg-a/software/updatedRunList.txt","w")
for i in sorted_runs.iloc[:,0]:
    print ' Adding run ' + i + ' to new run list '
    updated_run_list.write(i+' \n')

updated_run_list.close()

