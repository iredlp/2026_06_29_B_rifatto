import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):
        try:
            self._model.creaGrafo()
            n_nodes = self._model.get_num_nodes()
            n_edges = self._model.get_num_edges()
            # Stampa immediata numero di vertici e archi (Punto 1.c)
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text(f"Grafo creato con successo!\nNumero vertici: {n_nodes}\nNumero archi: {n_edges}",
                        color="green"))
            # RIEMPIO IL DROPDOWN DEI FILM DEL GRAFO
            self.fillDDAlbum()
        except Exception as ex:
            self._view._txt_result.controls.append(
                ft.Text(f"Errore durante la creazione del grafo: {ex}", color="red"))
            # return
        self._view.update_page()

    def handleStampaInfo(self,e):
        self._view._txt_result.controls.clear()

        numero, largest, details = self._model.getConnessaInfo()
        self._view._txt_result.controls.clear()

        # self._view._txt_result.controls.append(
        # ft.Text(f"Film con maggior numero archi uscenti: {film_max_out} (archi uscenti: {max_out})\n", color="green"))
        self._view._txt_result.controls.append(
            ft.Text(f"Il grafo ha  {numero} componenti connesse\n", color="orange"))

        self._view._txt_result.controls.append(
            ft.Text(f"La componente connessa maggiore ha dimensione  {len(largest)}\n", color="green"))

        self._view._txt_result.controls.append(
            ft.Text(f"La componente connessa maggiore in ordine ALFABETICO \n", color="green"))

        for titolo, numero_brani in details:
            self._view._txt_result.controls.append(ft.Text(f"{titolo}: {numero_brani} brani"))
        self._view.update_page()

    def fillDDAlbum(self):
        try:
            self._view._ddAlbum .options.clear()
            attori = self._model.getAllNodes()
            for actor in attori:
                self._view._ddAlbum .options.append(ft.dropdown.Option(key=actor.AlbumId,
                                                                        text=actor.Title))
        # self._view.update_page()
        except Exception as ex:
            self._view._txt_result.controls.append(
                ft.Text(f"Errore nel recupero degli ALBUM: {ex}", color="red"))

        self._view.update_page()


    def handleSelezione(self,e):
        self._view._txt_result.controls.clear()
        if self._model.get_num_nodes() == 0 :
            self._view.create_alert("Creare prima il grafo!", color="red")
            return
        k = self._view._txtInN.value
        # qui dovremmo fare i solti controlli sulla validità
        try:
            kInt = int(k)
        except Exception as ex:
            self._view._txt_result.controls.append(
                ft.Text(f"Errore ! devi inserire un intero per procedere: {ex}", color="red"))
            self._view.update_page()
            return
        if kInt <= 0:
            self._view.create_alert(
                "La soglia deve essere un intero positivo.", color="red")
            return

        start = self._model.getProdottoById(self._view._ddAlbum.value)
        # end = self._model.getProdottoById(self._view._ddProdEnd.value)
        # qui dovremmo fare i solti controlli sulla validità

        if start is None:
            self._view._txt_result.controls.append(
                ft.Text(f"Errore ! devi inserire i nodi iniziali   per procedere!", color="red")
            )
            self._view.update_page()
            return

        gruppo, punteggio = self._model.getGruppoAlbum(kInt, start)

        gruppo.sort(key=lambda x: x.Title)  # ORDINE ALFABETICO!


        if len(gruppo) < kInt:
            self._view._txt_result.controls.append(
                ft.Text("Non esiste una selezione valida di K artisti."))
            self._view.update_page()
            return

        self._view._txt_result.controls.append(
            ft.Text(f"numero totale di ALBUM selezionati: {len(gruppo)}"))

        for prodotto in gruppo:
            self._view._txt_result.controls.append(
                ft.Text(
                    f"{prodotto.Title} - "
                    f" che compare in {len(prodotto.list_brani)} brani"))

        tot = 0
        for prodotto in gruppo:
            tot += len(prodotto.list_brani)

        self._view._txt_result.controls.append(ft.Text(
            f"Totale di brani della soluzione ottime: {tot}"))

        self._view.update_page()
