#include <iostream>
#include <vector>
#include <string>
#include <cstring>
#include <ctime>
#include <algorithm>
#include <queue>
#include <map>

#define _DEBUG_ 0
#define _TIME_  1

using namespace std;

long LX, RX, UX, DX;
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

// 事前に作ったほうがよい
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

int GetSpacePos(string b)
{
    for(int i = 0; i < b.size(); i++) {
        if(b[i] == '0'){
            return i;
        }
    }
    return -1;
}

void PrintBoard(int w, int h, string b)
{
    for(int i = 0; i < b.size(); i++) {
        cout << b[i];
        if((i+1) % w == 0) cout << endl;
    }
    cout << endl;
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

string Search(int w, int h, string bi, string bf, int adj[][5])
{
    queue<string> q;
    map<string, string> visited;
    q.push(bi);
    visited.insert(pair<string, string>(bi, ""));

    while(!q.empty()) {
        string state = q.front();
        q.pop();
        int space_pos = GetSpacePos(state);
        int n;
        for(int i = 0; (n = adj[space_pos][i]) != -1; i++) {
            if(state[n] == '=') continue;
            string next_state(state);
            next_state[space_pos] = state[n];
            next_state[n] = '0';
            string op = visited[state];
            op += GetOperation(n, space_pos, w);

            if(next_state == bf) {
                //PrintBoard(w, h, next_state);
                if(DecUsedOperation(op)) return op;             
                else                     return "";
            }else if(visited.count(next_state) == 0) {
                q.push(next_state);
                visited.insert(pair<string, string>(next_state, op));
/*
#if _DEBUG_
                PrintBoard(w, h, next_state);
#endif
*/
            }
        }
    }
    return "";
}

int main()
{
    int N;
    scanf("%ld %ld %ld %ld %d", &LX, &RX, &UX, &DX, &N);
 
#if _TIME_
    long lx, rx, ux, dx;
    lx = LX;
    rx = RX;
    ux = UX;
    dx = DX;
#endif

#if _TIME_
    clock_t stime = clock();
#endif
    //N = 1;
    for(int i = 0; i < N; i++) {
        int wi, hi;
        string s, bi, ret;
        
        cin >> s;
        sscanf(s.c_str(), "%d,%d,", &wi, &hi);
        bi = s.substr(4);
        
        //bi =  "168452=30";
        //bi =  "867254301";
        //bi =  "123405786";
        //wi = hi = 3;
        // とりあえず3x3をとくの目標に
        if(wi != 3 or hi != 3){ cout << endl;  continue; }
        
        int buf[wi * hi][5];
        //PrintBoard(wi, hi, bi);
        CreateAdjList(wi, hi, buf);
        ret = Search(wi, hi, bi, GetFinalState(bi), buf);
        cout << ret << endl;
    }

#if _TIME_
    clock_t etime = clock();
    cout << "TIME:" << (etime - stime) << "[usec] " << endl;
    cout << "OPERATION:" << LX << "/" << lx << " " << RX << "/" << rx << " " << UX << "/" << ux << " " << DX << "/" << dx << endl; 
    cout << "TOTAL USED:" << (lx - LX) + (rx - RX) + (ux - UX) + (dx - DX) << endl;
#endif
    return 0;
}
