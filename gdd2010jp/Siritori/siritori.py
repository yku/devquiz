#words = ["eat", "egg", "get", "gift", "see", "song", "take", "text"]

def get_words(filename):
    words = []
    for line in open(filename, 'r'):
        words.append(line[:-1])
    return words

def get_neighbour(g, s):
    ret = []
    for v in vertex:
        key = (s, v)
        if key in g and g[key] > 0:
            ret.append(v)
    return ret

def dfs(g, s, goal, route):
    r = route[:]
    r.append(s)
    if s == goal:
        if (len(r) %2) == 0: print r
        return
    l = g.copy()
    neighbours = get_neighbour(l, s)
    for n in neighbours:
        l[(s, n)] -= 1
        dfs(l, n, goal, r)

def get_easy_graph(g):
    dellist = []
    for k in g:
        t = (k[1], k[0])
        if t not in g or k == t: continue
    
        if g[k] >= g[t]:
            g[k] -= g[t]
            g[t] = 0 
            dellist.append(t)
        else:
            g[t] -= g[k]
            g[k] = 0 
            dellist.append(k)
    for d in dellist:
        del(g[d])
    

words = get_words("siritori2.txt")

g = {}
vertex = []
for w in words:
    s = w[0]
    e = w[-1]
    vertex.append(s)
    vertex.append(e)
    g.setdefault((s,e), 0)
    g[s,e] += 1
vertex = set(vertex)

get_easy_graph(g)
#for k in sorted(g.keys()):
#    print '%s %s' % (k, g[k])

dead_nodes = ["b", "h", "k", "l", "t", "u", "v", "x"]
r = []
dfs(g, "d", "b", r)
