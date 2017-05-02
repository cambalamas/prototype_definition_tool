geometry = app.primaryScreen().availableGeometry()
doExit = self.nAction('Exit','Ctrl+Q','Leave the app!',self.close)





def getCurState(__V):

	# Creamos una copia de las escena actual.
	scene = []

	# Creamos una copia de la cola de componentes simples actual.
	simpleStorage = []
	for item in __M.getSimpleCompStorage():
		scItem = copy(item)
		scene.append(scItem)
		simpleStorage.append(scItem)

	# Creamos una copia de la cola de componentes complejos actual.
	complexStorage = []
	for item in __M.getComplexCompStorage():
		ccItem = copy(item)
		scene.append(ccItem)
		complexStorage.append(ccItem)

	# Volteamos el array para respetar el orden de la pila.
	scene.reverse()

	# Devolvemos dichas copias en forma de tupla.
	return (scene,deque(simpleStorage),deque(complexStorage))


''' Recupera el anterior estado en el historico de Deshacer. '''

def getPrevState(__V):

	saveStateFromUndo(__V)

	# Recuperamos la tupla del estado anterior.
	toUndo = __M.getPrevState()

	if toUndo is not None:
		# Asignamos lo que representa cada elemento.
		prevScene 			= toUndo[0]
		prevSimpleStorage 	= toUndo[1]
		prevComplexStorage 	= toUndo[2]

		# Recuperamos el estado de la escena.
		__V.centralWidget().scene().clear()
		for item in prevScene:
			print(item)
			print(prevSimpleStorage)
			__V.centralWidget().scene().addItem(item)
		# Recuperamos el estado de la cola de componentes simples.
		__M.setSimpleCompStorage(prevSimpleStorage)
		# Recuperamos el estado de la cola de componentes complejos.
		__M.setComplexCompStorage(prevComplexStorage)

		# Actualizamos la informacion mostrada en el Arbol.
		updateTrees(__V)


''' Recupera el siguiente estado en el historico de Rehacer. '''

def getNextState(__V):

	saveStateFromRedo(__V)

	# Recuperamos la tupla del estado anterior.
	toRedo = __M.getNextState()

	if toRedo is not None:
		# Asignamos lo que representa cada elemento.
		nextScene 			= toRedo[0]
		nextSimpleStorage 	= toRedo[1]
		nextComplexStorage 	= toRedo[2]

		# Recuperamos el estado de la escena.
		__V.centralWidget().scene().clear()
		for item in nextScene:
			print(item)
			print(nextSimpleStorage)
			__V.centralWidget().scene().addItem(item)
		# Recuperamos el estado de la cola de componentes simples.
		__M.setSimpleCompStorage(nextSimpleStorage)
		# Recuperamos el estado de la cola de componentes complejos.
		__M.setComplexCompStorage(nextComplexStorage)

		# Actualizamos la informacion mostrada en el Arbol.
		updateTrees(__V)






	# def __str__( self ):
	# 	retVal = '\nRUTA\t--->\t'+str(self.getPath())
	# 	retVal += '\n\nNOMBRE\t--->\t" '+self.getName()+' "'
	# 	retVal += '\n\n--------------------\n'
	# 	retVal += '\nZ\t\t--->\t'+str(self.getPosZ())
	# 	retVal += '\nACTIVO\t\t--->\t'+str(self.getActive())
	# 	retVal += '\nVISIBLE\t\t--->\t'+str(self.getVisible())
	# 	retVal += '\nY\t\t--->\t'+str(self.getPosY())
	# 	retVal += '\nX\t\t--->\t'+str(self.getPosX())
	# 	retVal += '\nALTO\t\t--->\t'+str(self.getSizeY())
	# 	retVal += '\nANCHO\t\t--->\t'+str(self.getSizeX())
	# 	return retVal


	# Necesario para luego tener acceso a 'e.lastPos()'.
	def mousePressEvent(self, ev):
		ev.accept()


	# Mientras se manteniene clicado.
	def mouseMoveEvent(self, ev):
		ELogic.saveState(self.getWindow())
		# Si esta pulsado el boton izquierdo del raton.
		if ev.buttons() == Qt.LeftButton:
			# Calcular nueva posicion en base al desplazamiento del cursor.
			newPos = ev.pos() - ev.lastPos()
			# Calculamos X e Y teniendo en cuenta el factor de escalado.
			x = newPos.x() * self.scale()
			y = newPos.y() * self.scale()
			# Mover en base a la posicion calculada.
			self.moveBy(x,y)




	""" Cuando alguno de los campos que permiten edicion de una fila
	del arbol sufre cualquier cambio, sera evaluado desde aqui. """

	def listener_simpleTreeItemChange(self):
		tree = self.view.getSimpleTree()
		indexList = tree.selectedIndexes()

		for index in indexList:

			# Fila correspondiente al item seleccionado.
			row = tree.model().itemFromIndex(index)

			# Recupero los datos cambiado.
			name = row.data(0)

			if row.data(1) == Qt.Checked:
				visible = True
			else:
				visible = False

			if row.data(2) == Qt.Checked:
				active = True
			else:
				active = False

			# Recuperamos el id 'ocultado' en el hijo.
			compID = row.child(0,0).data(Qt.UserRole)

			# Guardamos la modificacion en la estructura de datos.
			compData = { 'Name':name,
						 'Visible':visible,
						 'Active':active }

			# Actualizamos el modelo.
			self.model.modComponent(compId,compData)




