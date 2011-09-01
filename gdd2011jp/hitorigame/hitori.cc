#include <iostream>
#include <vector>
#include <string>
#include <cstring>
#include <queue>
#include <algorithm>

using namespace std;

/*
 * Op1 5の倍数を取り除く
 * Op2 半分にする。端数は切り捨て。
 * Condition 集合が空になるor無限に続く場合探索打ち切り
 */
int calcMinOperation(vector<int> root) 
{
    queue<vector<int> > q;
    queue<int> d;
    int depth; 

    q.push(root);
    d.push(0);
    
    while(!q.empty()) {
        vector<int> v = q.front();
        vector<int> left, right;
        
        q.pop();
        depth = d.front() + 1;
        d.pop();
        // Op1. vから5の倍数を取り除く操作
        for(int i = 0; i < v.size(); i++) 
            if(v[i] % 5) left.push_back(v[i]);
        // Op2. vの各要素を半分にする操作
        for(int i = 0; i < v.size(); i++) 
            right.push_back(v[i] / 2);
        // 5の倍数を取り除く操作後でも要素数が
        // 変わらないものは無限に続くので探索打ち切り
        if(left.size() != v.size()){ 
            if(left.empty()) break;
            q.push(left);
            d.push(depth);
        }
        q.push(right);
        d.push(depth);
    }

    return depth;
}

int main()
{
    int T;
    
    scanf("%d", &T);
    
    for(int t = 1; t <= T; t++) {
        int N, n, ret;
        vector<int> v;
        scanf("%d", &N);
        for(int i = 0; i < N; i++) {
            scanf("%d", &n);
            v.push_back(n);
        }
        ret = calcMinOperation(v);
        cout << ret << endl;
    }
}
