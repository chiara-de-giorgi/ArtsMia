import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._lunValue=None

    def handleAnalizzaOggetti(self, e):
        self._view.txt_result.controls.clear()
        self._model.buildGraph()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato!"))

        n, a = self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text(f"Il grafo contiene {n} nodi e {a} archi!"))

        self._view.update_page()

    def handleCompConnessa(self,e):
        idOggetto=self._view._txtIdOggetto.value
        if idOggetto is None or idOggetto=="":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire l'ID di un oggetto per calcolare la componente connessa!", color="red"))
            self._view.update_page()
            return

        try:
            intIdOggetto= int(idOggetto)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("L'ID di un oggetto deve essere un intero!", color="red"))
            self._view.update_page()
            return

        if intIdOggetto<0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("L'ID di un oggetto deve essere un intero positivo!", color="red"))
            self._view.update_page()
            return

        if not self._model._hasNode(intIdOggetto):
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("L'ID di un oggetto deve essere un numero valido!", color="red"))
            self._view.update_page()
            return


        compConnessa=list(self._model.getComponenenteConnessa(intIdOggetto))
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"La componente connessa contenente l'oggetto con id {intIdOggetto} è composta di {len(compConnessa)} nodi:"))

        self._view.update_page()

        self._view._ddLunghezza.disabled = False
        self._view._btnCercaOggetti.disabled = False
        listLunValues = list(range(2, len(compConnessa)))
        lunDDOption=list(map(lambda x: ft.dropdown.Option(data=x, key=x, on_click=self._choiceDDlun), listLunValues))
        self._view._ddLunghezza.options = lunDDOption
        self._view.update_page()

    def handleCercaOggetti(self, e):
        id_oggetto=int(self._view._txtIdOggetto.value)
        LUN=self._lunValue


        if LUN is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, selezionare un valore di lunghezza tra le scelte proposte. ", color="red"))
            self._view.update_page()
            return

        lun=int(LUN)
        bestPath, bestScore = self._model.getBestPath(id_oggetto, lun)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Ho trovato un cammino che parte da {id_oggetto} che ha peso totale pari a {bestScore}"))
        self._view.txt_result.controls.append(ft.Text(f"Di seguito i nodi che compongono questo cammino: ", color="green"))

        bestPath_ordinato = sorted(bestPath, key=lambda x: x.object_name)
        for p in bestPath_ordinato:
            self._view.txt_result.controls.append(ft.Text(p))

        self._view.update_page()

    def _choiceDDlun(self, e):
        self._lunValue = e.control.data






