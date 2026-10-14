# Trie（前缀树）：按字符逐层存储字符串，前缀查询只和前缀长度有关
class Trie:
    def __init__(self): self.root = {}
    END = "$"
    def insert(self, word, freq=1):
        node = self.root
        for ch in word: node = node.setdefault(ch, {})
        node[self.END] = node.get(self.END, 0) + freq
    def _walk(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node: return None
            node = node[ch]
        return node
    def contains(self, w): n = self._walk(w); return bool(n and self.END in n)
    def complete(self, prefix, k=3):
        node, out = self._walk(prefix), []
        def dfs(n, path):
            for ch, child in n.items():
                if ch == self.END: out.append((child, prefix + path))
                else: dfs(child, path + ch)
        if node: dfs(node, "")
        return [w for _, w in sorted(out, reverse=True)[:k]]

t = Trie()
for w, f in [("tensor", 50), ("tensorflow", 30), ("tensorboard", 10), ("token", 80), ("tokenizer", 60), ("torch", 90)]:
    t.insert(w, f)
print("包含 token:", t.contains("token"), "| 包含 tok:", t.contains("tok"))
print("自动补全 'to':", t.complete("to"))
print("自动补全 'tensor':", t.complete("tensor"))

def count_nodes(n): return sum(1 + count_nodes(c) for k, c in n.items() if k != Trie.END)
words = ["tensor", "tensorflow", "tensorboard", "token", "tokenizer", "torch"]
print(f"共享前缀：6 个词共 {sum(map(len, words))} 个字符，Trie 只用了 {count_nodes(t.root)} 个节点")

# 分词器里的最长前缀匹配（类似 WordPiece/BPE 词表查找的思路）
vocab = Trie()
for piece in ["un", "unhappi", "happi", "ness", "u", "n", "h", "a", "p", "i", "e", "s"]: vocab.insert(piece)
def greedy_tokenize(word):
    out, i = [], 0
    while i < len(word):
        node, best = vocab.root, None
        for j in range(i, len(word)):
            node = node.get(word[j])
            if node is None: break
            if Trie.END in node: best = j + 1
        if best is None: out.append("[UNK]"); i += 1
        else: out.append(word[i:best]); i = best
    return out
print("最长前缀匹配分词 unhappiness ->", greedy_tokenize("unhappiness"))
