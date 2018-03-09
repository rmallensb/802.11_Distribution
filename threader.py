from threading import Thread, Lock
import sys, os
import pyshark
import json
from pathlib import Path

from gen_parser import parse

# This program takes as input a directory path
# It will fork off a thread and parse every file capture located in the directory path



parsers = ['gen_parser.py']

output_a = 'gen_a.txt'
output_g = 'gen_g.txt'
output_n = 'gen_n.txt'

a_lock = Lock()
g_lock = Lock()
n_lock = Lock()

def gen_template():
    # General parser template
    gt               = {}
    gt['Count']      = 0
    gt['fc_retry']   = 0
    gt['Signal_dbm'] = {}
    gt['Noise_dbm']  = {}
    gt['Data_rate']  = {}
    gt['Duration']   = {}
    gt['SNR']        = {}

    return gt


def merger(d1, d2):
    final = gen_template()
    for key in d1.keys():
        # Need to go deeper to get actual values
        if type(d1.get(key)) == dict:
            final[key] = {k : d1[key].get(k, 0) + d2[key].get(k, 0) for k in set(d1[key].keys()) | set(d2[key].keys())}
        else:
            final[key] = d1.get(key, 0) + d2.get(key, 0)    

    return final

def write(d, type):
    if type == 'a':
        with a_lock:
            path = Path(output_a)
            if path.is_file():
                with open(output_a, 'r') as fa:
                    data = json.load(fa)
                    new_data = merger(d, data)
            else:
                os.system('touch {}'.format(output_a))
                new_data = d

            with open(output_a, 'w') as fa:
                fa.write(json.dumps(new_data, indent=2))

    if type == 'g':
        with g_lock:
            path = Path(output_g)
            if path.is_file():
                with open(output_g, 'r') as fg:
                    data = json.load(fg)
                    new_data = merger(d, data)
            else:
                os.system('touch {}'.format(output_g))
                new_data = d

            with open(output_g, 'w') as fg:
                fg.write(json.dumps(new_data, indent=2))
    
    if type == 'n':
        with n_lock:
            path = Path(output_n)
            if path.is_file():
                with open(output_n, 'r') as fn:
                    data = json.load(fn)
                    new_data = merger(d, data)
            else:
                os.system('touch {}'.format(output_n))
                new_data = d

            with open(output_n, 'w') as fn:
                fn.write(json.dumps(new_data, indent=2))

def threader(pcap):
    (a, g, n) = splitter(pcap) 

    ta = Thread(target=write, args=(a, 'a'))
    ta.run()
    tg = Thread(target=write, args=(g, 'g'))
    tg.run()
    tn = Thread(target=write, args=(n, 'n'))
    tn.run()

    if ta.is_alive():
        ta.join()
    if tg.is_alive():
        tg.join()
    if tn.is_alive():
        tn.join()


def splitter(path):
    # Add a guard to assign dict to correct template
    # Determined by a 'template' argument
    dict_a = gen_template()
    dict_g = gen_template()
    dict_n = gen_template()

    pcap  = pyshark.FileCapture(path)
    index = 0
    for packet in pcap:
        try:
            if packet['WLAN_RADIO'].get('phy')   == '5':    #802.11a
                dict_a = parse(packet, dict_a)
            elif packet['WLAN_RADIO'].get('phy') == '6':    #802.11g
                dict_g = parse(packet, dict_g)
            elif packet['WLAN_RADIO'].get('phy') == '7':    #802.11n
                dict_n = parse(packet, dict_n)
            else:
                with open('catcher.txt', 'a') as fd:
                    fd.write(str(packet['WLAN_RADIO']))
                    fd.write('\n')
            index += 1
        except Exception as e:
            print 'error at {0}: {1}'.format(index, e)

    #print ('Here is a: {}'.format(str(dict_a)))
    #print '\n'
    #print ('Here is g: {}'.format(str(dict_g)))
    #print '\n'
    #print ('Here is n: {}'.format(str(dict_n)))
    #print '\n'   

    return (dict_a, dict_g, dict_n)


def main():
    try:
        directory = sys.argv[1]
    except:
        print( "Usage: python {} pcap_file".format(sys.argv[0]))
        exit(1)

    # List of threads to join on
    t_list = []

    # Kick off the parser threads
    for script in parsers:
        for root, dirs, files in os.walk(directory):
            for file in files:
                path = '{0}{1}'.format(directory, file)
                t = Thread(target=threader, args=(path,))
                #t.dameon = True
                t_list.append(t)
                t.run()

    for thread in t_list:
        if thread.is_alive():
            thread.join()
                

    
    print 'All threads finished.'
    exit(0)

if __name__ == "__main__":
    main()
