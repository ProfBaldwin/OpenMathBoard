from PySide6.QtCore import (
        Qt,
        )

from PySide6.QtGui import (
        QKeySequence,
        )

from PySide6.QtWidgets import (
        QDialog,
        QVBoxLayout,
        QTextEdit,
        )


class HotkeysDialog(QDialog):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("OpenMathBoard Hotkeys and Shortcuts")
        self.setMinimumSize(600, 600)

        textEdit = QTextEdit(self)
        textEdit.setReadOnly(True)

        text = "<h1>Hotkeys and Shortcuts</h1>\n"
        text += "<p>OpenMathBoard is a simple whiteboard application designed to get out of your way and let you teach. The application is meant to be used with a pen tablet together with the keyboard for quick access to tools and features. This short guide will introduce the application's hotkeys and shortcuts.</p>\n"

        text += "<h2>General</h2>\n"
        text += "<p>The hotkeys below are general to the application and can be used while using any tool.</p>"
        text += "<div style=\"margin-left: auto;\">"
        text += "<table>"
        text += "   <tr>"
        text += "       <th align=\"left\">Hotkey</th>"
        text += "       <th align=\"left\">Function</th>"
        text += "   </tr>"
        text += "   <tr>"
        text += "       <td>Esc</td>"
        text += "       <td>Hide/Show Ribbon</td>"
        text += "   </tr>"
        text += "   <tr>"
        text += "       <td>Arrow Keys</td>"
        text += "       <td>Scroll Left, Right, Up, and Down</td>"
        text += "   </tr>"
        text += "   <tr>"
        text += "       <td>F1</td>"
        text += "       <td>Select Pen Tool</td>"
        text += "   </tr>"
        text += "   <tr>"
        text += "       <td>F2</td>"
        text += "       <td>Select Eraser Tool</td>"
        text += "   </tr>"
        text += "   <tr>"
        text += "       <td>F3</td>"
        text += "       <td>Select Laser Tool</td>"
        text += "   </tr>"
        text += "   <tr>"
        text += "       <td>F4</td>"
        text += "       <td>Select Highlighter Tool</td>"
        text += "   </tr>"
        text += "   <tr>"
        text += "       <td>F11</td>"
        text += "       <td>Toggle Fullscreen</td>"
        text += "   </tr>"
        text += "   <tr>"
        text += "       <td>{}</td>".format(QKeySequence(Qt.CTRL | Qt.Key_Tab).toString())
        text += "       <td>Next Board</td>"
        text += "   </tr>"
        text += "   <tr>"
        text += "       <td>{}</td>".format(QKeySequence(Qt.CTRL | Qt.SHIFT | Qt.Key_Tab).toString())
        text += "       <td>Previous Board</td>"
        text += "   </tr>"
        text += "   <tr>"
        text += "       <td>{}</td>".format(QKeySequence(Qt.CTRL | Qt.Key_N).toString())
        text += "       <td>File &gt; New</td>"
        text += "   </tr>"
        text += "   <tr>"
        text += "       <td>{}</td>".format(QKeySequence(Qt.CTRL | Qt.Key_O).toString())
        text += "       <td>File &gt; Open...</td>"
        text += "   </tr>"
        text += "   <tr>"
        text += "       <td>{}</td>".format(QKeySequence(Qt.CTRL | Qt.Key_S).toString())
        text += "       <td>File &gt; Save</td>"
        text += "   </tr>"
        text += "   <tr>"
        text += "       <td>{}</td>".format(QKeySequence(Qt.CTRL | Qt.SHIFT | Qt.Key_S).toString())
        text += "       <td>File &gt; Save As...</td>"
        text += "   </tr>"
        text += "   <tr>"
        text += "       <td>{}</td>".format(QKeySequence(Qt.CTRL | Qt.Key_Q).toString())
        text += "       <td>File &gt; Quit</td>"
        text += "   </tr>"
        text += "   <tr>"
        text += "       <td>{}</td>".format(QKeySequence(Qt.CTRL | Qt.Key_Z).toString())
        text += "       <td>Edit &gt; Undo</td>"
        text += "   </tr>"
        text += "   <tr>"
        text += "       <td>{}</td>".format(QKeySequence(Qt.CTRL | Qt.SHIFT | Qt.Key_Z).toString())
        text += "       <td>Edit &gt; Redo</td>"
        text += "   </tr>"
        text += "   <tr>"
        text += "       <td>{}</td>".format(QKeySequence(Qt.CTRL | Qt.Key_X).toString())
        text += "       <td>Edit &gt; Cut Image</td>"
        text += "   </tr>"
        text += "   <tr>"
        text += "       <td>{}</td>".format(QKeySequence(Qt.CTRL | Qt.Key_C).toString())
        text += "       <td>Edit &gt; Copy Image</td>"
        text += "   </tr>"
        text += "   <tr>"
        text += "       <td>{}</td>".format(QKeySequence(Qt.CTRL | Qt.Key_V).toString())
        text += "       <td>Edit &gt; Paste Image</td>"
        text += "   </tr>"
        text += "   <tr>"
        text += "       <td>{}</td>".format(QKeySequence(Qt.CTRL | Qt.SHIFT | Qt.Key_V).toString())
        text += "       <td>Edit &gt; Paste Image with Colors Inverted</td>"
        text += "   </tr>"
        text += "   <tr>"
        text += "       <td>{}</td>".format(QKeySequence(Qt.CTRL | Qt.Key_Delete).toString())
        text += "       <td>Edit &gt; Clear Board</td>"
        text += "   </tr>"
        text += "</table>"
        text += "</div>"

        text += "<h2>Tools</h2>\n"
        text += "<p>OpenMathBoard has four primary tools: Pen, Eraser, Laser, Highlighter. The hotkeys below are used to change the options for these tools. Not all options are available for all tools.</p>\n"
        text += "<div style=\"margin-left: auto;\">"
        text += "<table>"
        text += "   <tr>"
        text += "       <th align=\"left\">Hotkey</th>"
        text += "       <th align=\"left\">Function</th>"
        text += "   </tr>"
        text += "   <tr>"
        text += "       <td>1</td>"
        text += "       <td>Set tool color to color 1</td>"
        text += "   </tr>"
        text += "   <tr>"
        text += "       <td>2</td>"
        text += "       <td>Set tool color to color 2</td>"
        text += "   </tr>"
        text += "   <tr>"
        text += "       <td>3</td>"
        text += "       <td>Set tool color to color 3</td>"
        text += "   </tr>"
        text += "   <tr>"
        text += "       <td>4</td>"
        text += "       <td>Set tool color to color 4</td>"
        text += "   </tr>"
        text += "   <tr>"
        text += "       <td>5</td>"
        text += "       <td>Set tool color to color 5</td>"
        text += "   </tr>"
        text += "   <tr>"
        text += "       <td>W</td>"
        text += "       <td>Set mode to Write Mode</td>"
        text += "   </tr>"
        text += "   <tr>"
        text += "       <td>E</td>"
        text += "       <td>Set mode to Ellipse Mode. Resets to Write Mode after next draw operation.</td>"
        text += "   </tr>"
        text += "   <tr>"
        text += "       <td>R</td>"
        text += "       <td>Set mode to Rectangle Mode. Resets to Write Mode after next draw operation.</td>"
        text += "   </tr>"
        text += "   <tr>"
        text += "       <td>+</td>"
        text += "       <td>Increase line width</td>"
        text += "   </tr>"
        text += "   <tr>"
        text += "       <td>-</td>"
        text += "       <td>Decrease line width</td>"
        text += "   </tr>"
        text += "</table>"
        text += "</div>"

        text += "<h2>Write Mode</h2>\n"
        text += "<p>Write Mode is the default drawing mode. It allows the user to draw freehand. The hotkeys below allow the user to engage the different options for this mode. Not all options are available for all tools.</p>\n"
        text += "<div style=\"margin-left: auto;\">"
        text += "<table>"
        text += "   <tr>"
        text += "       <th align=\"left\">Hotkey</th>"
        text += "       <th align=\"left\">Function</th>"
        text += "   </tr>"
        text += "   <tr>"
        text += "       <td>Shift</td>"
        text += "       <td>Draw a straight line. Shift key must be held at start of draw operation.</td>"
        text += "   </tr>"
        text += "   <tr>"
        text += "       <td>{}</td>".format(QKeySequence(Qt.CTRL | Qt.Key_Shift).toString())
        text += "       <td>Draw a straight line snapped to the nearest 15°. Shift key must be held at start of draw operation.</td>"
        text += "   </tr>"
        text += "   <tr>"
        text += "       <td>Alt</td>"
        text += "       <td>Use alternate line style. Alt key must be held at start of draw operation.</td>"
        text += "   </tr>"
        text += "</table>"
        text += "</div>"

        text += "<h2>Write Mode</h2>\n"
        text += "<p>Write Mode is the default drawing mode. It allows the user to draw freehand. The hotkeys below allow the user to engage the different options for this mode. Not all options are available for all tools.</p>\n"
        text += "<div style=\"margin-left: auto;\">"
        text += "<table>"
        text += "   <tr>"
        text += "       <th align=\"left\">Hotkey</th>"
        text += "       <th align=\"left\">Function</th>"
        text += "   </tr>"
        text += "   <tr>"
        text += "       <td>Shift</td>"
        text += "       <td>Draw a straight line. Shift key must be held at start of draw operation.</td>"
        text += "   </tr>"
        text += "   <tr>"
        text += "       <td>{}</td>".format(QKeySequence(Qt.CTRL | Qt.Key_Shift).toString())
        text += "       <td>Draw a straight line snapped to the nearest 15°. Shift key must be held at start of draw operation.</td>"
        text += "   </tr>"
        text += "   <tr>"
        text += "       <td>Alt</td>"
        text += "       <td>Use alternate line style. Alt key must be held at start of draw operation.</td>"
        text += "   </tr>"
        text += "</table>"
        text += "</div>"

        text += "<h2>Ellipse Mode</h2>\n"
        text += "<p>Ellipse Mode allows the user to draw ellipses and circles. The hotkeys below allow the user to engage the different options for this mode. Not all options are available for all tools. After a single draw operation, the tool will reset to Write Mode.</p>\n"
        text += "<div style=\"margin-left: auto;\">"
        text += "<table>"
        text += "   <tr>"
        text += "       <th align=\"left\">Hotkey</th>"
        text += "       <th align=\"left\">Function</th>"
        text += "   </tr>"
        text += "   <tr>"
        text += "       <td>Shift</td>"
        text += "       <td>Draws a circle</td>"
        text += "   </tr>"
        text += "   <tr>"
        text += "       <td>{}</td>".format(QKeySequence(Qt.Key_Control).toString())
        text += "       <td>Expand the ellipse/circle from the center</td>"
        text += "   </tr>"
        text += "   <tr>"
        text += "       <td>Alt</td>"
        text += "       <td>Use alternate line style. Alt key must be held at start of draw operation.</td>"
        text += "   </tr>"
        text += "</table>"
        text += "</div>"

        text += "<h2>Rectangle Mode</h2>\n"
        text += "<p>Rectangle Mode allows the user to draw rectangles and squares. The hotkeys below allow the user to engage the different options for this mode. Not all options are available for all tools. After a single draw operation, the tool will reset to Write Mode.</p>\n"
        text += "<div style=\"margin-left: auto;\">"
        text += "<table>"
        text += "   <tr>"
        text += "       <th align=\"left\">Hotkey</th>"
        text += "       <th align=\"left\">Function</th>"
        text += "   </tr>"
        text += "   <tr>"
        text += "       <td>Shift</td>"
        text += "       <td>Draws a square</td>"
        text += "   </tr>"
        text += "   <tr>"
        text += "       <td>{}</td>".format(QKeySequence(Qt.Key_Control).toString())
        text += "       <td>Expand the rectangle/square from the center</td>"
        text += "   </tr>"
        text += "   <tr>"
        text += "       <td>Alt</td>"
        text += "       <td>Use alternate line style. Alt key must be held at start of draw operation.</td>"
        text += "   </tr>"
        text += "</table>"
        text += "</div>"

        textEdit.setHtml(text)

        layout = QVBoxLayout(self)
        layout.addWidget(textEdit)
