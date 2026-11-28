#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <random>
#include <string>
#include <vector>
using B=__uint128_t;
int pc(B x){return __builtin_popcountll((uint64_t)x)+__builtin_popcountll((uint64_t)(x>>64));}
int first(B x){uint64_t lo=(uint64_t)x;return lo?__builtin_ctzll(lo):64+__builtin_ctzll((uint64_t)(x>>64));}
const B ALL=(B(1)<<81)-1;
std::vector<B> cubes,clauses;
std::array<std::array<int,4>,81> words;
std::mt19937_64 rng(2026112801);
uint64_t nodes=0; bool timedout=false; int limit=16, seconds=120; B answer=0;
auto started=std::chrono::steady_clock::now();

void initialize(std::string kind){
 for(int i=0;i<81;++i)words[i]={i/27,(i/9)%3,(i/3)%3,i%3};
 for(int fixed=0;fixed<4;++fixed)for(int a=0;a<3;++a)
 for(int i=0;i<27;++i){int excluded[3]={i/9,(i/3)%3,i%3};B C=0;
  for(int v=0;v<81;++v){if(words[v][fixed]!=a)continue; bool ok=true;int l=0;
   for(int j=0;j<4;++j)if(j!=fixed&&words[v][j]==excluded[l++])ok=false;
   if(ok)C|=B(1)<<v;
  }cubes.push_back(C);
 }
 if(kind=="star")for(int v=0;v<81;++v){B C=0;for(int u=0;u<81;++u){int d=0;for(int j=0;j<4;++j)d+=words[u][j]!=words[v][j];if(d<=1)C|=B(1)<<u;}clauses.push_back(C);}
 if(kind=="face"||kind.rfind("cover",0)==0){
  int q=kind=="face"?1:1+std::stoi(kind.substr(5));
  for(int j=0;j<4;++j)for(int k=j+1;k<4;++k){
   std::array<B,9> fs{};
   for(int a=0;a<3;++a)for(int b=0;b<3;++b)for(int v=0;v<81;++v)if(words[v][j]==a&&words[v][k]==b)fs[3*a+b]|=B(1)<<v;
   // No q of the nine disjoint faces may all be ghost-free.
   for(int sel=1;sel<512;++sel)if(__builtin_popcount((unsigned)sel)==q){B C=0;for(int a=0;a<9;++a)if(sel>>a&1)C|=fs[a];clauses.push_back(C);}
  }
 }
}
void report(B H,std::string status){
 std::cout<<status<<" count="<<pc(H)<<" nodes="<<nodes<<" words=";
 for(int v=0;v<81;++v)if(H&(B(1)<<v)){std::cout<<'[';for(int j=0;j<4;++j)std::cout<<words[v][j];std::cout<<']';}std::cout<<std::endl;
}

// Reversible integer propagation. This is a direct exact search, not a
// floating-point infeasibility claim. Timeouts are reported explicitly.
bool dfs(B T,B F){
 ++nodes;if((nodes&4095)==0&&std::chrono::duration<double>(std::chrono::steady_clock::now()-started).count()>seconds){timedout=true;return false;}
 std::vector<B> active;
 for(;;){
  if(pc(T)>limit||T&F)return false;
  B U=ALL^(T|F),addT=0,addF=0;active.clear();
  for(B C:cubes){int t=pc(C&T);B u=C&U;int n=pc(u);
   if(t==1){if(!n)return false;if(n==1)addT|=u;else active.push_back(u);}
   else if(!t&&n==1)addF|=u;
  }
  for(B C:clauses)if(!(C&T)){B u=C&U;if(!u)return false;if(!(u&(u-1)))addT|=u;else active.push_back(u);}
  if(!addT&&!addF)break;
  T|=addT;F|=addF;
 }
 if(active.empty()){answer=T;return true;}
 int remaining=limit-pc(T);if(remaining<=0)return false;
 std::sort(active.begin(),active.end(),[](B a,B b){return pc(a)<pc(b);});
 B used=0;int lb=0;for(B C:active)if(!(used&C)){used|=C;if(++lb>remaining)return false;}
 std::array<int,81> score{};
 for(B C:active){int n=pc(C);while(C){int v=first(C);C&=C-1;score[v]+=2520/n;}}
 B branch=active[0];
 int bestsum=-1;for(B C:active){if(pc(C)>pc(branch))break;int sum=0;B D=C;while(D){int v=first(D);D&=D-1;sum+=score[v];}if(sum>bestsum){bestsum=sum;branch=C;}}
 std::vector<int> choices;while(branch){int v=first(branch);branch&=branch-1;choices.push_back(v);}
 std::sort(choices.begin(),choices.end(),[&](int a,int b){return score[a]>score[b];});
 for(int v:choices){if(dfs(T|(B(1)<<v),F))return true;if(timedout)return false;F|=B(1)<<v;}
 return false;
}

int cost(B H){int c=0;for(B C:cubes)c+=pc(C&H)==1;for(B C:clauses)c+=!(C&H);return c;}
void anneal(int secs){
 int best=1000;auto st=std::chrono::steady_clock::now();uint64_t iter=0;
 while(std::chrono::duration<double>(std::chrono::steady_clock::now()-st).count()<secs){
  B H=1;while(pc(H)<limit)H|=B(1)<<(rng()%81);int cur=cost(H);
  for(int step=0;step<30000;++step){
   int a,b;do{a=rng()%81;}while(!(H&(B(1)<<a))||a==0);do{b=rng()%81;}while(H&(B(1)<<b));
   B next=H^(B(1)<<a)^(B(1)<<b);int nc=cost(next);
   double temp=.08+2.2*(1.-double(step%3000)/3000.);
   if(nc<=cur||double(rng())/double(UINT64_MAX)<std::exp((cur-nc)/temp)){H=next;cur=nc;}
   if(cur<best){best=cur;std::cout<<"anneal cost="<<best<<" ";report(H,"candidate");}
   if(!cur){answer=H;return;}++iter;
  }
 }
 std::cout<<"anneal iterations="<<iter<<" best_cost="<<best<<std::endl;
}
int main(int argc,char**argv){
 std::string kind=argc>1?argv[1]:"star";limit=argc>2?std::stoi(argv[2]):16;seconds=argc>3?std::stoi(argv[3]):120;
 std::string mode=argc>4?argv[4]:"dfs";initialize(kind);
 std::cout<<"kind="<<kind<<" limit="<<limit<<" cubes="<<cubes.size()<<" clauses="<<clauses.size()<<std::endl;
 if(mode=="anneal"){anneal(seconds);if(answer)report(answer,"SAT");else std::cout<<"HEURISTIC_NO_SOLUTION"<<std::endl;return 0;}
 started=std::chrono::steady_clock::now();
 for(int d=1;d<=3;++d){
  B F=0;int q=0;for(int j=4-d;j<4;++j)q+=j==0?27:j==1?9:j==2?3:1;
  for(int v=1;v<81;++v){int w=0;for(int j=0;j<4;++j)w+=words[v][j]!=0;if(w<d)F|=B(1)<<v;}
  std::cout<<"branch min distance="<<d<<std::endl;
  if(dfs(1|(B(1)<<q),F)){report(answer,"SAT");return 0;}
  if(timedout){std::cout<<"TIMEOUT nodes="<<nodes<<std::endl;return 0;}
 }
 std::cout<<"UNSAT exact completed nodes="<<nodes<<std::endl;
}
