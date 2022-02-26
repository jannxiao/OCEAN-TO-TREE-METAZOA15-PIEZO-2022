#! python

import random
import sys

color_annotation = sys.argv[1] #color-annotation.txt
before_tree = sys.argv[2]
after_tree = sys.argv[3] 
itol_map = sys.argv[4] #itol-friendly-annotated-identifier-to-color-map.txt


#make random colors for elements based on input map
element_colors = []
input_map = open( color_annotation, 'r')
for nextline in input_map:
    info = nextline[:-1].split('\t')
    if len(info) == 2:
        element = info[0]
        color = info[1]
    elif len(info) == 1:
        element = info[0]
        color = "#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])
    else:
        print('map should be two column, tab separated, element followed by hex color')
        break
    element_colors.append( (element, color) )
input_map.close()

#parse newick tree
infile = open(before_tree,'r')
tree = infile.readline()
infile.close()

leftremoved = tree.replace('(','')
commasplit = leftremoved.split(',')

nodes = []
for item in commasplit:
    colonsplit = item.split(':')
    nodes.append(colonsplit[0])

#sort nodes by first character
nodes.sort()

#annotate color
annotated_map = []
nodes_annotated = []
for node in nodes:
    annotated = False
    for element, color in element_colors:
        if element in node:
            nodes_annotated.append(node + '[&!color='+color+']')
            annotated = True
            annotated_map.append( (node, color) )
    if not annotated:
        nodes_annotated.append(node)

#write nexus tree
outfile = open(after_tree,'w')
outfile.write('#NEXUS\n'+'begin taxa;\n')
outfile.write('\tdimensions ntax='+str(len(nodes))+';\n'+ '\ttaxlabels\n')
for node in nodes_annotated:
    outfile.write('\t'+node+'\n')
outfile.write(';\n'+'end;\n'+'\n'+'begin trees;\n')
outfile.write('\ttree tree_1 = '+tree+'\n'+'end;\n')
outfile.close()

output_map = open(itol_map,'w')
output_map.write('TREE_COLORS\n'+ 'SEPARATOR TAB\n'+'DATA\n')
for node, color in annotated_map:
    output_map.write(node + '\t' + 'label' + '\t')
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)
    rgb = 'rgb(' + str(r) + ', ' + str(g) + ', ' + str(b) + ')'
    output_map.write(rgb + '\t' + 'normal' + '\t' + '1\n')
output_map.write('\n')
output_map.close()

