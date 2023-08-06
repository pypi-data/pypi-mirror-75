
import ngsgui.gui as G
import pytest, os

@pytest.fixture
def gui(qtbot):
    G.gui = gui = G.GUI(startApplication=False, flags=[])
    return gui

def test_loadPython(gui, qtbot, tmpdir):
    f = tmpdir.join("small.py")
    f.write("a=5")
    gui.loadPythonFile(str(f))
    qtbot.wait(10)
    callback_called = []
    def callback(msg):
        callback_called.append(True)
        assert msg['data']['text/plain'] == '5'
    gui.console._silent_exec_callback("a", callback)
    qtbot.wait(10)
    assert callback_called

def test_exception_in_console(gui, qtbot):
    # raise an exception
    gui.console.execute("asdf")
    callback_called = []
    # console should still work
    def callback(msg):
        callback_called.append(True)
        assert msg['data']['text/plain'] == '5'
    gui.console._silent_exec_callback("5", callback)
    qtbot.wait(10)
    assert callback_called
