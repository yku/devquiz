#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <cstring>
#include <cstdio>
#include <ctime>
#include <algorithm>
#include <queue>
#include <map>
#include <set>
#include <iomanip>

#define _DEBUG_    0
#define _SCORE_    1
#define _SKIP_     0

#define TIMEOUT   30
#define MAX_WIDTH  6
#define MAX_HEIGHT 6

using namespace std;

long LX, RX, UX, DX;

int answers[MAX_WIDTH][MAX_HEIGHT] = { 0 };
int questions[MAX_WIDTH][MAX_HEIGHT] = { 0 };

typedef struct {
    string state, route;
    int depth;
    int cost;
    char dir;
} NODE;

typedef struct {
    string route;
    int cost;
    char dir;
} PARM;

struct cmp {
    bool operator() (NODE lhs, NODE rhs) { return lhs.cost > rhs.cost; }
};

int GetSpacePos(string b) {
    return b.find("0");
}

string GetFinalState(string bi)
{
    static const char t[] = { '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A',
                              'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                              'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                              'V', 'W', 'X', 'Y', 'Z', '0' };
    string bf(bi);

    for(int i = 0; i < bf.size(); i++) {
        if(bf[i] == '=') continue;
        bf[i] = t[i];
    }
    bf[bf.size()-1] = '0'; 
    return bf;
}

void CreateAdjList(int w, int h, int adj[][5])
{
    memset(adj, -1, w * h * 5 * sizeof(int)); // 4ではなく5なのは番兵
 
    for(int i = 0; i < w * h; i++) {
        int j = 0;
        // 横方向の隣接チェック
        if(i % w - 1 > -1) adj[i][j++] = i - 1;
        if(i % w + 1 < w)  adj[i][j++] = i + 1;
        // 縦方向の隣接チェック
        if(i - w > -1) adj[i][j++] = i - w;
        if(i + w < w * h) adj[i][j++] = i + w;
    }
#if _DEBUG_
    for(int i = 0; i < w * h; i++) {
        cout << "[" << i << "] "; 
        for(int j = 0; j < 5; j++) {
            cout << adj[i][j] << " ";
        }
        cout << endl;
    }
#endif
}

string GetOperation(const int n, const int sp, const int w) 
{
    string ret = "";

    if(n == (sp - 1))      ret = "L";
    else if(n == (sp + 1)) ret = "R";
    else if(n == (sp - w)) ret = "U";
    else if(n == (sp + w)) ret = "D";
    
    return ret;
}

string ReverseOperation(string op)
{
    string ret = "";
    for(int i = 0; i < op.size(); i++) {
        switch(op[i]) {
            case 'L': ret += "R"; break;
            case 'R': ret += "L"; break;
            case 'U': ret += "D"; break;
            case 'D': ret += "U"; break;
        }
    }
    return ret;
}

bool DecUsedOperation(string op)
{

    for(int i = 0; i < op.size(); i++) {
        switch(op[i]) {
            case 'L': LX--; break;
            case 'R': RX--; break;
            case 'U': UX--; break;
            case 'D': DX--; break;
            default: 
                cout << "Invalid Operation" << endl;
                return false;
        }
    }
    if(LX >= 0 and RX >= 0 and UX >= 0 and DX >= 0) return true;
    cout << "LX=" << LX << " RX=" << RX << " UX=" << UX << " DX=" << DX << endl;
    return false;
}

void PrintBoard(int w, int h, string b)
{
    for(int i = 0; i < b.size(); i++) {
        cout << b[i];
        if((i+1) % w == 0) cout << endl;
    }
}

int CalculateCost(int w, int h, string b1, string b2)
{
    int ret = 0;
    for(int i = 0; i < b1.size(); i++) {
        if(b1[i] == '0' or b1[i] == '=') continue;
        int target = b2.find(b1[i]);
        int x = i % w;
        int y = i / w;
        int xx = target % w;
        int yy = target / w;
        
        if(x == xx and y == yy) continue;
        ret += abs(xx - x) + abs(yy - y);
        
        if(x == xx) {
            // equal col
            if(y < yy) {
                for(int j = i; j < target; j += w) {
                    if(b1[j] == '=') { ret += 2; break; }
                }
            } else {
                for(int j = i; j > target; j -= w) {
                    if(b1[j] == '=') { ret += 2; break; }
                }
            }
        } else if(y == yy) {
            // equal row
            if(x < xx) {
                for(int j = i; j < target; j++) {
                    if(b1[j] == '=') { ret += 2; break; }
                }
            } else {
                for(int j = i; j > target; j--) {
                    if(b1[j] == '=') { ret += 2; break; }
                }
            }
        } 
#if _DEBUG_
        int t = 0;
        t = abs(xx - x) + abs(yy - y);
        cout << t << " ";
        if((i+1) % w == 0) cout << endl;
#endif
    }

    return ret;
}

string GASearch(const int w, const int h, const string bi, const string bf)
{

}

