import json
import sys, os


# TODO: Figure out I want to make this file
# Is it going to be dynamic across all analysis
# Only needs to pull out data and make percentages
# Want specific analyzer for each dataset, or just one?

output_a = 'a_gen_analysis.txt'
output_n = 'n_gen_analysis.txt'


# Channel, Frequency, Signal, Noise, SNR, Rate
def analyze_a(file):
    interest = ['Channel', 'Frequency', 'Signal', 'Noise', 'SNR', 'rate']
    
    fa = open(file, 'r')
    data = json.load(fa)
    fa.close()

    total_packets = data['Count']
    analysis = {}

    for item in interest:
        analysis[item] = {}
        for key in data[item]:
            value = data[item][key]
            analysis[item][key] = float(value) / float(total_packets)

    fa = open(output_a, 'n')
    fa.write('\n')
    fa.write(json.dumps(analysis, indent=2))
    fa.close()



# Channel, Frequency, Signal, Noise, SNR, Rate, Bandwidth
def analyze_n(file):
    interest = ['Channel', 'Frequency', 'Signal', 'Noise', 'SNR', 'rate'] #Ignoring bandwidth for now
    
    fn = open(file, 'r')
    data = json.load(fn)
    fn.close()

    total_packets = data['Count']
    analysis = {}

    for item in interest:
        analysis[item] = {}
        for key in data[item]:
            value = data[item][key]
            analysis[item][key] = float(value) / float(total_packets)

    fn = open(output_n, 'n')
    fn.write('\n')
    fn.write(json.dumps(analysis, indent=2))
    fn.close()


def main():

    try:
        a_file = sys.argv[1]
        n_file = sys.argv[2]
    except:
        print( "Usage: python {} a_file n_file ".format(sys.argv[0]))
        exit(1)

    analyze_a(a_file)
    analyze_n(n_file)


if __name__ == '__main__':
    main()
