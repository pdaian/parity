import psutil, time, os

os.system("touch resources")
file_handle = open('resources', 'a')

while 1:
    cpu, mem = sum(psutil.cpu_percent(interval=1, percpu=True)), psutil.virtual_memory() 
    file_handle.write(str(time.time()) + "," + str(cpu) + "," + str(mem[2]) + "\n")
    file_handle.flush()