string AstarSearch(const int w, const int h, const string bi, const string bf)
{
    string ret = "";
    NODE init, goal;
    priority_queue<NODE, vector<NODE>, cmp> open;
    map<string, PARM> close;
    bool clear = false;
    clock_t stime = clock();
    int adj[w * h][5];

    init.state = bi;
    init.route = "";
    init.depth = 0;
    init.cost  = 0;
    init.dir   = 'F';
    open.push(init);
    
    goal.state = bf;
    goal.route = "";
    goal.depth = 0;
    goal.cost  = 0;
    goal.dir   = 'B';
    open.push(goal);
    
    CreateAdjList(w, h, adj);
    while(!open.empty()) {
        NODE node = open.top();
        string target;
        PARM parm;
        clock_t etime = clock();
        if((etime - stime) / CLOCKS_PER_SEC > TIMEOUT) { return ""; } 
        open.pop();
        if(node.dir == 'F') target = bf;
        else                target = bi;
        parm.route = node.route;
        parm.cost = CalculateCost(w, h, node.state, target) + node.depth;
        parm.dir = node.dir;
        close.insert(pair<string, PARM>(node.state, parm));
        if(node.state == bf and clear) { 
            DecUsedOperation(node.route);
            return node.route; 
        }
        int space_pos = node.state.find("0");
        int n;
        for(int i = 0; (n = adj[space_pos][i]) != -1; i++) {
            if(node.state[n] == '=') continue;
            string next_state(node.state);
            string route;
            
            next_state[space_pos] = node.state[n];
            next_state[n] = '0';
            
            if(close.count(next_state) != 0) {
                if(close[next_state].dir != node.dir) {
                    string f_route, b_route;
                    
                    if(close[next_state].dir == 'B') {
                        f_route = node.route + GetOperation(n, space_pos, w);
                        b_route = close[next_state].route;
                    }else{
                        f_route = close[next_state].route;
                        b_route = node.route + GetOperation(n, space_pos, w);  
                    }
                    reverse(b_route.begin(), b_route.end());
                    route = f_route + ReverseOperation(b_route);
                    clear = true;
                }else{
                    int cost, prev_cost;
                    cost = CalculateCost(w, h, next_state, target) + node.depth + 1;
                    prev_cost = close[next_state].cost;
                    if(cost >= prev_cost) { continue; }
                    close.erase(next_state);
                } 

            }
            
            NODE next;
            next.state = clear ? bf : next_state;
            next.route = clear ? route : node.route + GetOperation(n, space_pos, w);
            next.cost = clear ? 0 : CalculateCost(w, h, next_state, target) + node.depth + 1;
            next.depth = node.depth + 1;
            next.dir = node.dir;
            open.push(next);
        }
    }
    
    return ret;
}

int main()
{
    int N;
    scanf("%ld %ld %ld %ld %d", &LX, &RX, &UX, &DX, &N);

#if _SKIP_
    ifstream ifs("result.txt");
    if(ifs.fail()) {
        cerr << "Could not open file:result.txt\n";
        exit(8);
    }
#endif


#if _SCORE_
    long lx, rx, ux, dx;
    lx = LX;
    rx = RX;
    ux = UX;
    dx = DX;

    clock_t stime = clock();
#endif
    for(int i = 0; i < N; i++) {
        int wi, hi;
        string s, bi, bf, ret;
        cin >> s;
        sscanf(s.c_str(), "%d,%d,", &wi, &hi);
        bi = s.substr(4);
        bf = GetFinalState(bi);
        questions[wi][hi]++;
#if _RESUME_
        string str = "";
        getline(ifs, str);
        if(str != ""){ 
            cout << str << endl;
            DecUsedOperation(str);
            answers[wi][hi]++;
            continue;
        }
#endif
        if(wi != 3 or hi != 3) { cout << endl; continue; }
        ret = AstarSearch(wi, hi, bi, bf); 
        if(ret != "") answers[wi][hi]++;
        cout << ret << endl;
    }
#if _SCORE_
    clock_t etime = clock();
    int a = 0;
    cout << "TIME:" << (etime - stime) / CLOCKS_PER_SEC << "." << (etime - stime) % CLOCKS_PER_SEC << "[sec] " << endl;
    cout << "OPERATION:" << LX << "/" << lx << " " << RX << "/" << rx << " " << UX << "/" << ux << " " << DX << "/" << dx << endl; 
    cout << "TOTAL USED:" << (lx - LX) + (rx - RX) + (ux - UX) + (dx - DX) << endl;
    for(int h = 3; h <= MAX_HEIGHT; h++) {
        for(int w = 3; w <= MAX_WIDTH; w++) {
            cout << setw(4) << answers[w][h] << "/" << setw(4) << questions[w][h] << " ";
            a += answers[w][h];
        }
        cout << endl;
    }
    cout << "ANSWERS:" << setw(4) << a << "/" << N << endl;
#endif
    return 0;
}
