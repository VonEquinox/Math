// Independent checker: hypercube paths of half-plane signs. No signed-triple formula,
// no precomputed first-enumerator orders, sphere capacities, or reflection quotient.
// ./audit facetmasks.txt [threshold=25]. Columns: type, nf, viable signed walks, nodes.
#include <iostream>
#include <string>
#include <fstream>
#include <array>
#include <vector>
#include <set>
#include <cstdlib>
using namespace std;using U=unsigned long long;
int threshold,tr[84];struct B{U a=0,b=0;void put(int i){(i<64?a:b)|=1ull<<(i%64);}int n(){return __builtin_popcountll(a)+__builtin_popcountll(b);}friend B operator&(B x,B y){return{x.a&y.a,x.b&y.b};}};
B cross[512];bool admiss[512];long long full,nodes;
void walk(int chamber,int left,B alive){nodes++;if(!admiss[chamber]||(alive=alive&cross[chamber]).n()<threshold)return;
 if(!left){full++;return;}
 for (int i=1;i<9;i++)if((left>>i)&1)walk(chamber^(1<<i),left^(1<<i),alive);
}
int main(int argc,char**argv){if(argc<2)return 1;threshold=argc>2?atoi(argv[2]):25;
 int t=0;for(int i=0;i<9;i++)for(int j=0;j<i;j++)for(int k=0;k<j;k++)tr[t++]=(1<<i)|(1<<j)|(1<<k);
 for(int s=0;s<512;s++)for(int i=0;i<84;i++)if((tr[i]&s)!=0&&(tr[i]&s)!=tr[i])cross[s].put(i);
 ifstream file(argv[1]);string id;int nf;
 while(file>>id>>nf){vector<set<int>> F(5);for(int j=0;j<nf;j++){int f;file>>f;for(int s=1;s<512;s++)if((s&f)==s)F[__builtin_popcount(s)].insert(s);}
 B tris;for(int k=0;k<84;k++)if(F[3].count(tr[k]))tris.put(k);
 int chi[512]={};for(int s=0;s<512;s++)for(int d=1;d<=4;d++)for(int f:F[d])if((f&s)==f)chi[s]+=(d%2?1:-1);
 for(int s=0;s<512;s++)admiss[s]=chi[s]==1&&chi[511^s]==1;
 full=nodes=0;for(int s=0;s<512;s+=2){ // p[0]=0 first direction; choose sign of item 0 positive
   if(!admiss[s])continue;walk(s^1,510,tris&cross[s]);}
 cout<<id<<" "<<nf<<" "<<full<<" "<<nodes<<"\n";
 }}
