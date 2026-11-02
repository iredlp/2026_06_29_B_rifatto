import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()  # grafo semplice
        self._idMapA = {}

    def creaGrafo(self):
        self._grafo.clear()
        self._idMapA.clear()

        album = DAO.getAllNodes()
        for a in  album:
            self._idMapA[a.AlbumId] = a
            self._grafo.add_node(a)
            # aggiungo i nodi
        print("2 - Nodi aggiunti")


        for a in album:
            a.list_brani.clear()
            a.list_generi.clear()
            # a.clientiPerArtista = set(DAO.getClientiPerArtista(a.ArtistId))
            a.list_brani = DAO.getBraniPerAlbum(a.AlbumId)
            a.list_generi=DAO.getGeneriPerAlbum(a.AlbumId)
           # print(a.ArtistId, a.list_playlist)
          #  a.popolarita = DAO.getPopolarita(a.ArtistId, genere)
        print("3 - Informazioni recuperate")


        for i in range(len(album)):
            a1 = album[i]

            for j in range(i + 1, len(album)):
                a2 = album[j]

                # for p in
                playlistComuni = (set(a1.list_generi) & set(a2.list_generi))
                #  peso = 0
                # ND: & FUNZIONA SOLO CON I SET! SE HAI LE LISTE CONSERVTILE IN SET E POI CONFRONTALE
                #  for film in  clientiComuni:
                #     incasso=DAO.getIncassiPerFilm(film)
                #    peso+=incasso[0]
                if len(playlistComuni) > 0:# and a1 != a2:
                    # print(a1.ArtistId, a2.ArtistId, playlistComuni)
                   # peso = len(playlistComuni)
                    self._grafo.add_edge(a1, a2)
        print("4 - Archi aggiunti")

    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def get_num_nodes(self) -> int:
        return self._grafo.number_of_nodes()

    def get_num_edges(self) -> int:
        return self._grafo.number_of_edges()

    def getProdottoById(self, idP):
        return self._idMapA[int(idP)]

    def getAllNodes(self):
        return DAO.getAllNodes()

    def getConnessaInfo(self):
        # lo trasformo in non orientato pk richiesto di ignorare
        components = list(nx.connected_components(self._grafo))
        #grafo_non_orientato = self._grafo.to_undirected()
        #components = list(nx.connected_components(grafo_non_orientato))

        # Se il grafo è vuoto
        if len(components) == 0:
            return 0, set(), []

        # components = list(nx.connected_components(self._grafo))  # TROVO LE COMP CONNESSE e ci faccio una lista
        largest = max(components, key=len)  # trova la + grande

        # b. Film con maggior numero di archi uscenti
        # film_max_out = max(self._grafo.nodes, key=lambda n: self._grafo.out_degree(n))
        # relativo numero archi usenti
        # max_out = self._grafo.out_degree(film_max_out)

        # ORDINO PER  GRADO!!
        ordered_nodes = sorted(largest, key=lambda n:n.Title)  # ordine decrescente
        details = [(n, len(n.list_brani)) for n in ordered_nodes]

        return len(components), largest, details

    def getGruppoAlbum(self, k, start_node):
        self._best_path = []
        self._best_score = float("-inf")

        parziale = [start_node]
        score = len(start_node.list_brani)
        self._creaMappaComponenti()

        costruttori = list(self._grafo.nodes)

        self._ricorsione(parziale,costruttori, k, score, 0)

        return self._best_path, self._best_score

    def _ricorsione(self, parziale, costruttori,k, score, pos):
        print("Entro nella ricorsione:", len(parziale), k, pos)
        if len(parziale) == k:
           # score = self._score(parziale)
          #  score = sum(len(a.list_brani) for a in parziale)

            if score >self._best_score:
                self._best_score = score
                self._best_path = list(parziale)
            return

        # Se non restano abbastanza costruttori, termino
        if len(costruttori) - pos < k - len(parziale):
            return

        # Provo i costruttori a partire dalla posizione pos
        for i in range(pos, len(costruttori)):
            candidato = costruttori[i]

            # Controllo che non ci sia già un costruttore
            # della stessa componente nella soluzione parziale
            stessa_componente = False

            for costruttore in parziale:
                if (self._mappaComponenti[candidato] == self._mappaComponenti[costruttore]):
                    stessa_componente = True
                    break

            if stessa_componente:
                continue

            parziale.append(candidato)
            self._ricorsione(parziale, costruttori,k, score + len(candidato.list_brani), i+1)
            parziale.pop()

    def _creaMappaComponenti(self):
        self._mappaComponenti = {}

       # grafoNonOrientato = self._grafo.to_undirected()
        componenti = list(nx.connected_components(self._grafo))

        for i, componente in enumerate(componenti):
            for costruttore in componente:
                self._mappaComponenti[costruttore] = i
