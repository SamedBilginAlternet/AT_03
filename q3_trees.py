"""
Algoritma Analizi ve Tasarımı - Ödev 3 / Soru 3
Binary Search Tree, AVL ve 2-3 Ağacı karşılaştırması
"""

import random


# ============================================================
# Binary Search Tree (BST)
# ============================================================
class BSTNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None
        self.comparisons = 0
        self.swaps = 0  # BST'de döndürme/swap yok

    def insert(self, key):
        if self.root is None:
            self.root = BSTNode(key)
            return
        cur = self.root
        while True:
            self.comparisons += 1
            if key < cur.key:
                if cur.left is None:
                    cur.left = BSTNode(key)
                    return
                cur = cur.left
            else:
                if cur.right is None:
                    cur.right = BSTNode(key)
                    return
                cur = cur.right


# ============================================================
# AVL Tree
# ============================================================
class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


class AVL:
    def __init__(self):
        self.root = None
        self.comparisons = 0
        self.swaps = 0  # rotation sayısı

    def _h(self, n):
        return n.height if n else 0

    def _update_height(self, n):
        n.height = 1 + max(self._h(n.left), self._h(n.right))

    def _bf(self, n):
        return self._h(n.left) - self._h(n.right)

    def _rotate_right(self, y):
        self.swaps += 1
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        self._update_height(y)
        self._update_height(x)
        return x

    def _rotate_left(self, x):
        self.swaps += 1
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        self._update_height(x)
        self._update_height(y)
        return y

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if node is None:
            return AVLNode(key)
        self.comparisons += 1
        if key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)

        self._update_height(node)
        bf = self._bf(node)

        # Sol-Sol
        if bf > 1 and key < node.left.key:
            return self._rotate_right(node)
        # Sağ-Sağ
        if bf < -1 and key >= node.right.key:
            return self._rotate_left(node)
        # Sol-Sağ
        if bf > 1 and key >= node.left.key:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        # Sağ-Sol
        if bf < -1 and key < node.right.key:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node


# ============================================================
# 2-3 Tree
# ============================================================
class Node23:
    def __init__(self, keys=None, children=None):
        self.keys = keys if keys is not None else []
        self.children = children if children is not None else []

    def is_leaf(self):
        return len(self.children) == 0


class Tree23:
    def __init__(self):
        self.root = None
        self.comparisons = 0
        self.swaps = 0  # split sayısı

    def insert(self, key):
        if self.root is None:
            self.root = Node23(keys=[key])
            return
        result = self._insert(self.root, key)
        if result is not None:
            promoted, left, right = result
            self.root = Node23(keys=[promoted], children=[left, right])

    def _insert(self, node, key):
        if node.is_leaf():
            for _ in node.keys:
                self.comparisons += 1
            new_keys = sorted(node.keys + [key])
            if len(new_keys) <= 2:
                node.keys = new_keys
                return None
            # split (3 anahtar oluştu)
            self.swaps += 1
            left = Node23(keys=[new_keys[0]])
            right = Node23(keys=[new_keys[2]])
            return (new_keys[1], left, right)

        # iç düğüm: hangi çocuğa ineceğimizi bul
        self.comparisons += 1
        if key < node.keys[0]:
            child_idx = 0
        elif len(node.keys) == 1:
            child_idx = 1
        else:
            self.comparisons += 1
            child_idx = 1 if key < node.keys[1] else 2

        result = self._insert(node.children[child_idx], key)
        if result is None:
            return None

        promoted, left, right = result
        new_keys = node.keys[:]
        new_children = node.children[:]
        new_keys.insert(child_idx, promoted)
        new_children[child_idx] = left
        new_children.insert(child_idx + 1, right)

        if len(new_keys) <= 2:
            node.keys = new_keys
            node.children = new_children
            return None

        # düğümü split et
        self.swaps += 1
        left_child = Node23(keys=[new_keys[0]], children=new_children[:2])
        right_child = Node23(keys=[new_keys[2]], children=new_children[2:])
        return (new_keys[1], left_child, right_child)


