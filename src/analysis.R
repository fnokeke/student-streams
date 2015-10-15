# __author__ = "Fabian Okeke"
# __date__ = "Oct 15, 2015"

##############################
# student-streams
##############################

library(jsonlite)

######
# MAIN
######
json_file <- "~/dev/student-streams/dataset/LocationHistory.json"
df.loc <- fromJSON(txt=json_file)
length(df.loc)
