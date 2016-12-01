import os


all_blocknums = []
all_timestamps = []

for i in range(0, 50):
    basedir = "data/" + str(i)
    if not os.path.exists(basedir):
        continue
    if not os.path.exists(basedir + "/resources"):
        print i
    if not "allfalldown" in open(basedir + "/landmarks").read():
        print i
    time_exp_end = open(basedir + "/landmarks").read().strip().splitlines()[-1].split(",")[1]
    time_lastevent = open(basedir + "/resources").read().strip().splitlines()[-1].split(",")[0]
    if (float(time_lastevent) - float(time_exp_end)) < 0:
        print i
    block = open(basedir + "/chaindata").read().strip().splitlines()[-1].split(",") 
    blocknum = int(block[0])
    timestamp = int(block[2])
    all_blocknums.append(blocknum)
    all_timestamps.append(timestamp)
    if blocknum > 3100 and timestamp >= 1481405570:
        print i, blocknum, timestamp

print sorted(all_blocknums, reverse=True)
print sorted(all_timestamps, reverse=True)
