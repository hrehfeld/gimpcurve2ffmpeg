import re
import argparse

#make generator
lower=0
upper=1
length=256
zerotoonestepped256gen = [lower + x*(upper-lower)/length for x in range(length)]

def formatForFFMPEG(values):
    serializedValues = values.split(' ')
    list = []
    for i in range (len(serializedValues)):
        if not list or zerotoonestepped256gen[i] - float(re.match(r"^[^////]*",list[-1]).group(0)) > 0.01:
            list.append('%s/%s' % (zerotoonestepped256gen[i], serializedValues[i]))
    return list

def main(args):
    #Open the curves file
    with open(args.curve_path,"r") as curvesfile:
        curvesString = curvesfile.read()
    values = re.findall(r'(?<=samples 256) [\d. ]*',curvesString)

    values = [formatForFFMPEG(value[1:]) for value in values]

    master, red, green, blue, alpha = values

    commandPrelim = 'curves=master="'

    command = commandPrelim + ' '.join(master) + '":red="' + ' '.join(red) +'":green="' + ' '.join(green) + '":blue="' + ' '.join(blue) + '"'


    print(command)

p = argparse.ArgumentParser(description='Tool to convert a color curves map from GIMP to a curves filter that can be inserted into the -complex_filter. Note that you still need to append the input and output streams onto either side of the command.')

p.add_argument('curve_path', help='Input GIMP Color Curve Preset File')

args = p.parse_args()


main(args)
