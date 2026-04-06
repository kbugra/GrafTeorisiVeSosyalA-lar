import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class GrafUygulamasi:
    """
    Bu sınıf Graf Teorisi ve Sosyal Ağlar dersinizin 1., 2., 4., 6. ve 7. 
    haftalarında işlediğiniz konuları uygulamalı olarak bir araya getirir.
    """
    def __init__(self, matris=None, num_nodes=None, directed=True):
        self.directed = directed
        if matris is not None:
            self.matrix = np.array(matris)
            self.num_nodes = self.matrix.shape[0]
            self.adj_list = self._matrix_to_adj_list()
        else:
            self.num_nodes = num_nodes if num_nodes else 0
            self.matrix = np.zeros((self.num_nodes, self.num_nodes), dtype=int)
            self.adj_list = {i: [] for i in range(self.num_nodes)}
            
    def _matrix_to_adj_list(self):
        adj_list = {i: [] for i in range(self.num_nodes)}
        for i in range(self.num_nodes):
            for j in range(self.num_nodes):
                if self.matrix[i][j] != 0:
                    adj_list[i].append(j)
        return adj_list

    def add_edge(self, u, v, weight=1):
        if v not in self.adj_list[u]:
            self.adj_list[u].append(v)
            self.matrix[u][v] = weight
            if not self.directed:
                self.adj_list[v].append(u)
                self.matrix[v][u] = weight

    # -------------------------------------------------------------
    # HAFTA 1 & 2: Temel Kavramlar, Matris ve Liste Gösterimleri, Dereceler
    # -------------------------------------------------------------
    def get_degrees(self):
        """In-degree ve Out-degree değerlerini hesaplar"""
        in_degree = np.sum(self.matrix, axis=0)
        out_degree = np.sum(self.matrix, axis=1)
        return in_degree, out_degree
    
    def print_representation(self):
        print("--- GRAF GÖSTERİMLERİ ---")
        print("Komşuluk Matrisi (Adjacency Matrix):")
        print(self.matrix)
        print("\nBağlı Listeler (Adjacency List):")
        for node, edges in self.adj_list.items():
            print(f"{node} -> {edges}")

    # -------------------------------------------------------------
    # HAFTA 4: DFS Çıkarımları, Keşif/Bitiş Zamanı ve Transpoz Graf
    # -------------------------------------------------------------
    def dfs(self, start_node=0):
        print("\n--- DFS (Depth First Search) İŞLEMİ ---")
        visited = [False] * self.num_nodes
        discovery_time = [0] * self.num_nodes
        finish_time = [0] * self.num_nodes
        self.time_counter = 0

        def dfs_recursive(node):
            if not visited[node]:
                self.time_counter += 1
                discovery_time[node] = self.time_counter
                visited[node] = True
                print(f"Ziyaret Edilen Düğüm: {node} (Keşif Zamanı: {discovery_time[node]})")
                for neigh in self.adj_list[node]:
                    dfs_recursive(neigh)
                self.time_counter += 1
                finish_time[node] = self.time_counter

        # Ayrı bileşenler (disconnected components) için tüm düğümleri dolaşalım
        for i in range(self.num_nodes):
             if not visited[i]:
                  dfs_recursive(i)
        
        print("\nDFS Zaman Çizelgesi:")
        for i in range(self.num_nodes):
            print(f"Düğüm {i} | Keşif (disc): {discovery_time[i]} | Bitiş (finish): {finish_time[i]}")
            
    def get_transpose(self):
        """Yönlü grafta kenarların yönünü tersine çevirerek Transpoz grafını döndürür."""
        g_t = GrafUygulamasi(num_nodes=self.num_nodes, directed=self.directed)
        g_t.matrix = self.matrix.T
        g_t.adj_list = g_t._matrix_to_adj_list()
        return g_t

    # -------------------------------------------------------------
    # HAFTA 6: DFS ile Bridge (Köprü) Bulma
    # -------------------------------------------------------------
    def find_bridges(self):
        """
        disc[u] ve low[u] değerlerini tutarak köprü olan kenarları bulur.
        low[v] > disc[u] ise (u, v) bir köprüdür.
        """
        visited = [False] * self.num_nodes
        disc = [float("inf")] * self.num_nodes
        low = [float("inf")] * self.num_nodes
        parent = [-1] * self.num_nodes
        time_counter = [0] # Referans olarak geçmek için liste içinde kullanıyoruz
        bridges = []

        def bridge_dfs(u):
            visited[u] = True
            disc[u] = time_counter[0]
            low[u] = time_counter[0]
            time_counter[0] += 1

            for v in self.adj_list[u]:
                if not visited[v]:
                    parent[v] = u
                    bridge_dfs(v)
                    # Alt ağaçtan dönülen minimum discovery zamanı güncellenir
                    low[u] = min(low[u], low[v])

                    # Köprü tespiti koşulu (Slayt Hafta 6 - low[v] > disc[u])
                    if low[v] > disc[u]:
                        bridges.append((u, v))
                # Back edge kontrolü
                elif v != parent[u]:
                    low[u] = min(low[u], disc[v])
                    
        for i in range(self.num_nodes):
            if not visited[i]:
                bridge_dfs(i)
                
        return bridges

    # -------------------------------------------------------------
    # HAFTA 7: Merkeziyet Ölçütleri (Centrality) ve Floyd Algorithm
    # -------------------------------------------------------------
    def floyd_warshall(self):
        """Aracılık merkeziyeti için temel teşkil eden en kısa yollar matrisini bulur."""
        # 0 bağlantıları sonsuz mesafe kabul ediyoruz
        dist = np.where(self.matrix == 0, float('inf'), self.matrix)
        np.fill_diagonal(dist, 0)
        V = self.num_nodes
        
        for k in range(V):
            for i in range(V):
                for j in range(V):
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
        return dist

    def calculate_centralities(self):
        """NetworkX kütüphanesini kullanarak slaytlardaki merkeziyet metriklerini hesaplar"""
        print("\n--- MERKEZİYET (CENTRALITY) TESPİTİ ---")
        nx_graph = nx.DiGraph(self.matrix) if self.directed else nx.Graph(self.matrix)
        
        deg_centrality = nx.degree_centrality(nx_graph)
        print("Derece Merkeziyeti (Degree):", [round(v, 3) for v in deg_centrality.values()])
        
        closeness_cent = nx.closeness_centrality(nx_graph)
        print("Yakınlık Merkeziyeti (Closeness):", [round(v, 3) for v in closeness_cent.values()])
        
        betweenness_cent = nx.betweenness_centrality(nx_graph)
        print("Aracılık Merkeziyeti (Betweenness):", [round(v, 3) for v in betweenness_cent.values()])
        
        try:
            eigen_cent = nx.eigenvector_centrality(nx_graph, max_iter=1000)
            print("Eigenvector Merkeziyeti:", [round(v, 3) for v in eigen_cent.values()])
        except Exception as e:
            print("Eigenvector Merkeziyeti hesaplanamadı (Graf yapısı yakınsamadı sınırına ulaştı).")
            
        try:
            pagerank = nx.pagerank(nx_graph)
            print("PageRank (Katmanlı Merkeziyet):", [round(v, 3) for v in pagerank.values()])
        except Exception as e:
            print("PageRank hesaplanamadı.")

    # -------------------------------------------------------------
    # GÖRSELLEŞTİRME
    # -------------------------------------------------------------
    def visualize(self):
        """Grafı NetworkX ile çizdirir, köprü (bridge) kenarlarını kırmızı yapar."""
        print("\nGraf görselleştirme penceresi açılıyor...")
        nx_graph = nx.DiGraph(self.matrix) if self.directed else nx.Graph(self.matrix)
        
        pos = nx.spring_layout(nx_graph, seed=42)
        plt.figure(figsize=(10, 7))
        
        # Tüm grafın çizimi
        nx.draw(nx_graph, pos, with_labels=True, node_color='skyblue', 
                node_size=800, edge_color='gray', font_size=12, font_weight='bold')
        
        # Köprülerin bulunup farklı renkle çizilmesi
        # Köprü algoritması yönlü graflarda farklı çalışabilir, genelde yönsüz graflar için işlenir.
        # Bizim bridge algoritmamız temel yapıyı işaretler.
        bridges = self.find_bridges()
        if bridges:
            print(f"Çizimde Kırmızı ile belirtilen köprüler bulundu: {bridges}")
            nx.draw_networkx_edges(nx_graph, pos, edgelist=bridges, edge_color='red', width=2.5)
            
        plt.title("Graf Analizi (Kırmızı çizgiler sistemsel 'Bridge'leri gösterir)")
        plt.show()


