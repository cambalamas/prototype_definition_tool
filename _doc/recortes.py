geometry = app.primaryScreen().availableGeometry()
doExit = self.nAction('Exit','Ctrl+Q','Leave the app!',self.close)

#
# MULTIIDIOMA
#
#
# presenter:
#
## @brief      Configura 'locale' de i18n para ver la interfaz en Español.
## @param      self  Este objeto
## @return     None
def listener_TrEs(self):
	i18n.set('locale', 'es')

## @brief      Configura 'locale' de i18n para ver la interfaz en Ingles.
## @param      self  El objeto presentador.
## @return     None
def listener_TrEn(self):
	i18n.set('locale', 'en')

## @brief      Configura 'locale' de i18n para ver la interfaz en Frances.
## @param      self  El objeto presentador.
## @return     None
def listener_TrFr(self):
	i18n.set('locale', 'fr')

## @brief      Configura 'locale' de i18n para ver la interfaz en Aleman.
## @param      self  El objeto presentador.
## @return     None
def listener_TrDe(self):
	i18n.set('locale', 'de')
#
# señales en view:
#
def emit_TrEs(self):
	self.signal_TrEs.emit()
def emit_TrEn(self):
	self.signal_TrEn.emit()
def emit_TrFr(self):
	self.signal_TrFr.emit()
def emit_TrDe(self):
	self.signal_TrDe.emit()
#
# menu actions en gui:
#
act = mHelp.addAction('Traducir a Español')
act.setCheckable(True)
act.setIcon(icon('trES.ico'))
act.setStatusTip('Traduce los textos a Español')
actions.append(act)
act = mHelp.addAction('Translate to English')
act.setCheckable(True)
act.setIcon(icon('trEN.ico'))
act.setStatusTip('The texts translated into English')
actions.append(act)
act = mHelp.addAction('Traduire en français')
act.setCheckable(True)
act.setIcon(icon('trFR.ico'))
act.setStatusTip('Les textes traduits en français')
actions.append(act)
act = mHelp.addAction('Übersetzen Sie zum Deutsch')
act.setCheckable(True)
act.setIcon(icon('trDE.ico'))
act.setStatusTip('Die Texte ins Deutsche übersetzt')
actions.append(act)


#------------------------------------------------------------------------------#

#
# MOVIMIENTO DE UN qgItem
#
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


#------------------------------------------------------------------------------#

#
# Cuando alguno de los campos que permiten edicion de una fila
# del arbol sufre cualquier cambio, sera evaluado desde aqui.
#
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
		# Guardamos la modificacion en la estructura de datos. (version dict)
		compData = { 'Name':name,
					 'Visible':visible,
					 'Active':active }
		# Actualizamos el modelo.
		self.model.modComponent(compId,compData)
