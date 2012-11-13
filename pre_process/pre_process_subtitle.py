import re


timeline = []
next_segment = 1
current_time_interval = 0
processing_time_interval = 0
processing_line = ""
processed_lines =[]
for line in open("subtitles.srt", "r"):
  if line.strip() == str(next_segment):
    next_segment += 1 
    #print "Skipping"
    continue

  elif len(line.split(" --> ")) == 2:
    time_str = line.split(" --> ")[0].split(":")
    processing_time_interval = int(time_str[0]) * 60 + int(time_str[1])
    #print "pt,",  processing_time_interval
    #break

  else:
    if current_time_interval == processing_time_interval:
       #print line
       processing_line += " " + line.strip()
    else:
       current_time_interval += 1
       processed_lines.append(processing_line)
       processing_line = line.strip()
processed_lines.append(processing_line)

f = open("subtitles.processed", "w")
for l in processed_lines:
  f.write(l + "\n")

f.close()
