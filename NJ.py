from sys import *
import pygraphviz as pgv

def parseInput(arg):
    #reads the file given, parses it and returns a dict of dicts
    try:
        dists = {}
        #opens file
        infile = open(arg, "r")
        for line in infile:
            line = line.strip()
            items = line.split(" ")
            if items[0] in dists:
                vals = dists.get(items[0])
                if items[1] not in vals:
                    vals[items[1]] = float(items[2])
                    dists[items[0]] = vals
            else:
                dists[items[0]] = {}
                dists[items[0]][items[1]] = float(items[2])
            if items[1] in dists:
                vals = dists.get(items[1])
                if items[0] not in vals:
                    vals[items[0]] = float(items[2])
                    dists[items[1]] = vals
            else:
                dists[items[1]] = {}
                dists[items[1]][items[0]] = float(items[2])
        return dists
    #file exception (i.e. cannot read file)
    except:
        print "failed to read in distance matrix"
        exit(1)
def neighbourJoining(dists):
    #runs the main nj algorithm
    T = pgv.AGraph()
    #list of clusters
    clusters = []
    for keyA in dists.keys():
        T.add_node(keyA)
        clusters.append(keyA)
    M = {}
    R = {}
    for keyA in dists.keys():
        R[keyA] = 0
        for keyB in dists[keyA].keys():
            R[keyA] += dists[keyA][keyB]/(len(clusters)-2)
    for keyA in dists.keys():
        M[keyA] = {}
        for keyB in dists[keyA].keys():
            M[keyA][keyB] = dists[keyA][keyB] - R[keyA] - R[keyB]

    while len(dists) > 2:
        #initialises the minimum value to the very first val in matrix
        minA = dists.keys()[0]
        minB = dists[minA].keys()[0]
        minval = M[minA][minB]
        for keyA in dists.keys():
            for keyB in dists[keyA].keys():
                val = M[keyA].get(keyB)
                if val < minval:
                    minval = val
                    minA = keyA
                    minB = keyB

        edgeA = (dists[minA][minB]-R[minB]+R[minA])/2
        edgeB = (dists[minA][minB]+R[minB]-R[minA])/2
        clusters.remove(minA)
        clusters.remove(minB)
        newcluster = (minA+'-'+minB)
        clusters.append(newcluster)
        T.add_edge(minA, newcluster, label=str(edgeA), len=max(1, edgeA))
        T.add_edge(minB, newcluster, label= str(edgeB), len=max(1, edgeB))
        print (str(minA) + " " + str(newcluster) + " " + str(edgeA))
        print (str(minB) + " " + str(newcluster) + " " + str(edgeB))
        newdists = {}
        for cluster in clusters:
            if cluster in dists:
                dists[cluster][newcluster] = (dists[cluster][minA] + dists[cluster][minB] - dists[minA][minB])/2
                del dists[cluster][minA]
                del dists[cluster][minB]
                newdists[cluster] = dists[cluster][newcluster]
        del dists[minA]
        del dists[minB]
        dists[newcluster] = newdists

        if len(dists) == 2:
            break
        R = {}
        for keyA in dists.keys():
            R[keyA] = 0
            for keyB in dists[keyA].keys():
                R[keyA] += dists[keyA][keyB]/(len(dists)-2)
        clusters = []
        for keyA in dists.keys():
            clusters.append(keyA)

        M = {}
        for keyA in dists.keys():
            M[keyA] = {}
            for keyB in dists[keyA].keys():
                M[keyA][keyB] = (dists[keyA][keyB] - R[keyA] - R[keyB])


    newcluster = [(clusters[0])+'-'+clusters[1]]
    T.add_edge(clusters[0], clusters[1], label = str(dists[clusters[0]][clusters[1]]), len=max(1, dists[clusters[0]][clusters[1]]))
    print (str(clusters[0]) + " " + str(clusters[1]) + " " + str(dists[clusters[0]][clusters[1]]))
    return T


def main():
    try:
        dists = parseInput(argv[1])
    except:
        print "please provide distance matrix"
        exit(1)
    T = neighbourJoining(dists)
    T.draw("tree.png",prog="neato")
    #print dists.keys()[0]
main()
