import pyshark
import math

def parse(packet, d):
    
    # For cap['WLAN']
    wlan_interest  = ['fc_retry', 'fc_type']
    # For cap['WLAN_RADIO']
    radio_interest = ['Signal_dbm', 'Noise_dbm', 'Data_rate']

    d['Count'] += 1

    snr_true = True

    for item in wlan_interest:
        data = packet['WLAN'].get(item)
        if type(data) == type(None):            
            continue

        if item == 'fc_retry':
            d[item] += int(data)
        elif item == 'fc_type':
            if data in d[item]:
                d[item][data] += 1
            else:
                d[item][data] = 1
   
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
        s = math.pow(10, (float(signal)/10.0))
        n = math.pow(10, (float(noise)/10.0))

        snr = s/n

        if snr in d['SNR']:
            d['SNR'][snr] += 1
        else:
            d['SNR'][snr] = 1


    return d
