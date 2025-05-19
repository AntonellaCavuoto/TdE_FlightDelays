from datetime import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._choiceDDAeroportoP = None
        self._choiceDDAeroportoD = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleAnalizza(self, e):
        # self._view.txt_result.controls.append(ft.Text(f"Hello, {name}!"))
        # self._view.update_page()
        cMinTxt = self._view._txtInCMin.value
        if cMinTxt == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire un valore numerico."))
            self._view.update_page()
            return

        try:
            cMin = int(cMinTxt)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Il valore inserito non è un intero."))
            self._view.update_page()
            return

        if cMin <= 0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire un intero positivo."))
            self._view.update_page()
            return

        self._model.buildGraph(cMin)
        # dopo aver costruito il grafo prendo i nodi per il DD
        allNodes = self._model.getAllNodes()
        self.fillDDNodes(allNodes)

        nNodes, nEdges = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi:{nNodes}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi:{nEdges}"))
        self._view.update_page()

    def handleConnessi(self, e):
        if self._choiceDDAeroportoP is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, selezionare una voce dal menù."))
            self._view.update_page()
            return

        viciniTuple = self._model.getSortedNeighbors(self._choiceDDAeroportoP)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Di seguito i vicini di {self._choiceDDAeroportoP}"))
        for v in viciniTuple:
            self._view.txt_result.controls.append(ft.Text(f"{v[0]} - peso: {v[1]}"))
        self._view.update_page()

    def handlePercorso(self, e):
        if self._choiceDDAeroportoP is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, selezionare una voce dal menù come partenza."))
            self._view.update_page()
            return
        if self._choiceDDAeroportoD is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione, selezionare una voce dal menù come destinazione."))
            self._view.update_page()
            return

        path = self._model.getPath(self._choiceDDAeroportoP, self._choiceDDAeroportoD)
        if len(path) == 0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(f"Cammino fra {self._choiceDDAeroportoP} e {self._choiceDDAeroportoD} non trovato."))

        else:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(f"Cammino fra {self._choiceDDAeroportoP} e {self._choiceDDAeroportoD} trovato!"
                        f"Di seguito i nodi del cammino"))

            for p in path:
                self._view.txt_result.controls.append(
                    ft.Text(p))
        self._view.update_page()

    def handleCerca(self, e):
        v0 = self._choiceDDAeroportoP
        v1 = self._choiceDDAeroportoD
        t = self._view._txtInTratteMax.value
        tInt = int(t)

        tic = datetime.now()
        path, scoreTot = self._model.getCamminoOttimo(v0, v1, tInt)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Il percorso ottimo fra {v0} e {v1} è:"))
        for p in path:
            self._view.txt_result.controls.append(ft.Text(p))
        self._view.txt_result.controls.append(
            ft.Text(f"Score: {scoreTot}"))
        self._view.txt_result.controls.append(
            ft.Text(f"Percorso trovato in {datetime.now() - tic}"))
        self._view.update_page()

    def fillDDNodes(self, allNodes):
        for n in allNodes:
            self._view._ddAeroportoP.options.append(
                ft.dropdown.Option(data=n,
                                   key=n.IATA_CODE,
                                   on_click=self.pickDDPartenza))  # quando seleziono voce salva la voce
            self._view._ddAeroportoD.options.append(
                ft.dropdown.Option(data=n,
                                   key=n.IATA_CODE,
                                   on_click=self.pickDdDestinazione))

    def pickDDPartenza(self, e):
        self._choiceDDAeroportoP = e.control.data  # recupero oggetto selezionato
        print("PickDDPartenza called", self._choiceDDAeroportoP)

    def pickDdDestinazione(self, e):
        self._choiceDDAeroportoD = e.control.data  # recupero oggetto selezionato
        print("PickDdDestinazione called", self._choiceDDAeroportoD)
