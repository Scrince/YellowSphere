                                                                      

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Optional
from importlib import resources

from .core import APP_VERSION


JSPDF_CDN_URL = "https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"
_PACKAGED_ASSET_CONTEXTS = []


def find_html_app() -> Path:
    candidates = [
        Path.cwd() / "YellowSphere.html",
        Path(__file__).resolve().parents[2] / "YellowSphere.html",
        Path(sys.argv[0]).resolve().parent / "YellowSphere.html",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    packaged = resources.files("yellowsphere.assets").joinpath("YellowSphere.html")
    if packaged.is_file():
        context = resources.as_file(packaged)
        asset_path = context.__enter__()
        _PACKAGED_ASSET_CONTEXTS.append(context)
        return asset_path
    raise FileNotFoundError("YellowSphere.html was not found next to the launcher, in the current directory, or in packaged assets.")


def find_vendored_jspdf() -> Optional[Path]:
    candidates = [
        Path.cwd() / "vendor" / "jspdf" / "jspdf.umd.min.js",
        Path(__file__).resolve().parents[2] / "vendor" / "jspdf" / "jspdf.umd.min.js",
        Path(sys.argv[0]).resolve().parent / "vendor" / "jspdf" / "jspdf.umd.min.js",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    packaged = resources.files("yellowsphere.assets").joinpath("jspdf.umd.min.js")
    if packaged.is_file():
        context = resources.as_file(packaged)
        asset_path = context.__enter__()
        _PACKAGED_ASSET_CONTEXTS.append(context)
        return asset_path
    return None


def find_packaged_asset(name: str) -> Optional[Path]:
    candidates = [
        Path.cwd() / name,
        Path(__file__).resolve().parents[2] / name,
        Path(sys.argv[0]).resolve().parent / name,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    packaged = resources.files("yellowsphere.assets").joinpath(name)
    if packaged.is_file():
        context = resources.as_file(packaged)
        asset_path = context.__enter__()
        _PACKAGED_ASSET_CONTEXTS.append(context)
        return asset_path
    return None


def launch_gui() -> None:
    try:
        from PySide6.QtCore import QUrl
        from PySide6.QtGui import QIcon
        from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow
        from PySide6.QtWebEngineCore import QWebEngineScript, QWebEngineUrlRequestInterceptor
        from PySide6.QtWebEngineWidgets import QWebEngineView
    except ImportError as exc:
        raise RuntimeError(
            "PySide6 with Qt WebEngine is required for GUI mode. Install it with "
            "`python -m pip install -r requirements.txt` from the repo, or `python -m pip install \".[gui]\"` for package installs."
        ) from exc

    class OfflineAssetInterceptor(QWebEngineUrlRequestInterceptor):
        def __init__(self, jspdf_path: Path) -> None:
            super().__init__()
            self._jspdf_url = QUrl.fromLocalFile(str(jspdf_path))

        def interceptRequest(self, info) -> None:
            if info.requestUrl().toString().split("?", 1)[0] == JSPDF_CDN_URL:
                info.redirect(self._jspdf_url)

    os.environ.setdefault("QTWEBENGINE_DISABLE_SANDBOX", "1")

    app = QApplication.instance() or QApplication(sys.argv)
    icon_path = find_packaged_asset("favicon.png")
    if icon_path:
        app.setWindowIcon(QIcon(str(icon_path)))
    window = QMainWindow()
    window.setWindowTitle(f"YellowSphere v{APP_VERSION}")
    if icon_path:
        window.setWindowIcon(QIcon(str(icon_path)))
    window.resize(1180, 860)

    view = QWebEngineView(window)
    html_path = find_html_app()
    jspdf_path = find_vendored_jspdf()
    if jspdf_path:
        jspdf_script = QWebEngineScript()
        jspdf_script.setName("vendored-jsPDF")
        jspdf_script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentReady)
        jspdf_script.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)
        jspdf_script.setRunsOnSubFrames(False)
        jspdf_script.setSourceCode(jspdf_path.read_text(encoding="utf-8"))
        view.page().scripts().insert(jspdf_script)

        interceptor = OfflineAssetInterceptor(jspdf_path)
        view.page().profile().setUrlRequestInterceptor(interceptor)
        view.page().profile()._yellowsphere_offline_interceptor = interceptor
    view.setUrl(QUrl.fromLocalFile(str(html_path)))
    window.setCentralWidget(view)

    def choose_download_path(download) -> None:
        suggested = download.suggestedFileName() or "YellowSphere_export"
        is_pdf = Path(suggested).suffix.lower() == ".pdf"
        file_filter = "PDF Files (*.pdf);;All Files (*)" if is_pdf else "All Files (*)"
        target, _ = QFileDialog.getSaveFileName(window, "Save Export", suggested, file_filter)
        if not target:
            download.cancel()
            return
        target_path = Path(target)
        if is_pdf and target_path.suffix.lower() != ".pdf":
            target_path = target_path.with_suffix(".pdf")
        download.setDownloadDirectory(str(target_path.parent))
        download.setDownloadFileName(target_path.name)
        download.accept()

    view.page().profile().downloadRequested.connect(choose_download_path)
    window.show()
    app.exec()
