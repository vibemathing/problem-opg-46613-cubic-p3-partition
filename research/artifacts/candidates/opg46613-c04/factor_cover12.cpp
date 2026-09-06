// Reproduction candidate; execution is not asserted by this source file.
// Build: c++ -std=c++17 -O2 -Wall -Wextra -pedantic factor_cover12.cpp -o factor_cover12
// Run under an external 35-second, 256-MiB, 2-MiB-output limit.
// A successful run emits one witness per retained union and a final DONE marker.
#include <array>
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

using Mask = std::uint32_t;
using Mate = std::array<int, 12>;
using Graph = std::array<Mask, 12>;
constexpr Mask ALL = (Mask(1) << 12) - 1;
const auto started = std::chrono::steady_clock::now();
std::uint64_t recursion_ticks = 0;
std::array<std::uint64_t, 4> unions{}, retained{};
const std::array<std::vector<int>, 4> types{{{4,8},{5,7},{3,4,5},{4,4,4}}};

void require(bool condition, const char* message) {
    if (!condition) throw std::runtime_error(message);
}
Mask bit(int v) { return Mask(1) << v; }
int first(Mask x) {
    require(x != 0, "empty bit scan");
    int v = 0;
    while (!(x & 1)) { ++v; x >>= 1; }
    return v;
}
void tick() {
    if ((++recursion_ticks & 4095) == 0) {
        const double seconds = std::chrono::duration<double>(
            std::chrono::steady_clock::now() - started).count();
        require(seconds < 30.0, "deadline: incomplete certificate");
    }
}
void add(Graph& g, int u, int v) {
    require(0 <= u && u < 12 && 0 <= v && v < 12 && u != v, "invalid edge");
    require(!(g[u] & bit(v)), "duplicate edge");
    g[u] |= bit(v); g[v] |= bit(u);
}
Graph cycles(int t) {
    Graph f{}; int start = 0;
    for (int n : types[t]) {
        for (int i = 0; i < n; ++i) add(f, start+i, start+(i+1)%n);
        start += n;
    }
    require(start == 12, "factor order");
    return f;
}
bool connected(const Graph& g, Mask deleted) {
    const Mask remaining = ALL & ~deleted;
    Mask seen = bit(first(remaining)), todo = seen;
    while (todo) {
        int u = first(todo); todo &= todo - 1;
        Mask new_vertices = g[u] & remaining & ~seen;
        seen |= new_vertices; todo |= new_vertices;
    }
    return seen == remaining;
}
bool three_connected(const Graph& g) {
    if (!connected(g, 0)) return false;
    for (int u = 0; u < 12; ++u) {
        if (!connected(g, bit(u))) return false;
        for (int v = u+1; v < 12; ++v)
            if (!connected(g, bit(u)|bit(v))) return false;
    }
    return true;
}
bool divisible_complement(const Graph& g, const Mate& m) {
    Mask seen = 0;
    for (int root = 0; root < 12; ++root) {
        if (seen & bit(root)) continue;
        int u = root, previous = -1, length = 0;
        do {
            require(!(seen & bit(u)), "complementary cycle collision");
            seen |= bit(u); ++length;
            Mask options = g[u] & ~bit(m[u]);
            if (previous >= 0) options &= ~bit(previous);
            require(options != 0, "broken complementary cycle");
            int next = first(options); previous = u; u = next;
        } while (u != root);
        require(length >= 3, "non-simple complementary cycle");
        if (length % 3) return false;
    }
    return true;
}
bool witness_search(const Graph& g, Mask remaining, Mate& m) {
    tick();
    if (!remaining) return divisible_complement(g, m);
    int u = first(remaining);
    Mask partners = g[u] & remaining;
    while (partners) {
        int v = first(partners); partners &= partners - 1;
        m[u] = v; m[v] = u;
        if (witness_search(g, remaining ^ bit(u) ^ bit(v), m)) return true;
    }
    return false;
}
std::string encode(const Mate& m) {
    const char* digits = "0123456789ab";
    std::string result;
    for (int u = 0; u < 12; ++u) {
        require(0 <= m[u] && m[u] < 12 && m[u] != u && m[m[u]] == u,
                "invalid matching encoding");
        result += digits[m[u]];
    }
    return result;
}
void emit_union(int t, const Graph& f, const Mate& input) {
    ++unions[t];
    require(unions[t] <= 10395, "input count exceeds proved bound");
    Graph g = f;
    for (int u = 0; u < 12; ++u) if (u < input[u]) add(g, u, input[u]);
    if (!three_connected(g)) return;
    ++retained[t];
    Mate witness{};
    if (!witness_search(g, ALL, witness)) {
        std::cerr << "OBSTRUCTION type=" << t << " input=" << encode(input) << '\n';
        throw std::runtime_error("retained union has no divisible-factor witness");
    }
    std::cout << t << '\t' << encode(input) << '\t' << encode(witness) << '\n';
    require(bool(std::cout), "certificate output failure");
}
void input_search(int t, const Graph& f, Mask remaining, Mate& m) {
    tick();
    if (!remaining) { emit_union(t, f, m); return; }
    int u = first(remaining);
    Mask partners = remaining & ~bit(u) & ~f[u];
    while (partners) {
        int v = first(partners); partners &= partners - 1;
        m[u] = v; m[v] = u;
        input_search(t, f, remaining ^ bit(u) ^ bit(v), m);
    }
}
int main() {
    try {
        std::cout << "# opg46613-bad-factor-cover-v1\n";
        for (int t = 0; t < 4; ++t) {
            Graph f = cycles(t); Mate m{};
            input_search(t, f, ALL, m);
        }
        std::cout << "# DONE";
        for (int t = 0; t < 4; ++t) std::cout << '\t' << unions[t] << ':' << retained[t];
        std::cout << '\n';
        std::cout.flush();
        require(bool(std::cout), "certificate flush failure");
        return 0;
    } catch (const std::exception& ex) {
        std::cerr << ex.what() << '\n';
        return 1;
    }
}
