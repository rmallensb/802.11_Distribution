import pyshark
import sys, os
import json
from pathlib import Path


output_a = 'gen_a.txt'
output_n = 'gen_n.txt'


# 0 - Turbo Type
# 1 - Channel
# 2 - Frequency
# 3 - Signal Strength
# 4 - TSF Timestamp
# 5 - Preamble
# 6 - Noise Level
# 7 - PHY Type
# 8 - Duration
# 9 - Data Rate
def parse_a(cap, dict):
    capture = cap.split('\n')[1:]
    interest = {'Channel': 1, 'Frequency': 2, 'Signal': 3, 'Noise': 6, 'rate': 9, 'Duration': 8}

    dict['Count'] += 1

    snr_true = True

    for item in interest:
        index = interest[item]

        # Make sure we have that data
        # If not increment 'omitted' value
        if item not in capture[index]:
            # Can't calculate SNR if one is missing
            if item == 'Signal' or item == 'Noise':
                snr_true = False

            if 'omitted' in dict[item]:
                dict[item]['omitted'] += 1
            else:
                dict[item]['omitted'] = 1
            continue

        data = capture[index].split(': ')[1]

        if data in dict[item]:
            dict[item][data] += 1
        else:
            dict[item][data] = 1

    # Also calculate SNR if both data values present
    if snr_true:
        s_index = interest['Signal']
        n_index = interest['Noise']
        s = capture[s_index].split(': ')[1].split(' ')[0]
        n = capture[n_index].split(': ')[1].split(' ')[0]
        snr = float(s) / float(n)

        if snr in dict['SNR']:
            dict['SNR'][snr] += 1
        else:
            dict['SNR'][snr] = 1
    else:
        if 'omitted' in dict['SNR']:
            dict['SNR']['omitted'] += 1
        else:
            dict['SNR']['omitted'] = 1


    return dict


# 0  - Channel
# 2  - Duration
# 3  - MCS Index
# 7  - Signal Strength
# 10 - PHY Type
# 11 - Data Rate
# 14 - Frequency
# 15 - Noise Level
# 18 - Preamble
# 20 - Bandwidth
def parse_n(cap, dict):
    capture = cap.split('\n')[1:]
    interest = {'Channel': 0, 'Signal': 7, 'rate': 11, 'Frequency': 14, 'Noise': 15, 'Bandwidth': 20, 'Duration': 2}

    dict['Count'] += 1

    snr_true = True

    for item in interest:
        index = interest[item]
    
        # Make sure we have that data
        # If not increment 'omitted' value
        if item not in capture[index]:
            # Can't calculate SNR if one is missing
            if item == 'Signal' or item == 'Noise':
                snr_true = False

            if 'omitted' in dict[item]:
                dict[item]['omitted'] += 1
            else:
                dict[item]['omitted'] = 1
            continue

        data = capture[index].split(': ')[1]

        if data in dict[item]:
            dict[item][data] += 1
        else:
            dict[item][data] = 1

    # Also calculate SNR if both data values present
    if snr_true:
        s_index = interest['Signal']
        n_index = interest['Noise']
        s = capture[s_index].split(': ')[1].split(' ')[0]
        n = capture[n_index].split(': ')[1].split(' ')[0]
        snr = float(s) / float(n)

        if snr in dict['SNR']:
            dict['SNR'][snr] += 1
        else:
            dict['SNR'][snr] = 1
    else:
        if 'omitted' in dict['SNR']:
            dict['SNR']['omitted'] += 1
        else:
            dict['SNR']['omitted'] = 1

    return dict


def main():
    # TODO Make this parse all packets within a directory
    # TODO Output statistics into another directory

    try:
        capture = sys.argv[1]
    except:
        print( "Usage: python {} pcap_file ".format(sys.argv[0]))
        exit(1)

    cap = pyshark.FileCapture(capture)

    index = 0

    # Check if files exist already
    # If they do we will just add the new data to them
    # Otherwise create the files
    a_path = Path(output_a)
    n_path = Path(output_n)
    if a_path.is_file():
        fa = open(output_a, 'r')
        dict_a = json.load(fa)
        fa.close()
    else:
        dict_a = {}
        dict_a['Retransmission'] = 0
        dict_a['Count'] = 0
        dict_a['Channel'] = {}
        dict_a['Frequency'] = {}
        dict_a['Signal'] = {}
        dict_a['Noise'] = {}
        dict_a['rate'] = {}
        dict_a['Duration'] = {}
        dict_a['SNR'] = {}
    if n_path.is_file():
        fn = open(output_n, 'r')
        dict_n = json.load(fn)
        fn.close()
    else:
        dict_n = {}
        dict_n['Retransmission'] = 0
        dict_n['Count'] = 0
        dict_n['Channel'] = {}
        dict_n['Frequency'] = {}
        dict_n['Signal'] = {}
        dict_n['Noise'] = {}
        dict_n['rate'] = {}
        dict_n['Bandwidth'] = {}
        dict_n['Duration'] = {}
        dict_n['SNR'] = {}

    while True:
        try:

            # Keep track of how many we've done in case of failure
            if (index % 10 == 0):
                ft = open("tracker.txt", "w")
                ft.write(str(index))
                ft.close()
            
            # First check if retransmission
            # TODO: Also decide later on if we want to include retransmitted packets in analysis

            wlan = str(cap[index][1])
            radiotap = str(cap[index][0]).split('\n')
            for line in radiotap:
                if 'Flags: ' in line:
                    flag_code = line.split(' ')[1]
                    flag_byte = int(flag_code[-1])
                    if flag_byte >= 8:
                        if '802.11a' in wlan:
                            dict_a['Retransmission'] += 1
                        elif '802.11n' in wlan:
                            dict_n['Retransmission'] += 1
                    break


            if '802.11a' in wlan:
                dict_a = parse_a(wlan, dict_a)
            elif '802.11n' in wlan:
                dict_n = parse_n(wlan, dict_n)
            else:
                fd = open("catcher.txt", "a")
                fd.write(wlan)
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


    return
    

if __name__ == "__main__":
    main()


