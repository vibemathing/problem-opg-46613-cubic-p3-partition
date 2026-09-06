// Candidate-side exhaustive construction traces; no isomorphism pruning.
// Completeness uses Schmidt STACS 2010, Theorem 2.5, plus degree monotonicity.
#include <array>
#include <cstdint>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>
#include <algorithm>
#include <chrono>
using Mask=std::uint32_t;
struct Graph { int n=0; std::array<Mask,32> adj{}; };
const auto started=std::chrono::steady_clock::now();
std::array<std::uint64_t,33> traces{}, matching_nodes{}, matching_leaves{}, deletion_tests{};
std::map<std::string,std::uint64_t> spectra;
void require(bool b,const char* m) { if(!b) throw std::runtime_error(m); }
int first(Mask m) { require(m!=0,"empty bit scan"); return __builtin_ctz(m); }
Mask bit(int v) { require(0<=v && v<31,"label out of range"); return Mask(1)<<v; }
Mask all(int n) { return (Mask(1)<<n)-1; }
void edge(Graph& g,int u,int v) { require(u!=v && !(g.adj[u]&bit(v)),"loop or duplicate edge"); g.adj[u]|=bit(v);g.adj[v]|=bit(u); }
void erase(Graph& g,int u,int v) { require(g.adj[u]&bit(v),"missing edge");g.adj[u]^=bit(v);g.adj[v]^=bit(u); }
std::vector<std::pair<int,int>> edges(const Graph& g) {
 std::vector<std::pair<int,int>> e;
 for(int u=0;u<g.n;++u) for(int v=u+1;v<g.n;++v) if(g.adj[u]&bit(v))e.emplace_back(u,v);
 return e;
}
void domain(const Graph& g) {
 require(g.n>=4 && g.n<31,"order");
 for(int u=0;u<g.n;++u) {
  require(__builtin_popcount(g.adj[u])==3,"not cubic");
  require(!(g.adj[u]&bit(u)) && !(g.adj[u]&~all(g.n)),"invalid adjacency");
  for(int v=0;v<g.n;++v) require(bool(g.adj[u]&bit(v))==bool(g.adj[v]&bit(u)),"asymmetry");
 }
 auto connected=[&](Mask del) {
  ++deletion_tests[g.n];Mask rem=all(g.n)&~del, seen=bit(first(rem)), todo=seen;
  while(todo) { int u=first(todo);todo&=todo-1;Mask add=g.adj[u]&rem&~seen;seen|=add;todo|=add; }
  return seen==rem;
 };
 require(connected(0),"disconnected");
 for(int u=0;u<g.n;++u) {
  require(connected(bit(u)),"cut vertex");
  for(int v=u+1;v<g.n;++v)require(connected(bit(u)|bit(v)),"two-cut");
 }
}
Graph expand(const Graph& g,std::pair<int,int> e,std::pair<int,int> f) {
 require(e!=f,"same edge twice"); Graph h=g;int x=g.n,y=x+1;h.n+=2;
 erase(h,e.first,e.second);erase(h,f.first,f.second);
 edge(h,e.first,x);edge(h,e.second,x);edge(h,f.first,y);edge(h,f.second,y);edge(h,x,y);
 return h;
}
std::string factor(const Graph& g,const std::array<int,32>& mate) {
 Mask covered=0;std::vector<int> lens;
 for(int root=0;root<g.n;++root) if(!(covered&bit(root))) {
  int u=root,prev=-1,len=0;
  do {
   require(!(covered&bit(u)),"cycle collision");covered|=bit(u);++len;
   Mask nb=g.adj[u]&~bit(mate[u]); if(prev>=0)nb&=~bit(prev);
   require(nb!=0,"broken complementary cycle");int next=first(nb);prev=u;u=next;
  } while(u!=root);
  require(len>=3,"short cycle");lens.push_back(len);
 }
 for(int len:lens)if(len%3)return "";
 std::sort(lens.begin(),lens.end());std::string s;
 for(int len:lens) {if(!s.empty())s+=",";s+=std::to_string(len);}
 return s;
}
std::string search(const Graph& g,Mask rem,std::array<int,32>& mate) {
 ++matching_nodes[g.n];
 if(!rem) {++matching_leaves[g.n];return factor(g,mate);}
 int u=first(rem);Mask options=g.adj[u]&rem;
 while(options) {
  int v=first(options);options&=options-1;mate[u]=v;mate[v]=u;
  std::string found=search(g,rem^bit(u)^bit(v),mate);if(!found.empty())return found;
 }
 return "";
}
void visit(const Graph& g) {
 if((traces[12]&4095)==0)require(std::chrono::duration<double>(std::chrono::steady_clock::now()-started).count()<35,"wall deadline");
 domain(g);++traces[g.n];
 if(g.n%3==0) {
  std::array<int,32> mate{};std::string s=search(g,all(g.n),mate);
  if(s.empty()) { std::cerr<<"uncovered trace n="<<g.n<<" edges:";for(auto e:edges(g))std::cerr<<" "<<e.first<<","<<e.second;std::cerr<<"\n";throw std::runtime_error("route obstruction within tested domain"); }
  ++spectra[std::to_string(g.n)+":"+s];
 }
 if(g.n==12)return;
 auto es=edges(g);
 for(std::size_t i=0;i<es.size();++i)for(std::size_t j=i+1;j<es.size();++j)visit(expand(g,es[i],es[j]));
}
Graph obstruction18() {
 Graph p;p.n=10;
 for(int i=0;i<5;++i) {edge(p,i,(i+1)%5);edge(p,i,i+5);edge(p,i+5,5+(i+2)%5);}
 Graph h;h.n=18;
 for(auto e:edges(p))if(e.first && e.second)edge(h,e.first-1,e.second-1);
 for(int i=0;i<10;++i) {int j=(i+1)%10;if(i&&j)edge(h,i+8,j+8);}
 for(int i=0;i<5;++i)if(i)edge(h,i+8,i+13);
 edge(h,0,9);edge(h,3,17);edge(h,4,13);
 return h;
}
int main() {
 try {
  Graph k;k.n=4;for(int i=0;i<4;++i)for(int j=i+1;j<4;++j)edge(k,i,j);
  domain(k);traces[4]=1;
  // S4 has exactly two orbits of unordered pairs of distinct K4 edges.
  visit(expand(k,{0,1},{0,2}));visit(expand(k,{0,1},{2,3}));
  require(traces[6]==2 && traces[8]==72 && traces[10]==4752 && traces[12]==498960,"trace count mismatch");
  Graph h=obstruction18();domain(h);std::array<int,32> mate{};
  require(search(h,all(h.n),mate).empty(),"negative control unexpectedly positive");
  require(matching_leaves[18]==26,"negative-control matching count");
  std::cout<<"{\n  \"verdict\":\"candidate_only\",\n  \"enumeration\":\"all BG(c) construction traces after two K4 edge-pair orbits; no deduplication\",\n  \"orders\":[\n";
  for(int n=4;n<=12;n+=2)std::cout<<"    {\"n\":"<<n<<",\"traces\":"<<traces[n]<<",\"vertex_deletion_tests\":"<<deletion_tests[n]<<",\"matching_search_nodes\":"<<matching_nodes[n]<<",\"matching_leaves_until_first_witness\":"<<matching_leaves[n]<<"}"<<(n==12?"\n":",\n");
  std::cout<<"  ],\n  \"selected_witness_spectra\":[\n";bool comma=false;
  for(auto kv:spectra) {if(comma)std::cout<<",\n";comma=true;std::cout<<"    {\"order_and_lengths\":\""<<kv.first<<"\",\"trace_count\":"<<kv.second<<"}";}
  std::cout<<"\n  ],\n  \"negative_control\":{\"n\":18,\"perfect_matchings_exhausted\":26,\"divisible_factor_found\":false},\n  \"limitations\":[\"candidate-side computation, not a verifier receipt\",\"counts are construction traces, not isomorphism classes\",\"coverage requires the separately cited construction theorem\"]\n}\n";
  return 0;
 } catch(const std::exception& e) {std::cerr<<e.what()<<"\n";return 1;}
}
