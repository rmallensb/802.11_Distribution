import sys, os
import pyshark
import json
from pathlib import Path
from optparse import OptionParser
from multiprocessing import Process

from gen_parser  import parse as gp
from dur_parser  import parse as dp
from rate_parser import parse as rp

# This program takes as input a directory path
# It will fork off a thread and parse every file capture located in the directory path

def get_output_names(type, output):
    a  = '{}_{}_a'.format(output, type)
    g  = '{}_{}_g'.format(output, type)
    n  = '{}_{}_n'.format(output, type)
    ac = '{}_{}_ac'.format(output, type)

    return (a, g, n, ac)

def get_dicts(type):
    if type == 'gen':
        return gen_template()
    elif type == 'dur' or type == 'rate':
        return cat_template()
    else:
        print 'Invalid type [{}], exiting.'.format(type)
        exit(1)

# General parser template
def gen_template():
    gt               = {}
    gt['Count']      = 0
    gt['fc_retry']   = 0
    gt['fc_type']    = {} 
    gt['Signal_dbm'] = {}
    gt['Noise_dbm']  = {}
    gt['Data_rate']  = {}
    gt['Duration']   = {}
    gt['SNR']        = {}

    return gt

# Duration parser template
def cat_template():
    dt = {}
    dt['omitted'] = 0

    return dt

def merger(d1, d2, script):
    final = get_dicts(script)
    for key in set(d1.keys()) | set(d2.keys()):
        if type(d1.get(key)) == dict or type(d2.get(key)) == dict:  
            v1 = d1.get(key, {})
            v2 = d2.get(key, {})
            
            if key in d1 and key in d2:
                final[key] = {}
                
                for nkey in set(v1.keys()) | set(v2.keys()):
                    if type(v1.get(nkey)) == dict or type(v2.get(nkey)) == dict:
                        
                        if nkey in v1 and nkey in v2:
                            final[key][nkey] = {k : v1.get(nkey, {}).get(k,0) + v2.get(nkey, {}).get(k,0) for k in set(v1.get(nkey, {}).keys()) | set(v2.get(nkey, {}).keys())}

                        else:
                            if nkey in v1:
                                final[key][nkey] = v1.get(nkey)
                            else:
                                final[key][nkey] = v2.get(nkey)

                    else:
                        final[key][nkey] = v1.get(nkey, 0) + v2.get(nkey, 0)

            else:
                if key in d1:
                    final[key] = v1
                else:
                    final[key] = v2

        else:
            final[key] = d1.get(key, 0) + d2.get(key, 0)



    return final

def write(d, out_file, script):
    
    path = Path(out_file)
    if path.is_file():
        with open(out_file, 'r') as f:
            data = json.load(f)
            new_data = merger(d, data, script)
    else:
        os.system('touch {}'.format(out_file))
        new_data = d

    with open(out_file, 'w') as f:
        f.write(json.dumps(new_data, indent=2))


def threader(pcap, script, output):
    (a, g, n, ac) = splitter(pcap, script) 

    (out_a, out_g, out_n, out_ac) = get_output_names(script, output)

    write(a,  out_a,  script)
    write(g,  out_g,  script)
    write(n,  out_n,  script)
    write(ac, out_ac, script)


def splitter(path, script):
    # Add a guard to assign dict to correct template
    # Determined by a 'template' argument
    
    dict_a  = get_dicts(script)
    dict_g  = get_dicts(script)
    dict_n  = get_dicts(script)
    dict_ac = get_dicts(script)

    pcap  = pyshark.FileCapture(path)
    index = 0
    tracker = open('tracker.txt', 'w')
    for packet in pcap:
        if index % 100 == 0:
            os.system("echo '' > tracker.txt")
            tracker.write(path)
            tracker.write('\n')
            tracker.write(script)
            tracker.write('\n')
            tracker.write(str(index))
            tracker.flush()
                
        try:
            if packet['WLAN_RADIO'].get('phy')   == '5':    #802.11a
                if script == 'gen':
                    dict_a  = gp(packet, dict_a)
                elif script == 'dur':
                    dict_a = dp(packet, dict_a)
                else:
                    dict_a = rp(packet, dict_a)
            elif packet['WLAN_RADIO'].get('phy') == '6':    #802.11g
                if script == 'gen':
                    dict_g = gp(packet, dict_g)
                elif script == 'dur':
                    dict_g  = dp(packet, dict_g)
                else:
                    dict_g = rp(packet, dict_g)
            elif packet['WLAN_RADIO'].get('phy') == '7':    #802.11n
                if script == 'gen':
                    dict_n = gp(packet, dict_n)
                elif script == 'dur':
                    dict_n = dp(packet, dict_n)
                else:
                    dict_n = rp(packet, dict_n)
            elif packet['WLAN_RADIO'].get('phy') == '8':    #802.11ac
                if script == 'gen':
                    dict_ac = gp(packet, dict_ac)
                elif script == 'dur':
                    dict_ac = dp(packet, dict_ac)
                else:
                    dict_ac = rp(packet, dict_ac)
            else:
                with open('catcher.txt', 'a') as fd:
                    fd.write(str(packet['WLAN_RADIO']))
                    fd.write('\n')
        except Exception as e:
            print 'error at {}: {}'.format(index, e)
        index += 1

    tracker.close()
    
    return (dict_a, dict_g, dict_n, dict_ac)


def main():
    parser = OptionParser(usage="usage: python {} [options] -p".format(sys.argv[0]),
                          version="%prog v0.1")
    
    parser.add_option("-p", "--pcaps",
                      dest="directory",
                      help="Directoring containing only pcap files")

    parser.add_option("-a", "--all",
                      action='store_true',
                      help="Run all parser scripts (default)")

    parser.add_option("-g", "--gen",
                      action='store_true',
                      help="Run the general parser script")

    parser.add_option("-d", "--dur",
                      action='store_true',
                      help="Run the duration parser script")

    parser.add_option("-r", "--rate",
                      action='store_true',
                      help="Run the data_rate parser script")

    parser.add_option("-o", "--output",
                      dest="output",
                      default="out",
                      help="Naming style for output files. ex {output}_gen_a")

    (options, args) = parser.parse_args()

    directory = options.directory
    all       = bool(options.all)
    gen       = bool(options.gen)
    dur       = bool(options.dur)
    rate      = bool(options.rate)
    output    = options.output

    if not gen and not dur and not rate:
        all = True

    parsers = []
    if all:
        gen  = True
        dur  = True
        rate = True
    if gen:
        parsers.append('gen')
    if dur:
        parsers.append('dur')
    if rate:
        parsers.append('rate')

    procs = []

    # Kick off the parser threads
    for script in parsers:
        for root, dirs, files in os.walk(directory):
            for file in files:
                path = '{0}{1}'.format(directory, file)
                #threader(path, script, output)
                p = Process(target=threader, args=(path, script, output))
                procs.append(p)
                p.start()
                if len(procs) >= 4:
                    for proc in procs:
                        proc.join()
                    del proc[:]

    for proc in procs:
        proc.join()
    
    with open('tracker.txt', 'a') as f:
        f.write('\n')
        f.write(files)

    print 'Done.'
    exit(0)

if __name__ == "__main__":
    main()