def main():
    print("=========================================================================")
    print("GRAF TEORİSİ VE SOSYAL AĞLAR - BÜTÜNLEŞİK DERS UYGULAMASI")
    print("=========================================================================\n")

    # Dersteki F.txt veya C.txt misali örnek bir matris ile ağı başlatalım
    # Yönsüz ve bridge içeren örnek bir yapı:
    # 0 - 1 - 2
    # |   |
    # 3 - 4 ------ 5 - 6
    
    matris = [
        [0, 1, 0, 1, 0, 0, 0], # 0
        [1, 0, 1, 0, 1, 0, 0], # 1
        [0, 1, 0, 0, 0, 0, 0], # 2
        [1, 0, 0, 0, 1, 0, 0], # 3
        [0, 1, 0, 1, 0, 1, 0], # 4
        [0, 0, 0, 0, 1, 0, 1], # 5
        [0, 0, 0, 0, 0, 1, 0], # 6
    ]

    graf_sistemi = GrafUygulamasi(matris, directed=False)
    
    # 1. ve 2. Hafta Konuları
    graf_sistemi.print_representation()
    in_deg, out_deg = graf_sistemi.get_degrees()
    print("\nIn-degree:", in_deg)
    print("Out-degree:", out_deg)

    # 4. Hafta Konuları
    graf_sistemi.dfs()
    
    print("\n--- GRAF TRANSPOZ İŞLEMİ ---")
    transpose_graf = graf_sistemi.get_transpose()
    print("Transpoz Matris:\n", transpose_graf.matrix)

    # 6. Hafta Konuları
    print("\n--- BRIDGE (KÖPRÜ) TESPİTİ ---")
    kopruler = graf_sistemi.find_bridges()
    if kopruler:
        print(f"Kaldırıldığında grafı parçalayan kritik yollar (Bridges): {kopruler}")
    else:
        print("Grafta köprü bulunamadı!")

    # 7. Hafta Konuları
    print("\n--- FLOYD-WARSHALL ALGORİTMASI ---")
    print("Tüm düğümler arası en kısa mesafeler:")
    # Sonsuz değerleri gösterimde daha güzel olması için numpy inf olarak basıyoruz.
    print(graf_sistemi.floyd_warshall())

    graf_sistemi.calculate_centralities()

    # Görselleştirme (Matplotlib - Arayüz varsa gösterir)
    graf_sistemi.visualize()


if __name__ == "__main__":
    main()
