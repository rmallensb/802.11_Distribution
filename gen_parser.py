import pyshark
import sys, os
import json
from pathlib import Path

output_a = 'gen_a.txt'
output_n = 'gen_n.txt'
output_g = 'gen_g.txt'


def parse(packet, d):
    
    # For cap['WLAN']
    wlan_interest  = ['fc_retry']
    # For cap['WLAN_RADIO']
    radio_interest = ['Signal_dbm', 'Noise_dbm', 'Data_rate', 'Duration']

    d['Count'] += 1

    snr_true = True

    for item in wlan_interest:
        retry = packet['WLAN'].get(item)
        if type(retry) == type(None):            
            continue

        d[item] += int(retry)
   
    for item in radio_interest:
        data = packet['WLAN_RADIO'].get(item)
        if type(data) == type(None):
            if item == 'Signal_dbm' or item == 'Noise_dbm':
                snr_true = False

            if 'omitted' in d[item]:
                d[item]['omitted'] += 1
            else:
                d[item]['omitted'] = 1
        else:
            if data in d[item]:
                d[item][data] += 1
            else:
                d[item][data] = 1

    # Calculate SNR
    if snr_true:
        signal = packet['WLAN_RADIO'].get('Signal_dbm')
        noise  = packet['WLAN_RADIO'].get('Noise_dbm')
        snr = float(signal) / float(noise)

        if snr in d['SNR']:
            d['SNR'][snr] += 1
        else:
            d['SNR'][snr] = 1


    return d


def main():
    # TODO Make this parse all packets within a directory
    # TODO Output statistics into another directory

    try:
        capture = sys.argv[1]
    except:
        print( "Usage: python {} pcap_file ".format(sys.argv[0]))
        exit(1)

    cap = pyshark.FileCapture(capture)

    index = 4290

    # Check if files exist already
    # If they do we will just add the new data to them
    # Otherwise create the files
    a_path = Path(output_a)
    n_path = Path(output_n)
    g_path = Path(output_g)

    if a_path.is_file():
        fa = open(output_a, 'r')
        dict_a = json.load(fa)
        fa.close()
    else:
        dict_a = {}
        dict_a['fc_retry'] = 0
        dict_a['Count'] = 0
        dict_a['Signal_dbm'] = {}
        dict_a['Noise_dbm'] = {}
        dict_a['Data_rate'] = {}
        dict_a['Duration'] = {}
        dict_a['SNR'] = {}

    if n_path.is_file():
        fn = open(output_n, 'r')
        dict_n = json.load(fn)
        fn.close()
    else:
        dict_n = {}
        dict_n['fc_retry'] = 0
        dict_n['Count'] = 0
        dict_n['Signal_dbm'] = {}
        dict_n['Noise_dbm'] = {}
        dict_n['Data_rate'] = {}
        dict_n['Duration'] = {}
        dict_n['SNR'] = {}

    if g_path.is_file():
        fg = open(output_g, 'r')
        dict_g = json.load(fg)
        fg.close()
    else:
        dict_g = {}
        dict_g['fc_retry'] = 0
        dict_g['Count'] = 0
        dict_g['Signal_dbm'] = {}
        dict_g['Noise_dbm'] = {}
        dict_g['Data_rate'] = {}
        dict_g['Duration'] = {}
        dict_g['SNR'] = {}


    while True:
        try:
            # Keep track of how many we've done in case of failure
            if (index % 10 == 0):
                ft = open("tracker.txt", "w")
                ft.write(str(index))
                ft.close()
            
            if cap[index]['WLAN_RADIO'].get('phy') == '5':      #802.11a
                dict_a = parse(cap[index], dict_a)
            elif cap[index]['WLAN_RADIO'].get('phy') == '7':    #802.11n
                dict_n = parse(cap[index], dict_n)
            elif cap[index]['WLAN_RADIO'].get('phy') == '6':    #802.11g
                dict_g = parse(cap[index], dict_g)
            else:
                fd = open("catcher.txt", "a")
                fd.write(str(cap[index]['WLAN_RADIO']))
                fd.write('\n')
                fd.close()
            index += 1
        except Exception as e:
            print e
            print index
            ft = open("tracker.txt", "w")
            ft.write(str(index))
            ft.close()
            break

    fn = open(output_n, "w")
    fn.write(json.dumps(dict_n, indent=2))
    fn.write('\n')
    fn.close()

    fa = open(output_a, "w")
    fa.write(json.dumps(dict_a, indent=2))
    fa.write('\n')
    fa.close()

    fg = open(output_g, "w")
    fg.write(json.dumps(dict_g, indent=2))
    fg.write('\n')
    fg.close()

    return
    

if __name__ == "__main__":
    main()


