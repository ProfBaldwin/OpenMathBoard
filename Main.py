import json
import os
import sys

import EllipseItem
import EraserWriteItem
import PixmapItem
import RectItem
import WriteItem

from BackgroundPixmap import BackgroundPixmap
from EraserToolBar import EraserToolBar
from GraphicsView import GraphicsView
from HighlighterToolBar import HighlighterToolBar
from HotkeysDialog import HotkeysDialog
from LaserToolBar import LaserToolBar
from MenuBar import MenuBar
from PenToolBar import PenToolBar
from PrimaryToolBar import PrimaryToolBar

from PySide6.QtCore import (
        Qt,
        QEvent,
        QKeyCombination,
        QObject,
        QPointF,
        QSize,
        )

from PySide6.QtGui import (
        QAction,
        QBrush,
        QGuiApplication,
        QKeySequence,
        QPainter,
        QTabletEvent,
        )

from PySide6.QtWidgets import (
        QApplication,
        QFileDialog,
        QGraphicsItem,
        QGraphicsPixmapItem,
        QMainWindow,
        QMessageBox,
        )


PRESSURE_DEADZONE = 0.05


class Main(QMainWindow):


    def __init__(self):
        super().__init__()

        self.windowTitleTemplate = "OpenMathBoard—{}[*]"
        self.setWindowTitle(self.windowTitleTemplate.format("Untitled.ombdoc"))
        self.resize(800, 600)
        self.wasMaximized = False

        self.fileName = None

        ################################################################
        # Ribbon
        ################################################################
        self.setMenuBar(MenuBar(self))

        self.primaryToolBar = PrimaryToolBar(self)
        self.addToolBar(self.primaryToolBar)

        self.addToolBarBreak()

        self.penToolBar = PenToolBar()
        self.addToolBar(self.penToolBar)

        self.eraserToolBar = EraserToolBar()
        self.addToolBar(self.eraserToolBar)
        self.eraserToolBar.hide()

        self.laserToolBar = LaserToolBar()
        self.addToolBar(self.laserToolBar)
        self.laserToolBar.hide()

        self.highlighterToolBar = HighlighterToolBar()
        self.addToolBar(self.highlighterToolBar)
        self.highlighterToolBar.hide()

        self.secondaryToolBar = self.penToolBar

        self.ribbonVisible = True

        
        ################################################################
        # Central Widget
        ################################################################
        self.new(startup = True)


        ################################################################
        # Actions
        ################################################################

        # Toggle FullScreen
        self.toggleFullScreenAction = self.addAction("Toggle Full Screen", "F11")
        self.toggleFullScreenAction.triggered.connect(self.toggleFullScreen)
        
        # Ribbon Visibility
        self.toggleRibbonVisibilityAction = self.addAction("Toggle Ribbon Visibility", "Esc")
        self.toggleRibbonVisibilityAction.triggered.connect(self.toggleRibbonVisibility)

        # Updates if background changes
        self.menuBar().backgroundMenu.triggered.connect(self.updateBackground)
        self.menuBar().backgroundMenu.modeChanged.connect(self.invertColors)

        # Switch Current Secondary Toolbar
        self.primaryToolBar.penButton.toggled.connect(
                lambda checked: self.setSecondaryToolBar(self.penToolBar, checked))
        self.primaryToolBar.eraserButton.toggled.connect(
                lambda checked: self.setSecondaryToolBar(self.eraserToolBar, checked))
        self.primaryToolBar.laserButton.toggled.connect(
                lambda checked: self.setSecondaryToolBar(self.laserToolBar, checked))
        self.primaryToolBar.highlighterButton.toggled.connect(
                lambda checked: self.setSecondaryToolBar(self.highlighterToolBar, checked))


        ################################################################
        # File Menu
        ################################################################

        self.menuBar().fileMenu.newAction.triggered.connect(self.new)
        self.menuBar().fileMenu.openAction.triggered.connect(self.open)
        self.menuBar().fileMenu.saveAction.triggered.connect(self.save)
        self.menuBar().fileMenu.saveAsAction.triggered.connect(self.saveAs)
        self.menuBar().fileMenu.exportAction.triggered.connect(self.export)
        self.menuBar().fileMenu.quitAction.triggered.connect(self.close)


        ################################################################
        # Edit Menu
        ################################################################

        self.menuBar().editMenu.clearAction.triggered.connect(self.clearScene)

        self.clipboard = QApplication.clipboard()
        self.clipboard.dataChanged.connect(self.clipboardDataChanged)
        self.clipboardDataChanged()


        ################################################################
        # Help Menu
        ################################################################

        self.menuBar().helpMenu.hotkeysAction.triggered.connect(self.hotkeysDialog)
        self.menuBar().helpMenu.aboutAction.triggered.connect(self.aboutDialog)


        ################################################################
        # Load Saved Configuration
        ################################################################
        self.loadConfig()


    def eventFilter(self, obj, event):

        # Key Press Events
        if event.type() == QEvent.KeyPress:
            # File Menu
            match event.key(), event.modifiers() & Qt.ControlModifier, event.modifiers() & Qt.ShiftModifier:
                case Qt.Key_N, Qt.ControlModifier, Qt.NoModifier:
                    self.menuBar().fileMenu.newAction.trigger()
                case Qt.Key_O, Qt.ControlModifier, Qt.NoModifier:
                    self.menuBar().fileMenu.openAction.trigger()
                case Qt.Key_S, Qt.ControlModifier, Qt.NoModifier:
                    self.menuBar().fileMenu.saveAction.trigger()
                case Qt.Key_S, Qt.ControlModifier, Qt.ShiftModifier:
                    self.menuBar().fileMenu.saveAsAction.trigger()
                case Qt.Key_Q, Qt.ControlModifier, Qt.NoModifier:
                    self.menuBar().fileMenu.quitAction.trigger()
            # Edit Menu
            match event.key(), event.modifiers() & Qt.ControlModifier, event.modifiers() & Qt.ShiftModifier:
                case Qt.Key_Z, Qt.ControlModifier, Qt.NoModifier:
                    self.menuBar().editMenu.undoAction.trigger()
                case Qt.Key_Z, Qt.ControlModifier, Qt.ShiftModifier:
                    self.menuBar().editMenu.redoAction.trigger()
                case Qt.Key_X, Qt.ControlModifier, Qt.NoModifier:
                    self.menuBar().editMenu.cutAction.trigger()
                case Qt.Key_C, Qt.ControlModifier, Qt.NoModifier:
                    self.menuBar().editMenu.copyAction.trigger()
                case Qt.Key_V, Qt.ControlModifier, Qt.NoModifier:
                    self.menuBar().editMenu.pasteAction.trigger()
                case Qt.Key_V, Qt.ControlModifier, Qt.ShiftModifier:
                    self.menuBar().editMenu.pasteInvertedAction.trigger()
                case Qt.Key_Delete, Qt.ControlModifier, Qt.NoModifier:
                    self.menuBar().editMenu.clearAction.trigger()
            # Tool Keys
            match event.key():
                case Qt.Key_F1:
                    self.primaryToolBar.penButton.setChecked(True)
                case Qt.Key_F2:
                    self.primaryToolBar.eraserButton.setChecked(True)
                case Qt.Key_F3:
                    self.primaryToolBar.laserButton.setChecked(True)
                case Qt.Key_F4:
                    self.primaryToolBar.highlighterButton.setChecked(True)
            # Slide navigation keys
            match event.key(), event.modifiers() & Qt.ControlModifier:
                case Qt.Key_Tab, Qt.ControlModifier:
                    self.primaryToolBar.nextSceneButton.click()
                case Qt.Key_Backtab, Qt.ControlModifier:
                    self.primaryToolBar.prevSceneButton.click()
            # Color Keys
            match event.key():
                case Qt.Key_1:
                    if self.secondaryToolBar.numColorButtons >= 1:
                        self.secondaryToolBar.colorButtonList[0].setChecked(True)
                case Qt.Key_2:
                    if self.secondaryToolBar.numColorButtons >= 2:
                        self.secondaryToolBar.colorButtonList[1].setChecked(True)
                case Qt.Key_3:
                    if self.secondaryToolBar.numColorButtons >= 3:
                        self.secondaryToolBar.colorButtonList[2].setChecked(True)
                case Qt.Key_4:
                    if self.secondaryToolBar.numColorButtons >= 4:
                        self.secondaryToolBar.colorButtonList[3].setChecked(True)
                case Qt.Key_5:
                    if self.secondaryToolBar.numColorButtons >= 5:
                        self.secondaryToolBar.colorButtonList[4].setChecked(True)
            # Drawing mode keys
            if self.secondaryToolBar in (self.penToolBar, self.eraserToolBar, self.highlighterToolBar):
                match event.key():
                    case Qt.Key_W:
                        self.secondaryToolBar.writeModeButton.setChecked(True)
                    case Qt.Key_E:
                        self.secondaryToolBar.ellipseModeButton.setChecked(True)
                    case Qt.Key_R:
                        self.secondaryToolBar.rectModeButton.setChecked(True)
            # Line width keys
            if self.secondaryToolBar in (self.penToolBar, self.laserToolBar, self.highlighterToolBar):
                match event.key():
                    case Qt.Key_Minus | Qt.Key_Underscore:
                        self.secondaryToolBar.lineWidthComboBox.setToPrevIndex()
                    case Qt.Key_Plus | Qt.Key_Equal:
                        self.secondaryToolBar.lineWidthComboBox.setToNextIndex()
            # Scroll keys
            match event.key():
                case Qt.Key_Up:
                    self.view.stepUp()
                case Qt.Key_Down:
                    self.view.stepDown()
                case Qt.Key_Left:
                    self.view.stepLeft()
                case Qt.Key_Right:
                    self.view.stepRight()

            return True

        return False


    def closeEvent(self, event):
        
        self.carryOn = False
        if self.isWindowModified():
            carryOn = self.saveFileMessageBox()
            if not carryOn:
                event.ignore()
                return
        
        self.saveConfig()
        

    def toggleRibbonVisibility(self):
        self.ribbonVisible = not self.ribbonVisible
        self.menuBar().setVisible(self.ribbonVisible)
        self.primaryToolBar.setVisible(self.ribbonVisible)
        self.secondaryToolBar.setVisible(self.ribbonVisible)


    def toggleFullScreen(self):
        if self.isFullScreen():
            if self.wasMaximized:
                self.showMaximized()
            else:
                self.showNormal()
        else:
            self.wasMaximized = self.isMaximized()
            self.showFullScreen()

    
    def setSecondaryToolBar(self, newToolBar, checked):
        if checked:
            self.secondaryToolBar.hide()
            self.secondaryToolBar = newToolBar
            self.secondaryToolBar.resetMode()
            if self.ribbonVisible:
                self.secondaryToolBar.show()


    def new(self, startup = False):

        if not startup:
            
            # Check if file has been saved
            self.carryOn = False
            if self.isWindowModified():
                carryOn = self.saveFileMessageBox()
                if not carryOn:
                    return

            # Out with the old
            self.primaryToolBar.prevSceneButton.pressed.disconnect()
            self.primaryToolBar.nextSceneButton.pressed.disconnect()

            self.menuBar().editMenu.cutAction.triggered.disconnect()
            self.menuBar().editMenu.copyAction.triggered.disconnect()
            self.menuBar().editMenu.pasteAction.triggered.disconnect()
            self.menuBar().editMenu.pasteInvertedAction.triggered.disconnect()

            del self.view
            self.penToolBar.itemList = []
            self.eraserToolBar.itemList = []
            self.laserToolBar.itemList = []
            self.highlighterToolBar.itemList = []

        # In with the new
        self.view = GraphicsView(self)
        self.setCentralWidget(self.view)
        self.item = None

        self.updateBackground()

        # Slide/scene navigation
        self.primaryToolBar.prevSceneButton.pressed.connect(self.prevScene)
        self.primaryToolBar.nextSceneButton.pressed.connect(self.nextScene)

        # Undo
        self.setupUndo(None, self.view.scene().undoStack)

        # Cut, copy, paste
        self.menuBar().editMenu.cutAction.triggered.connect(self.view.cut)
        self.menuBar().editMenu.copyAction.triggered.connect(self.view.copy)
        self.menuBar().editMenu.pasteAction.triggered.connect(self.view.paste)
        self.menuBar().editMenu.pasteInvertedAction.triggered.connect(lambda: self.view.paste(inverted = True))

        # Reset scene count label
        self.primaryToolBar.prevSceneButton.setDisabled(True)
        self.primaryToolBar.updateSceneCountLabel(1, 1)

        # Reset file info
        self.fileName = None
        self.setWindowTitle(self.windowTitleTemplate.format("Untitled.ombdoc"))
        self.setWindowModified(False)


    def open(self):

        # Check if file has been saved
        self.carryOn = False
        if self.isWindowModified():
            carryOn = self.saveFileMessageBox()
            if not carryOn:
                return

        openDialog = QFileDialog(self)
        openDialog.setAcceptMode(QFileDialog.AcceptOpen)
        openDialog.setNameFilter("*.ombdoc")
        openDialog.fileSelected.connect(self.openDialogComplete)
        openDialog.exec()


    def openDialogComplete(self, fileName):

        try:
            with open(fileName, "r") as f:

                data = json.load(f)

                self.new()

                savedMode = data["mode"]
                if savedMode != self.menuBar().backgroundMenu.getMode():
                    self.penToolBar.invertColors()
                    self.highlighterToolBar.invertColors()
                
                sceneDataList = data["scene data list"]
                for i, sceneData in enumerate(sceneDataList):

                    # Start in a new scene
                    if i > 0:
                        self.view.addScene()

                    # Load each item in the scene
                    for itemData in sceneData:

                        match itemData["type"]:

                            case "write item":
                                item = WriteItem.loadFromData(itemData)
                                if itemData["highlighter"]:
                                    self.highlighterToolBar.itemList.append(item)
                                else:
                                    self.penToolBar.itemList.append(item)
                                self.view.scene().addItem(item)

                            case "ellipse item":
                                item = EllipseItem.loadFromData(itemData, self.backgroundBrush)
                                if itemData["highlighter"]:
                                    self.highlighterToolBar.itemList.append(item)
                                elif itemData["eraser"]:
                                    self.eraserToolBar.itemList.append(item)
                                else:
                                    self.penToolBar.itemList.append(item)
                                self.view.scene().addItem(item)

                            case "rect item":
                                item = RectItem.loadFromData(itemData, self.backgroundBrush)
                                if itemData["highlighter"]:
                                    self.highlighterToolBar.itemList.append(item)
                                elif itemData["eraser"]:
                                    self.eraserToolBar.itemList.append(item)
                                else:
                                    self.penToolBar.itemList.append(item)
                                self.view.scene().addItem(item)

                            case "eraser write item":
                                item = EraserWriteItem.loadFromData(itemData, self.backgroundBrush)
                                self.eraserToolBar.itemList.append(item)
                                self.view.scene().addItem(item)

                            case "pixmap item":
                                item = PixmapItem.loadFromData(itemData, self.view.scene())

                        self.view.scene().itemFinished(item)

                if savedMode != self.menuBar().backgroundMenu.getMode():
                    self.penToolBar.invertColors()
                    self.highlighterToolBar.invertColors()

                self.view.setSceneIndex(0)
                self.primaryToolBar.prevSceneButton.setEnabled(False)
                self.primaryToolBar.updateSceneCountLabel(
                        self.view.currentSceneIndex() + 1, self.view.sceneCount())
        except:
            print("ERROR: Unable to load", fileName)

        # Set file info
        self.fileName = fileName
        self.setWindowTitle(self.windowTitleTemplate.format(os.path.basename(fileName)))
        self.setWindowModified(False)


    def save(self):

        if self.fileName is None:
            self.saveAs()
        else:
            self.view.save(self.fileName)
        self.setWindowModified(False)


    def saveAs(self):
        saveAsDialog = QFileDialog(self)
        saveAsDialog.setAcceptMode(QFileDialog.AcceptSave)
        saveAsDialog.setNameFilter("*.ombdoc")
        saveAsDialog.setDefaultSuffix(".ombdoc")
        saveAsDialog.fileSelected.connect(self.saveAsDialogComplete)
        saveAsDialog.exec()
        

    def saveAsDialogComplete(self, fileName):
        self.fileName = fileName
        self.setWindowTitle(self.windowTitleTemplate.format(os.path.basename(fileName)))
        self.save()
    

    def export(self):
        exportDialog = QFileDialog(self)
        exportDialog.setAcceptMode(QFileDialog.AcceptSave)
        exportDialog.setNameFilter("*.pdf")
        exportDialog.setDefaultSuffix(".pdf")
        exportDialog.fileSelected.connect(self.view.export)
        exportDialog.exec()


    def prevScene(self):
        if self.view.currentSceneIndex() > 0 and self.view.item is None:
            self.view.selectedItem.setSelected(False)
            oldUndoStack = self.view.scene().undoStack
            self.view.prevScene()
            newUndoStack = self.view.scene().undoStack
            self.setupUndo(oldUndoStack, newUndoStack)
            self.primaryToolBar.prevSceneButton.setDisabled(self.view.currentSceneIndex() == 0)
            self.primaryToolBar.updateSceneCountLabel(self.view.currentSceneIndex() + 1, self.view.sceneCount())


    def nextScene(self):
        if self.view.item is None:
            self.view.selectedItem.setSelected(False)
            oldUndoStack = self.view.scene().undoStack
            if self.view.currentSceneIndex() + 1 == self.view.sceneCount():
                self.view.addScene()
            else:
                self.view.nextScene()
            newUndoStack = self.view.scene().undoStack
            self.setupUndo(oldUndoStack, newUndoStack)
            self.primaryToolBar.prevSceneButton.setEnabled(True)
            self.primaryToolBar.updateSceneCountLabel(self.view.currentSceneIndex() + 1, self.view.sceneCount())


    def setupUndo(self, oldUndoStack, newUndoStack):

        # Disconnect old connections
        if oldUndoStack is not None:
            oldUndoStack.canUndoChanged.disconnect()
            oldUndoStack.canRedoChanged.disconnect()
            self.menuBar().editMenu.undoAction.triggered.disconnect()
            self.menuBar().editMenu.redoAction.triggered.disconnect()

        # Set whether undo/redo actions enabled based on undo stack
        self.menuBar().editMenu.undoAction.setEnabled(newUndoStack.canUndo())
        self.menuBar().editMenu.redoAction.setEnabled(newUndoStack.canRedo())

        # Update whether undo/redo actions enabled
        newUndoStack.canUndoChanged.connect(self.menuBar().editMenu.undoAction.setEnabled)
        newUndoStack.canRedoChanged.connect(self.menuBar().editMenu.redoAction.setEnabled)

        # Connect undo/redo actions
        self.menuBar().editMenu.undoAction.triggered.connect(newUndoStack.undo)
        self.menuBar().editMenu.redoAction.triggered.connect(newUndoStack.redo)
        
        # Connect undo/redo actions to show file has changed
        self.menuBar().editMenu.undoAction.triggered.connect(lambda: self.setWindowModified(True))
        self.menuBar().editMenu.redoAction.triggered.connect(lambda: self.setWindowModified(True))


    def clipboardDataChanged(self):
        self.menuBar().editMenu.pasteAction.setDisabled(self.clipboard.pixmap().isNull())
        self.menuBar().editMenu.pasteInvertedAction.setDisabled(self.clipboard.pixmap().isNull())


    def clearScene(self):
        if self.view.item is None:
            self.view.selectedItem.setSelected(False)
            clearRectItem = self.eraserToolBar.eraseRect(self.view.scene().sceneRect())
            self.view.scene().addItem(clearRectItem)
            self.view.scene().itemFinished(clearRectItem)
            clearRectItem.update()


    def updateBackground(self):
        mode = self.menuBar().backgroundMenu.getMode()
        gridSize = self.menuBar().backgroundMenu.getGridSize()

        self.backgroundBrush = QBrush()
        self.backgroundBrush.setTexture(BackgroundPixmap(mode, gridSize))
        self.view.setBackground(self.backgroundBrush)
        self.eraserToolBar.updateBackground(self.backgroundBrush)


    def invertColors(self):
        self.penToolBar.invertColors()
        self.laserToolBar.invertColors()
        self.highlighterToolBar.invertColors()
        self.view.invertColors()


    def saveConfig(self):

        config = {}

        # Background
        config["background mode"] = self.menuBar().backgroundMenu.getMode()
        config["background grid size"] = self.menuBar().backgroundMenu.getGridSize()

        # Pen
        config["pen width index"] = self.penToolBar.lineWidthComboBox.currentIndex()
        config["pen alt index"] = self.penToolBar.altStyleComboBox.currentIndex()

        # Laser
        config["laser color index"] = self.laserToolBar.colorButtonGroup.checkedId()
        config["laser width index"] = self.laserToolBar.lineWidthComboBox.currentIndex()

        # Highlighter
        config["highlighter color index"] = self.highlighterToolBar.colorButtonGroup.checkedId()
        config["highlighter width index"] = self.highlighterToolBar.lineWidthComboBox.currentIndex()

        # Save to json
        with open("config.json", "w") as f:
            json.dump(config, f)


    def loadConfig(self):
        try:
            with open("config.json", "r") as f:

                config = json.load(f)

                # Background
                self.menuBar().backgroundMenu.setMode(config["background mode"])
                self.menuBar().backgroundMenu.setGridSize(config["background grid size"])
                self.menuBar().backgroundMenu.checkModeChanged()
                self.updateBackground()

                # Pen
                self.penToolBar.lineWidthComboBox.setCurrentIndex(config["pen width index"])
                self.penToolBar.altStyleComboBox.setCurrentIndex(config["pen alt index"])

                # Laser
                self.laserToolBar.colorButtonList[config["laser color index"]].setChecked(True)
                self.laserToolBar.lineWidthComboBox.setCurrentIndex(config["laser width index"])

                # Highlighter
                self.highlighterToolBar.colorButtonList[config["highlighter color index"]].setChecked(True)
                self.highlighterToolBar.lineWidthComboBox.setCurrentIndex(config["highlighter width index"])
        
        except:
            pass


    def saveFileMessageBox(self):
        msgBox = QMessageBox(self)
        msgBox.setWindowTitle("Save Changes?")
        msgBox.setText("Do you want to save your changes?")
        msgBox.setInformativeText("The document has been modified.")
        msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        msgBox.button(QMessageBox.Discard).setText("Don't Save")
        msgBox.setDefaultButton(QMessageBox.Save)

        choice = msgBox.exec()

        match choice:
            case QMessageBox.Save:
                self.save()
                self.carryOn = True
            case QMessageBox.Discard:
                self.carryOn = True
            case QMessageBox.Cancel:
                self.carryOn = False

        return self.carryOn


    def hotkeysDialog(self):
        hotkeysDialog = HotkeysDialog(self)
        hotkeysDialog.exec()


    def aboutDialog(self):
        text = "OpenMathBoard is (C) 2023 by Taylor Baldwin. All rights reserved.\n\n"
        text += "OpenMathBoard is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License. You can find source code for this software at SOMEPLACE ON GITHUB.\n\n"
        text += "OpenMathBoard is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more detiails.\n\n"
        text += "You should have received a copy of the GNU General Public License along with OpenMathBoard. If not, see https://gnu.org/licenses/gpl-3.0.html"

        QMessageBox.about(self, "About OpenMathBoard", text)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()
    app.installEventFilter(main)
    main.show()
    app.exec()
