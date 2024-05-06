class TrieNode:
    def __init__(self):
        self.children = {}
        self.end_of_word = False
        self.document_ids = set()

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word, doc_id):
        current = self.root
        for char in word:
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]
        current.end_of_word = True
        current.document_ids.add(doc_id)
    
    def search(self, prefix):
        current = self.root
        for char in prefix:
            if char not in current.children:
                return []
            current = current.children[char]
        
        # At the end of the prefix, collect all document IDs recursively
        return self.collect_documents(current)
    
    def collect_documents(self, node):
        # A recursive function to collect all document IDs in the subtree
        documents = set(node.document_ids)
        for child in node.children.values():
            documents.update(self.collect_documents(child))
        return list(documents)
