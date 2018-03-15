import sys, os
import json


def get_dicts(type):
    if type == 'gen':
        return gen_template()
    elif type == 'dur' or type == 'rate':
        return cat_template()
    else:
        print 'Invalid type [{}], exiting.'.format(type)


def gen_template():
    gt               = {}
    gt['Count']      = 0
    gt['fc_retry']   = 0
    gt['Signal_dbm'] = {}
    gt['Noise_dbm']  = {}
    gt['Data_rate']  = {}
    gt['Duration']   = {}
    gt['SNR']        = {}

    return gt


def cat_template():
    dt            = {}
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



def main():
    try:
        j1 = sys.argv[1]
        j2 = sys.argv[2]

        o  = sys.argv[3]
    except Exception as e:
        print "Use: {} file1 file2 output_file".format(sys.argv[0])

    with open(j1, 'r') as file1:
        d1 = json.load(file1)
    with open(j2, 'r') as file2:
        d2 = json.load(file2)

    if 'gen' in j1 and 'gen' in j1:
        script = 'gen'
    elif 'dur' in j1 and 'dur' in j2:
        script = 'dur'
    elif 'rate' in j1 and 'rate' in j2:
        script = 'rate'
    else:
        print "Both files must be same type [gen,dur,rate]. Exiting."
        exit(1)

    d = merger(d1, d2, script)

    fd = open(o, 'w')
    fd.write(json.dumps(d, indent=2))
    fd.close()

    print 'Done.'
    exit(0)

if __name__ == "__main__":
    main()
