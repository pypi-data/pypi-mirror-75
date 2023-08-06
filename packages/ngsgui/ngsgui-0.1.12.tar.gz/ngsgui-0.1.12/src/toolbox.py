
from .widgets import ArrangeH, ArrangeV
from qtpy import QtWidgets, QtCore, QtGui
from ngsgui.icons import location as icon_path
import weakref

class ToolBoxItem(QtWidgets.QWidget):
    changeExpand = QtCore.Signal()
    removeSignal = QtCore.Signal()
    class Header(QtWidgets.QWidget):
        class Icon(QtWidgets.QToolButton):
            """List of icons to be changed by toggling signal"""
            def __init__(self, icons, signal = None, tooltip = None, **kwargs):
                super().__init__(**kwargs)
                if not isinstance(icons, list):
                    assert isinstance(icons, str)
                    self._lst = [icons]
                else:
                    assert all((isinstance(icon, str) for icon in icons))
                    self._lst = icons
                self._active = 0
                if signal:
                    self.clicked.connect(signal.emit)
                    signal.connect(self.next)
                self.setIcon(QtGui.QIcon(self._lst[0]))
                self.setIconSize(QtCore.QSize(2*12,2*12))
                self.setAutoRaise(True)
                if tooltip:
                    self.setToolTip(tooltip)

            def next(self):
                self._active = (self._active + 1)%len(self._lst)
                self.setIcon(QtGui.QIcon(self._lst[self._active]))

        def __init__(self, text, *args, **kwargs):
            super().__init__(*args,**kwargs)
            self._leftIcons = []
            self._rightIcons = []
            self._text = QtWidgets.QPushButton(text)
            self._text.setStyleSheet("QPushButton:flat { border:none; Text-align:left; }")
            self._text.setFlat(True)

        def updateLayout(self):
            if self.layout():
                wid = QtWidgets.QWidget()
                wid.setLayout(self.layout())
            self.setLayout(ArrangeH(*self._leftIcons, self._text, *reversed(self._rightIcons)))
            self.layout().setContentsMargins(0,0,0,0)

        def addIcon(self, images, action=None, tooltip=None, left=False):
            """Adds icon to header, if icon is list of icons then each time action is clicked, the icon
changes to the next one in the list. For that, action must be a QtCore.Signal

Parameters
----------

images: str or list of str
  Path to icon or list of paths

action: QtCore.Signal=None
  Signal to be emitted when icon is clicked

tooltip: str
  Tooltip for mouse hover"""
            if left:
                self._leftIcons.append(ToolBoxItem.Header.Icon(images, signal=action, tooltip=tooltip))
            else:
                self._rightIcons.append(ToolBoxItem.Header.Icon(images, signal=action, tooltip=tooltip))

    class Body(QtWidgets.QWidget):
        def __init__(self, *args,**kwargs):
            super().__init__(*args,**kwargs)

    def __init__(self, name, killButton=True, endLine = True, **kwargs):
        super().__init__(**kwargs)
        self.header = ToolBoxItem.Header(name)
        self.header._text.clicked.connect(self.changeExpand.emit)
        self.header.addIcon([icon_path + "/next.png", icon_path + "/down-arrow.png"], self.changeExpand,
                            "Expand menu", left=True)
        self.changeExpand.connect(self._changeExpand)
        if killButton:
            self.header.addIcon([icon_path + "/kill.png"], self.removeSignal, "Remove Scene")
            self.removeSignal.connect(self._removeItem)
        self.body = ToolBoxItem.Body()
        self.body.setVisible(False)
        widgets = [self.header, self.body]
        if endLine:
            line = QtWidgets.QFrame()
            line.setFrameShape(line.HLine)
            pal = line.palette()
            line.setPalette(pal)
            widgets.append(line)
        self.setLayout(ArrangeV(*widgets))
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setAlignment(QtCore.Qt.AlignTop)
        self.header.updateLayout()

    def _changeExpand(self):
        self.body.setVisible(not self.body.isVisible())

