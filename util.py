class IdMap:
    """
    Ingat kembali di kuliah, bahwa secara praktis, sebuah dokumen dan
    sebuah term akan direpresentasikan sebagai sebuah integer. Oleh
    karena itu, kita perlu maintain mapping antara string term (atau
    dokumen) ke integer yang bersesuaian, dan sebaliknya. Kelas IdMap ini
    akan melakukan hal tersebut.
    """

    def __init__(self):
        """
        Mapping dari string (term atau nama dokumen) ke id disimpan dalam
        python's dictionary; cukup efisien. Mapping sebaliknya disimpan dalam
        python's list.

        contoh:
            str_to_id["halo"] ---> 8
            str_to_id["/collection/dir0/gamma.txt"] ---> 54

            id_to_str[8] ---> "halo"
            id_to_str[54] ---> "/collection/dir0/gamma.txt"
        """
        self.str_to_id = {}
        self.id_to_str = []

    def __len__(self):
        """Mengembalikan banyaknya term (atau dokumen) yang disimpan di IdMap."""
        return len(self.id_to_str)

    def __get_str(self, i):
        """Mengembalikan string yang terasosiasi dengan index i."""
        return self.id_to_str[i]

    def __get_id(self, s):
        """
        Mengembalikan integer id i yang berkorespondensi dengan sebuah string s.
        Jika s tidak ada pada IdMap, lalu assign sebuah integer id baru dan kembalikan
        integer id baru tersebut.
        """
        if s not in self.str_to_id:
            self.id_to_str.append(s)
            self.str_to_id[s] = len(self.id_to_str) - 1
        return self.str_to_id[s]

    def __getitem__(self, key):
        """
        __getitem__(...) adalah special method di Python, yang mengizinkan sebuah
        collection class (seperti IdMap ini) mempunyai mekanisme akses atau
        modifikasi elemen dengan syntax [..] seperti pada list dan dictionary di Python.

        Silakan search informasi ini di Web search engine favorit Anda. Saya mendapatkan
        link berikut:

        https://stackoverflow.com/questions/43627405/understanding-getitem-method

        Jika key adalah integer, gunakan __get_str;
        jika key adalah string, gunakan __get_id
        """
        if type(key) is int:
            return self.__get_str(key)
        elif type(key) is str:
            return self.__get_id(key)
        else:
            raise TypeError

class PatriciaNode:
    def __init__(self):
        # Menyimpan struktur mapping: character_pertama -> (sisa_prefix_edge, child_node)
        # Hal ini menjamin O(1) saat mencari node anak, sambil memelihara efisiensi Radix Tree.
        self.children = {}
        self.term_id = None

class PatriciaTreeIdMap:
    """
    Alternatif struktur data untuk IdMap yang menggunakan Patricia Tree (Radix Tree) 
    untuk mengefisienkan penyimpanan dictionary terms di memori melalui prefix compression.
    """
    def __init__(self):
        self.root = PatriciaNode()
        self.id_to_str = [] 

    def __len__(self):
        """Mengembalikan banyaknya term yang disimpan di Patricia Tree."""
        return len(self.id_to_str)

    def __get_str(self, i):
        """Mengembalikan string yang terasosiasi dengan index i."""
        return self.id_to_str[i]

    def _add_term(self, s):
        """Helper untuk menambahkan term ke dictionary array dan mengembalikan index barunya."""
        self.id_to_str.append(s)
        return len(self.id_to_str) - 1

    def __get_id(self, s):
        """
        Mengembalikan integer id berkorespondensi dengan string s.
        Jika s belum ada pada Patricia Tree, jalankan logika INSERT untuk membuat
        node/edge baru sesuai kaidah Patricia Tree, berikan id baru, dan kembalikan id tersebut.
        """
        if not s:
            if self.root.term_id is None:
                self.root.term_id = self._add_term(s)
            return self.root.term_id
            
        original_s = s
        curr = self.root
        
        while s:
            if s[0] not in curr.children:
                new_node = PatriciaNode()
                new_node.term_id = self._add_term(original_s)
                curr.children[s[0]] = (s, new_node)
                return new_node.term_id
            
            edge_str, child_node = curr.children[s[0]]
            
            # Longest Common Prefix
            match_len = 0
            min_len = min(len(s), len(edge_str))
            while match_len < min_len and s[match_len] == edge_str[match_len]:
                match_len += 1
                
            if match_len == len(edge_str):
                s = s[match_len:]
                if not s:
                    if child_node.term_id is None:
                        child_node.term_id = self._add_term(original_s)
                    return child_node.term_id
                curr = child_node
            else:
                
                split_node = PatriciaNode()
                
                rem_edge = edge_str[match_len:]
                split_node.children[rem_edge[0]] = (rem_edge, child_node)
                
                curr.children[s[0]] = (edge_str[:match_len], split_node)
                
                s = s[match_len:]
                if not s:
                    split_node.term_id = self._add_term(original_s)
                    return split_node.term_id
                else:
                    new_node = PatriciaNode()
                    new_node.term_id = self._add_term(original_s)
                    split_node.children[s[0]] = (s, new_node)
                    return new_node.term_id

    def __getitem__(self, key):
        """Akses data menggunakan bracket operator [...]"""
        if type(key) is int:
            return self.__get_str(key)
        elif type(key) is str:
            return self.__get_id(key)
        else:
            raise TypeError

    def __contains__(self, key):
        """Metode opsional/penting untuk mengecek eksistensi term (bisa dipakai untuk query)."""
        if not key:
            return self.root.term_id is not None
            
        curr = self.root
        s = key
        while s:
            if s[0] not in curr.children:
                return False
                
            edge_str, child_node = curr.children[s[0]]
            
            if s.startswith(edge_str):
                s = s[len(edge_str):]
                curr = child_node
            else:
                return False
                
        return curr.term_id is not None