# ============================================================
# Ağaç yazdırma fonksiyonları (node-child gösterimi)
# ============================================================
def print_bst(node, prefix="", is_last=True, label="root"):
    if node is None:
        return
    branch = "└── " if is_last else "├── "
    print(prefix + branch + f"{label}: {node.key}")
    next_prefix = prefix + ("    " if is_last else "│   ")
    children = []
    if node.left or node.right:
        children.append(("L", node.left))
        children.append(("R", node.right))
    for i, (lbl, ch) in enumerate(children):
        last = (i == len(children) - 1)
        if ch is None:
            print(next_prefix + ("└── " if last else "├── ") + f"{lbl}: ·")
        else:
            print_bst(ch, next_prefix, last, lbl)


def print_avl(node, prefix="", is_last=True, label="root"):
    if node is None:
        return
    branch = "└── " if is_last else "├── "
    print(prefix + branch + f"{label}: {node.key} (h={node.height})")
    next_prefix = prefix + ("    " if is_last else "│   ")
    children = []
    if node.left or node.right:
        children.append(("L", node.left))
        children.append(("R", node.right))
    for i, (lbl, ch) in enumerate(children):
        last = (i == len(children) - 1)
        if ch is None:
            print(next_prefix + ("└── " if last else "├── ") + f"{lbl}: ·")
        else:
            print_avl(ch, next_prefix, last, lbl)


def print_23(node, prefix="", is_last=True, label="root"):
    if node is None:
        return
    branch = "└── " if is_last else "├── "
    print(prefix + branch + f"{label}: {node.keys}")
    next_prefix = prefix + ("    " if is_last else "│   ")
    for i, ch in enumerate(node.children):
        last = (i == len(node.children) - 1)
        print_23(ch, next_prefix, last, f"C{i}")


# ============================================================
# Ana program
# ============================================================
def main():
    # Veri seti 1 defa üret
    data = [random.randint(0, 1000) for _ in range(20)]

    print("=" * 70)
    print("VERİ SETİ (0-1000 arası 20 rastgele sayı, bir defa üretildi)")
    print("=" * 70)
    print(data)
    print()

    bst, avl, t23 = BST(), AVL(), Tree23()
    for x in data:
        bst.insert(x)
        avl.insert(x)
        t23.insert(x)

    print("=" * 70)
    print("BINARY SEARCH TREE")
    print("=" * 70)
    print_bst(bst.root)
    print(f"\n→ Karşılaştırma: {bst.comparisons}, Swap: {bst.swaps}")
    print()

    print("=" * 70)
    print("AVL TREE")
    print("=" * 70)
    print_avl(avl.root)
    print(f"\n→ Karşılaştırma: {avl.comparisons}, Rotation (swap): {avl.swaps}")
    print()

    print("=" * 70)
    print("2-3 TREE")
    print("=" * 70)
    print_23(t23.root)
    print(f"\n→ Karşılaştırma: {t23.comparisons}, Split (swap): {t23.swaps}")
    print()

    print("=" * 70)
    print("KARŞILAŞTIRMA TABLOSU")
    print("=" * 70)
    header = f"| {'Algoritma':<20} | {'Karşılaştırma':>14} | {'Swap':>6} |"
    sep = "|" + "-" * 22 + "|" + "-" * 16 + "|" + "-" * 8 + "|"
    print(sep)
    print(header)
    print(sep)
    print(f"| {'Binary Search Tree':<20} | {bst.comparisons:>14} | {bst.swaps:>6} |")
    print(f"| {'AVL Tree':<20} | {avl.comparisons:>14} | {avl.swaps:>6} |")
    print(f"| {'2-3 Tree':<20} | {t23.comparisons:>14} | {t23.swaps:>6} |")
    print(sep)


if __name__ == "__main__":
    main()
