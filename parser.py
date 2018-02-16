import pyshark
import sys, os
import json


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
    interest = {'Channel': 1, 'Frequency': 2, 'Signal': 3, 'Noise': 6, 'Rate': 9}

    dict['Count'] += 1

    for item in interest:
        index = interest[item]
        data = capture[index].split(': ')[1]

        if data in dict[item]:
            dict[item][data] += 1
        else:
            dict[item][data] = 1

    return dict


# 0  - Channel
# 2  - Duration
# 3  - MCS Index
# 7  - Signal Strength
# 10 - PHY Type
# 12 - Data Rate
# 15 - Frequency
# 16 - Noise Level
# 19 - Preamble
# 21 - Bandwidth
def parse_n(cap, dict):
    capture = cap.split('\n')[1:]
    interest = {'Channel': 0, 'Signal': 7, 'Rate': 12, 'Frequency': 15, 'Noise': 16, 'Bandwidth': 21}

    dict['Count'] += 1

    for item in interest:
        index = interest[item]
        data = capture[index].split(': ')[1]

        if data in dict[item]:
            dict[item][data] += 1
        else:
            dict[item][data] = 1

    return dict


def main():
    # TODO Make this parse all packets within a directory
    # TODO Output statistics into another directory

    cap = pyshark.FileCapture('wireless_test.pcap')
    
    index = 0

    dict_a = {}
    dict_a['Count'] = 0
    dict_a['Channel'] = {}
    dict_a['Frequency'] = {}
    dict_a['Signal'] = {}
    dict_a['Noise'] = {}
    dict_a['Rate'] = {}

    dict_n = {}
    dict_n['Count'] = 0
    dict_n['Channel'] = {}
    dict_n['Frequency'] = {}
    dict_n['Signal'] = {}
    dict_n['Noise'] = {}
    dict_n['Rate'] = {}
    dict_n['Bandwidth'] = {}

    while True:
        try:

            # Keep track of how many we've done in case of failure
            if (index % 10 == 0):
                ft = open("tracker.txt", "w")
                ft.write(str(index))
                ft.close

            wlan = str(cap[index][1])

            if '802.11a' in wlan:
                dict_a = parse_a(wlan, dict_a)
            elif '802.11n' in wlan:
                dict_n = parse_n(wlan, dict_n)
            else:
                fd = open("catcher.txt", "a")
                fd.write(wlan)
                fd.write('\n')
                fd.close
            index += 1
        except Exception as e:
            print e
            print "\nDone\n"
            break

    fn = open("n.txt", "a")
    fn.write(json.dumps(dict_n))
    fn.write('\n')
    fn.close

    fa = open("a.txt", "a")
    fa.write(json.dumps(dict_a))
    fa.write('\n')
    fa.close


    return
    

if __name__ == "__main__":
    main()


