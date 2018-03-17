import pyshark
import math

def parse(packet, d):
    
    # For cap['WLAN']
    wlan_interest  = ['fc_retry']
    # For cap['WLAN_RADIO']
    radio_interest = ['Signal_dbm', 'Noise_dbm']

    snr_true = True

    dur = packet['WLAN_RADIO'].get('Data_Rate')
    if type(dur) == type(None):
        d['omitted'] += 1
        return d

    if dur in d:
        d[dur]['Count'] += 1
    else:
        d[dur] = {}
        d[dur]['fc_retry'] = 0
        d[dur]['Count'] = 1

    for item in wlan_interest:
        retry = packet['WLAN'].get(item)
        if type(retry) == type(None):            
            continue

        d[dur][item] += int(retry)
   
    for item in radio_interest:
        data = packet['WLAN_RADIO'].get(item)
        
        if item not in d[dur]:
            d[dur][item] = {}
        
        if type(data) == type(None):
            if item == 'Signal_dbm' or item == 'Noise_dbm':
                snr_true = False

            if 'omitted' in d[dur][item]:
                d[dur][item]['omitted'] += 1
            else:
                d[dur][item]['omitted'] = 1
        else:
            if data in d[dur][item]:
                d[dur][item][data] += 1
            else:
                d[dur][item][data] = 1

    # Calculate SNR
    if snr_true:
        signal = packet['WLAN_RADIO'].get('Signal_dbm')
        noise  = packet['WLAN_RADIO'].get('Noise_dbm')
        s = math.pow(10, (signal/10.0))
        n = math.pow(10, (noise/10.0))

        snr = s/n

        if 'SNR' not in d[dur]:
            d[dur]['SNR'] = {}

        if snr in d[dur]['SNR']:
            d[dur]['SNR'][snr] += 1
        else:
            d[dur]['SNR'][snr] = 1


    return d

