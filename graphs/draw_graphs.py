import numpy as np
import matplotlib.pyplot as plt


top_nodes = ['14', '15', '21', '24', '29', '32', '36', '4', '5', '8'] # folders to draw graphs from (10 randomly sampled)
all_nodes = [str(x) for x in range(1, 50) if not x in [3, 9, 41]]
block_times = []

def init(nodeset):
    global avg_throughput_byte, avg_throughput_tx, tx_s, nodes, block_times, mem, cpu
    nodes = nodeset
    time_factors = {}

    for node in nodes:
        time_factor = float(open('data/' + node + '/landmarks').read().splitlines()[0].split(",")[1])
        time_factors[node] = time_factor

    tx_s = {}
    byte_s = {}

    max_len = 200000
    mem = [0.0] * max_len
    cpu = [0.0] * max_len
    for node in nodes:
        chaindata = open("data/"+ str(node) +"/chaindata").read().strip().splitlines()[2:] # exclude header line, genesis block
        blocks = [x.split(",") for x in chaindata]
        throughput_tx = ([0] * ((int(blocks[-1][2]) - int(time_factors[node])) + 2))
        throughput_byte = ([0] * ((int(blocks[-1][2]) - int(time_factors[node])) + 2))
        max_len = max(len(throughput_tx), max_len)
        last_mem = 0
        last_cpu = 0
        for block_idx in range(0, len(blocks)):
            block = blocks[block_idx]
            block_times.append(int(block[2]) - int(max(0, blocks[block_idx - 1])[2]))
            throughput_tx[int(block[2]) - int(time_factors[node])] += int(block[4])
            throughput_byte[int(block[2]) - int(time_factors[node])] += int(block[1])
        chaindata = open("data/"+ str(node) +"/resources").read().strip().splitlines()
        for dataline in chaindata:
            timestamp = int(float(dataline.split(",")[0]))
            cpu_used = float(dataline.split(",")[1])
            mem_used = float(dataline.split(",")[2])
            mem[timestamp - int(time_factors[node])] += mem_used
            cpu[timestamp - int(time_factors[node])] += cpu_used
        # smooth out mem, cpu arrays by filling in missing data
        last_mem = 0.0
        last_cpu = 0.0
        for item in range(0, max_len):
            if mem[item] == 0:
                mem[item] = last_mem
            else:
                last_mem = mem[item]
            if cpu[item] == 0:
                cpu[item] = last_cpu
            else:
                last_cpu = cpu[item]
        tx_s[node] = throughput_tx
        byte_s[node] = throughput_byte

    avg_throughput_tx = [0] * max_len
    avg_throughput_byte = [0] * max_len
    divisors = [0] * max_len

    for node in nodes:
        # get moving average of node tx/s to detect offline periods
        node_avg = np.convolve(tx_s[node], np.ones((50,))/50, mode='valid')
        for i in range(0, len(tx_s[node])):
            avg_throughput_tx[i] = avg_throughput_tx[i] + tx_s[node][i]
            avg_throughput_byte[i] = avg_throughput_byte[i] + byte_s[node][i]
            # if node not offline, add to divisors
            if node_avg[min(i, len(node_avg) - 1)] > 0:
                divisors[i] += 1.0

    avg_throughput_tx = [avg_throughput_tx[i] / max(divisors[i], 1.0) for i in range(0, max_len)]
    avg_throughput_byte = [avg_throughput_byte[i] / max(divisors[i], 1.0) for i in range(0, max_len)]
    cpu = [cpu[i] / max(divisors[i], 1.0) for i in range(0, max_len)]
    mem = [mem[i] / max(divisors[i], 6.0) for i in range(0, max_len)]

def draw_graph_one():
    global nodes
    for node in nodes:
        plt.xlabel("Time since experiment start (s)")
        plt.ylabel("Throughput (tx/s)")
        plt.title("Transaction Throughput - Single Node")
        txs = tx_s[str(node)]
        plt.plot(np.convolve(txs, np.ones((60,))/60, mode='valid'))
        plt.show()

init(all_nodes)
draw_graph_one()
plt.xlabel("Time since experiment start (s)")
plt.ylabel("Throughput")
plt.title("Average Transaction Throughput")
l1, = plt.plot(np.convolve(avg_throughput_tx[:6385], np.ones((60,))/60, mode='valid'), label="tx/s throughput")
l2, = plt.plot(np.convolve(avg_throughput_byte[:6385], np.ones((60,))/60, mode='valid'), label="bytes/s throughput")
l3, = plt.plot(np.convolve([x/10 for x in avg_throughput_byte[:6385]], np.ones((60,))/60, mode='valid'), label="tx/s throughput, 10 b/tx")
axes = plt.gca()
axes.set_ylim([0,1000000])
axes.set_yscale('symlog')
plt.legend(handles=[l1, l2, l3])
plt.show()
l1, = plt.plot(np.convolve(avg_throughput_tx[:6385], np.ones((60,))/60, mode='valid'), label="tx/s throughput")
plt.xlabel("Time since experiment start (s)")
plt.ylabel("Throughput (tx/s)")
plt.title("Average Transaction Throughput - Linear Scale")
plt.show()

l1, = plt.plot(np.convolve(cpu[:6385], np.ones((10,))/10, mode='valid'), label="tx/s throughput")
plt.xlabel("Time since experiment start (s)")
plt.ylabel("CPU (percent)")
plt.title("Average CPU Usage")
plt.show()

l1, = plt.plot(np.convolve(mem[:6385], np.ones((10,))/10, mode='valid'), label="tx/s throughput")
plt.xlabel("Time since experiment start (s)")
plt.ylabel("Memory Usage (percent)")
plt.title("Average Memory Usage")
plt.show()


