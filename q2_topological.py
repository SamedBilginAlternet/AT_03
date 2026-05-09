"""
Soru 2 doğrulama: DFS tabanlı topological sort.

Algoritma (CLRS):
  - WHITE/GRAY/BLACK renklendirmesiyle DFS yapılır.
  - GRAY bir düğüme tekrar gidilirse back-edge bulunmuştur → graf
    döngülüdür → topological sort yoktur.
  - Aksi halde her düğüm "finish" olduğunda yığına eklenir; topolojik
    sıralama bu yığının tersidir.

Bu, CEVAPLAR.md - Soru 2'deki manuel cevabın doğruluğunu kontrol eder.
"""

WHITE, GRAY, BLACK = 0, 1, 2


def topological_sort(nodes, edges):
    """
    DFS tabanlı topological sort.
    nodes: sıralı düğüm listesi (alfabetik gezinti için)
    edges: {u: [v1, v2, ...]} (alfabetik komşu sırası ile)
    return: (order_list, has_cycle, cycle_edge)
    """
    color = {u: WHITE for u in nodes}
    finish_stack = []
    has_cycle = False
    cycle_edge = None

    def dfs(u):
        nonlocal has_cycle, cycle_edge
        color[u] = GRAY
        for v in edges.get(u, []):
            if color[v] == GRAY:
                has_cycle = True
                cycle_edge = (u, v)
                return
            if color[v] == WHITE:
                dfs(v)
                if has_cycle:
                    return
        color[u] = BLACK
        finish_stack.append(u)

    for u in nodes:
        if color[u] == WHITE:
            dfs(u)
            if has_cycle:
                return [], True, cycle_edge

    return list(reversed(finish_stack)), False, None


def verify_order(order, edges):
    """Topolojik sıralamada her (u→v) için u, v'den önce gelmeli."""
    pos = {u: i for i, u in enumerate(order)}
    for u, vs in edges.items():
        for v in vs:
            if pos[u] >= pos[v]:
                return False, (u, v)
    return True, None


def run_case(name, nodes, edges):
    print(f"=== {name} ===")
    print("Kenarlar:", ", ".join(f"{u}->{v}" for u, vs in edges.items() for v in vs))

    order, cyc, back = topological_sort(nodes, edges)

    if cyc:
        print(f"DÖNGÜ TESPİT EDİLDİ — back-edge: {back[0]} → {back[1]}")
        print("Topolojik sıralama yok.")
    else:
        print("Topolojik sıralama:", " → ".join(order))
        ok, bad = verify_order(order, edges)
        print("Doğrulama:", "OK" if ok else f"FARK! ({bad})")
    print()


def main():
    # Graf (a) — CEVAPLAR.md'deki kenar yorumuna göre
    nodes_a = ["a", "b", "c", "d", "e", "f", "g"]
    edges_a = {
        "a": ["b", "f"],
        "b": ["e"],
        "c": [],
        "d": ["a", "b", "c", "f", "g"],
        "e": ["g"],
        "f": [],
        "g": ["f"],
    }
    run_case("Graf (a)", nodes_a, edges_a)

    # Graf (b)
    nodes_b = ["a", "b", "c", "d", "e", "f", "g"]
    edges_b = {
        "a": ["b", "e"],
        "b": ["c", "f"],
        "c": ["d", "f"],
        "d": ["g"],
        "e": ["f"],
        "f": ["g"],
        "g": [],
    }
    run_case("Graf (b)", nodes_b, edges_b)

    # Bonus: döngü içeren bir varyant — algoritmanın cycle bulduğunu gösterir
    print("=== Döngü örneği (bonus) ===")
    nodes_c = ["a", "b", "c"]
    edges_c = {"a": ["b"], "b": ["c"], "c": ["a"]}
    run_case("a→b→c→a", nodes_c, edges_c)


if __name__ == "__main__":
    main()