def sorted_merge_posts_and_tfs(posts_tfs1, posts_tfs2):
    """
    Menggabung (merge) dua lists of tuples (doc id, tf) dan mengembalikan
    hasil penggabungan keduanya (TF perlu diakumulasikan untuk semua tuple
    dengn doc id yang sama), dengan aturan berikut:

    contoh: posts_tfs1 = [(1, 34), (3, 2), (4, 23)]
            posts_tfs2 = [(1, 11), (2, 4), (4, 3 ), (6, 13)]

            return   [(1, 34+11), (2, 4), (3, 2), (4, 23+3), (6, 13)]
                   = [(1, 45), (2, 4), (3, 2), (4, 26), (6, 13)]

    Parameters
    ----------
    list1: List[(Comparable, int)]
    list2: List[(Comparable, int]
        Dua buah sorted list of tuples yang akan di-merge.

    Returns
    -------
    List[(Comparablem, int)]
        Penggabungan yang sudah terurut
    """
    i, j = 0, 0
    merge = []
    while (i < len(posts_tfs1)) and (j < len(posts_tfs2)):
        if posts_tfs1[i][0] == posts_tfs2[j][0]:
            freq = posts_tfs1[i][1] + posts_tfs2[j][1]
            merge.append((posts_tfs1[i][0], freq))
            i += 1
            j += 1
        elif posts_tfs1[i][0] < posts_tfs2[j][0]:
            merge.append(posts_tfs1[i])
            i += 1
        else:
            merge.append(posts_tfs2[j])
            j += 1
    while i < len(posts_tfs1):
        merge.append(posts_tfs1[i])
        i += 1
    while j < len(posts_tfs2):
        merge.append(posts_tfs2[j])
        j += 1
    return merge

def test(output, expected):
    """ simple function for testing """
    return "PASSED" if output == expected else "FAILED"

if __name__ == '__main__':

    doc = ["halo", "semua", "selamat", "pagi", "semua"]
    term_id_map = IdMap()
    assert [term_id_map[term] for term in doc] == [0, 1, 2, 3, 1], "term_id salah"
    assert term_id_map[1] == "semua", "term_id salah"
    assert term_id_map[0] == "halo", "term_id salah"
    assert term_id_map["selamat"] == 2, "term_id salah"
    assert term_id_map["pagi"] == 3, "term_id salah"

    docs = ["/collection/0/data0.txt",
            "/collection/0/data10.txt",
            "/collection/1/data53.txt"]
    doc_id_map = IdMap()
    assert [doc_id_map[docname] for docname in docs] == [0, 1, 2], "docs_id salah"

    assert sorted_merge_posts_and_tfs([(1, 34), (3, 2), (4, 23)], \
                                      [(1, 11), (2, 4), (4, 3 ), (6, 13)]) == [(1, 45), (2, 4), (3, 2), (4, 26), (6, 13)], "sorted_merge_posts_and_tfs salah"
