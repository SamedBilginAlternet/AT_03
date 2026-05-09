"""
Soru 1 doğrulama: Verilen ekleme sırası ile BST'yi inşa eder ve
preorder/inorder/postorder gezintilerini ekrana yazdırır.

Bu, manuel cevabı (CEVAPLAR.md - Soru 1) koddan da doğrulamak içindir.
"""


class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


def insert(root, key):
    if root is None:
        return Node(key)
    if key < root.key:
        root.left = insert(root.left, key)
    else:
        root.right = insert(root.right, key)
    return root


def preorder(node, out):
    if node is None:
        return
    out.append(node.key)
    preorder(node.left, out)
    preorder(node.right, out)


def inorder(node, out):
    if node is None:
        return
    inorder(node.left, out)
    out.append(node.key)
    inorder(node.right, out)


def postorder(node, out):
    if node is None:
        return
    postorder(node.left, out)
    postorder(node.right, out)
    out.append(node.key)


def print_tree(node, prefix="", is_last=True, label="root"):
    if node is None:
        return
    branch = "└── " if is_last else "├── "
    print(prefix + branch + f"{label}: {node.key}")
    next_prefix = prefix + ("    " if is_last else "│   ")
    if node.left or node.right:
        children = [("L", node.left), ("R", node.right)]
        for i, (lbl, ch) in enumerate(children):
            last = (i == len(children) - 1)
            if ch is None:
                print(next_prefix + ("└── " if last else "├── ") + f"{lbl}: ·")
            else:
                print_tree(ch, next_prefix, last, lbl)


def main():
    sequence = ["n", "z", "d", "f", "a", "k", "o", "m", "e", "l", "t", "g"]

    print("Ekleme sırası:", ", ".join(sequence))
    print()

    root = None
    for k in sequence:
        root = insert(root, k)

    print("BST yapısı:")
    print_tree(root)
    print()

    pre, ino, post = [], [], []
    preorder(root, pre)
    inorder(root, ino)
    postorder(root, post)

    print("Preorder  :", ", ".join(pre))
    print("Inorder   :", ", ".join(ino))
    print("Postorder :", ", ".join(post))

    # Cevapla karşılaştır
    expected = {
        "preorder": ["n", "d", "a", "f", "e", "k", "g", "m", "l", "z", "o", "t"],
        "inorder": ["a", "d", "e", "f", "g", "k", "l", "m", "n", "o", "t", "z"],
        "postorder": ["a", "e", "g", "l", "m", "k", "f", "d", "t", "o", "z", "n"],
    }
    print()
    print("Doğrulama:")
    print("  preorder  :", "OK" if pre == expected["preorder"] else "FARK!")
    print("  inorder   :", "OK" if ino == expected["inorder"] else "FARK!")
    print("  postorder :", "OK" if post == expected["postorder"] else "FARK!")


if __name__ == "__main__":
    main()
