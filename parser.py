import pyshark
import sys, os

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
def parse_a(cap) {
    
}


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
def parse_n(cap) {

}

main() {
    # TODO Make this parse all packets within a directory
    # TODO Output statistics into another directory

    cap = pyshark.FileCapture('wireless_test.pcap')
    
    index = 0
    capture = True
    while capture:
        try:
            wlan = cap[index][1]
}


if __name__ == "__main__":
    main();