class SceneToolBoxItem(ToolBoxItem):
    def __init__(self, scene, visibilityButton=True, colorButton=True, clippingPlaneButton=True,
                 lightButton=True, **kwargs):
        super().__init__(scene.name, **kwargs)
        if visibilityButton:
            self.header.addIcon([icon_path + "/visible.png", icon_path + "/hidden.png"], scene.activeChanged,
                                "Show/Hide scene")
        if colorButton:
            self.header.addIcon([icon_path + "/globalColor.png", icon_path + "/color.png"],
                                scene.individualColormapChanged,
                                "Use individual colormap")
        if clippingPlaneButton:
            icons = [icon_path + "/noscissors.png", icon_path + "/scissors.png"]
            if scene._individual_rendering_parameters:
                icons = [icon_path + "/globalScissors.png"] + list(reversed(icons))
            description = "Use global/local/no clipping plane(s)" if scene._individual_rendering_parameters else "Ebnable/disable global clipping plane"
            self.header.addIcon(icons, scene.individualClippingPlaneChanged, description)
        if lightButton:
            icons = [icon_path + "/light.png", icon_path + "/nolight.png"]
            if scene._individual_rendering_parameters:
                icons = [icon_path + "/globalLight.png"] + icons
            description = "Use global/local/no light settings" if scene._individual_rendering_parameters else "Use light"
            self.header.addIcon(icons, scene.individualLightChanged, description)
        self.header.updateLayout()
        self.body.setLayout(ArrangeV(*scene.widgets.groups))
        scene.widgets.setParent(self.body)
        self.body.layout().setContentsMargins(0,0,0,0)
        self.body.layout().setAlignment(QtCore.Qt.AlignTop)
        scene.widgets.update()
        self._scene = weakref.ref(scene)

    def _removeItem(self):
        self._scene().window().remove(self._scene())

class ToolBox(QtWidgets.QDockWidget):
    """Our own toolbox class, because the Qt one doesn't support the stuff we want"""
    def __init__(self, title="", **kwargs):
        super().__init__(title,**kwargs)
        self._widget = QtWidgets.QWidget()
        self._widget.setLayout(ArrangeV())
        self._widget.layout().setContentsMargins(0,0,0,0)
        self._widget.layout().setAlignment(QtCore.Qt.AlignTop)
        self.setWidget(self._widget)

    def addWidget(self, widget):
        self._widget.layout().addWidget(widget)

class SceneToolBox(ToolBox):
    def __init__(self, glWidget, **kwargs):
        super().__init__(title="Scene Toolbox")
        scrollarea = QtWidgets.QScrollArea()
        scrollarea.setWidgetResizable(True)
        self.sceneWidget = sceneWidget = QtWidgets.QWidget()
        sceneWidget.setLayout(ArrangeV())
        sceneWidget.layout().setAlignment(QtCore.Qt.AlignTop)
        sceneWidget.layout().setContentsMargins(0,0,0,0)
        scrollarea.setWidget(sceneWidget)
        self.addWidget(scrollarea)
        btnZoomReset = QtWidgets.QPushButton("ZoomReset", self)
        btnZoomReset.clicked.connect(glWidget.ZoomReset)
        btnZoomReset.setMinimumWidth(1);
        self.addWidget(btnZoomReset)

    def addScene(self, scene, **kwargs):
        widget = self.widget().layout().itemAt(0).widget().takeWidget()
        widget.layout().addWidget(SceneToolBoxItem(scene,**kwargs))
        self.widget().layout().itemAt(0).widget().setWidget(widget)

    def removeScene(self, scene):
        widgets = self.widget().layout().itemAt(0).widget().widget()
        for i in range(widgets.layout().count()):
            item = widgets.layout().itemAt(i)
            widget = item.widget()
            if hasattr(widget, "_scene") and (widget._scene() == scene):
                new_layout = ArrangeV(*[widgets.layout().itemAt(j).widget() for j in range(widgets.layout().count()) if i!=j])
                tmpwidget = QtWidgets.QWidget()
                tmpwidget.setLayout(widgets.layout())
                widgets.setLayout(new_layout)
                widgets.layout().setContentsMargins(0,0,0,0)
                widgets.layout().setAlignment(QtCore.Qt.AlignTop)
                break
        else:
            print("widget not found")