## CODIGO A REUBICAR.
# --------------------------------------------------------------------------


	# ----------------------------------------------------------------------- #
	#					 	- ACTUALIZADORES DEL MODELO - 				   	  #
	# ----------------------------------------------------------------------- #


	''' Solicitud de borrado invocada desde el propio objeto.'''

	def directDelSimpleComp(item):
		# Borrar del almacenaje.
		self.model.delSimpleComp(item)
		# Borrar de la escena.
		self.view.centralWidget().scene().removeItem(item)
		# Actualizamos la vista: TREEVIEW
		updateTrees(self.view)



	# ----------------------------------------------------------------------- #
	#					 		 	- ARBOLES - 				   			  #
	# ----------------------------------------------------------------------- #


	''' Dado un arbol devuelve el ID del item seleccionado '''

	# def getTreeSelectedItemID(tree):
	# 	indexList = tree.selectedIndexes()
	# 	if indexList is not None:
	# 		firstCol = tree.model().itemFromIndex(index[0])
	# 		itemID = firstCol.child(0,0).data(Qt.UserRole)
	# 		return itemID


	''' Actualiza los arboles en base a EModel. '''

	def updateTrees():
		model = self.view.simpleCompsTree.model()

		# Borramos el contenido actual del arbol.
		model.removeRows(0, model.rowCount())

		# Rellenamos el arbol en base al contenido de la cola.
		for elem in self.model.getSimpleCompStorage():

			# Nombre del elemento.
			col1 = QStandardItem(elem.getName())

			# Estado Visible del elemento.
			col2 = QStandardItem()
			col2.setEditable(False)
			# Estado del check.
			if elem.getVisible() == True:
				col2.setCheckState(Qt.Checked)
			else:
				col2.setCheckState(Qt.Unchecked)

			# Estado Acvtivo del elemento.
			col3 = QStandardItem()
			col3.setEditable(False)
			# Estado del check.
			if elem.getActive() == True:
				col3.setCheckState(Qt.Checked)
			else:
				col3.setCheckState(Qt.Unchecked)

			# Posicion Z para facilitar el control de la profundidad.
			col4 = QStandardItem(str(elem.getPosZ()))
			col4.setEditable(False)

			# Guardamos el ID de forma oculta.
			child = QStandardItem()
			child.setData(elem.getID(),Qt.UserRole)
			col1.setChild(0,0,child)

			# Componemos la fila y la agregamos al arbol.
			model.appendRow( [col1 , col2, col3, col4] )


	''' Atiende a la señal 'ItemCanged' del modelo qt del treeview '''

	def simpleCompsTreeItemChanged():
		tree = self.view.simpleCompsTree
		indexList = tree.selectedIndexes()
		if indexList is not None:
			# Recupero el dato cambiado. (Solo se permite cambiar el nombre)
			firstColData = tree.model().itemFromIndex(indexList[0]).data(0)
			# Columna donde 'ocultamos' el id del objeto.
			firstCol = tree.model().itemFromIndex(indexList[0])
			# Recuperamos el id 'ocultado' en el hijo.
			itemID = firstCol.child(0,0).data(Qt.UserRole)

			# Guardamos la modificacion en la estructura de datos.
			item = self.model.getSimpleComp(itemID)
			item.setName(firstColData)
