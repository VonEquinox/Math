// Enumerate generic 2-plane transverse ranks for 9-vertex simplicial 4-polytopes.
// C++17, standard library only. Input: ID, number of tetrahedra, their vertex masks.
// Enumerates all signed orders up to rotation (label 0 first), global reversal of all
// signs, orientation of projective axis (next label < previous label). Last quotient
// is safe: reflecting projective order at label 0 flips signs on the other eight lifts.
#include <array>
#include <vector>
#include <string>
#include <cstdio>
#include <algorithm>
#include <fstream>
#include <iostream>
#include <cstdint>
#include <cassert>
#include <numeric>
using namespace std;
using u64=uint64_t;
int pc(int x){return __builtin_popcount(x);} int bit(int i){return 1<<i;}
struct Tris{u64 lo=0,hi=0;void add(int i){if(i<64)lo|=(1ull<<i);else hi|=(1ull<<(i-64));} int common(const Tris&x)const{return __builtin_popcountll(lo&x.lo)+__builtin_popcountll(hi&x.hi);} };
int idx[512], mask[84];
struct Poly{string id; int nf,nt,raw=0,valid=0,connected=0,mx=0;vector<int> Fs;array<pair<int,int>,84> dual;bool ok[512];Tris T;};
struct W{int sign; vector<array<int,3>> tri; };
void init(Poly&P){
 bool face[512]={};for(auto F:P.Fs)for(int s=F;s;s=F&(s-1))face[s]=true;
 for(int b=0;b<512;b++){int chi=0;for(int s=b;s;s=b&(s-1))if(face[s])chi+=pc(s)%2?1:-1;P.ok[b]=(chi==1);}
 for(int i=0;i<84;i++)if(face[mask[i]]){P.T.add(i);vector<int> f;for(int j=0;j<P.nf;j++)if((P.Fs[j]&mask[i])==mask[i])f.push_back(j);assert(f.size()==2);P.dual[i]={f[0],f[1]};}
}
int main(int argc,char**argv){
 if(argc<2){cerr<<"input [detail-output/-] [threshold=25]"<<endl;return 1;}
 ofstream detail; if(argc>2 && string(argv[2])!="-")detail.open(argv[2]); const int threshold=argc>3?stoi(argv[3]):25;
 int n=0;for(int s=0;s<512;s++)if(pc(s)==3){idx[s]=n;mask[n++]=s;}
 assert(n==84); vector<Poly> Ps;ifstream f(argv[1]);string id;int nf;
 while(f>>id>>nf){Poly P;P.id=id;P.nf=nf;P.Fs.resize(nf);for(int&v:P.Fs)f>>v;init(P);Ps.push_back(P);}
 vector<W> words;
 for(int s=0;s<512;s+=2){W w;w.sign=s;
 for(int i=0;i<9;i++)for(int j=i+1;j<9;j++)for(int k=j+1;k<9;k++)if((((s>>i)^(s>>k))&1)==0&&(((s>>i)^(s>>j))&1)==1)w.tri.push_back({i,j,k});
 if(int(w.tri.size())>=threshold)words.push_back(w);}
 array<int,9> p={0,1,2,3,4,5,6,7,8};int iter=0;
 do{if(p[1]>p[8])continue;
 int pre[10]={0};for(int i=0;i<9;i++)pre[i+1]=pre[i]|bit(p[i]);
 for(const auto&w:words){++iter;Tris t;int S=0;
 for(int i=0;i<9;i++)if(w.sign&bit(i))S|=bit(p[i]);
 for(auto a:w.tri)t.add(idx[bit(p[a[0]])|bit(p[a[1]])|bit(p[a[2]])]);
 for(auto &P:Ps){int c=P.T.common(t);if(c<threshold)continue;P.raw++;
 bool ok=true;for(int j=0;j<9;j++){int a=S^pre[j];if(!P.ok[a]||!P.ok[511^a]){ok=false;break;}}
 if(!ok)continue;P.valid++;
 // A transversal convex section is ONE cycle; union forest of dual-tetrahedra recovers its components.
 int parent[32];iota(parent,parent+32,0);auto root=[&](int x){while(parent[x]!=x)x=parent[x];return x;};int merges=0;
 u64 lo=t.lo&P.T.lo,hi=t.hi&P.T.hi;
 for(int word=0;word<=1;word++){u64 m=word?hi:lo;while(m){int u=__builtin_ctzll(m)+64*word;m&=m-1;auto [a,b]=P.dual[u];a=root(a);b=root(b);if(a!=b){++merges;parent[a]=b;}}}
 if(merges!=c-1)continue;P.connected++;P.mx=max(P.mx,c);
 if(detail.is_open()){detail<<P.id<<' '<<c<<' '<<w.sign<<' ';for(auto v:p)detail<<v;detail<<'\n';}
 }
 }}while(next_permutation(p.begin()+1,p.end()));
 cerr<<Ps.size()<<" types; "<<iter<<" signed orders; "<<words.size()<<" words after ray-capacity filter\n";
 for(auto&P:Ps)cout<<P.id<<" "<<P.nf<<" "<<P.raw<<" "<<P.valid<<" "<<P.connected<<" "<<P.mx<<"\n";
}
