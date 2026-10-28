"""Interface tkinter verticale pour MAEL Scan (360 × 640, fixe)."""
from __future__ import annotations

import logging
import queue
import threading
from pathlib import Path
from typing import Any


class MaelController:
    """Logique indépendante de la vue; `scan_service` suit l'API MaelScan."""

    def __init__(self, scan_service: Any) -> None:
        self.scan_service = scan_service
        self.last_setup = None

    @property
    def can_repeat(self) -> bool:
        return self.last_setup is not None

    def on_scan(self) -> str:
        self.scan_service.scan()
        self.last_setup = getattr(self.scan_service, "last_tts_setup", None)
        if self.last_setup is None:
            return "Aucun texte à lire pour ce scan."
        return self.last_setup.to_show

    def on_repeat(self, slow: bool = False) -> None:
        if self.last_setup is None:
            return
        self.scan_service.repeat(slow=slow)


class MaelGui:
    """Fenêtre verticale simulant un téléphone, avec ressources PNG facultatives."""

    WIDTH = 360
    HEIGHT = 640
    BLUE = "#238ffe"
    ASSETS = Path(__file__).resolve().parent / "mael_scan_assets"

    def __init__(self, controller: MaelController, root: Any | None = None) -> None:
        import tkinter as tk

        self.tk = tk
        self.root = root or tk.Tk()
        self.controller = controller
        self._events: queue.Queue[tuple[str, Any]] = queue.Queue()
        self._busy = False
        self._images: dict[str, Any] = {}

        self.root.title("MAEL Scan")
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.root.resizable(False, False)
        self.root.configure(bg="white")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=0)

        self._build_header()
        self._build_body()
        self._build_footer()
        self.root.after(80, self._poll_events)

    def _load_image(self, filename: str, *, qr_limit: bool = False) -> Any | None:
        path = self.ASSETS / filename
        try:
            image = self.tk.PhotoImage(file=str(path))
            if qr_limit and image.width() > 32:
                divisor = max(1, (image.width() + 31) // 32)
                image = image.subsample(divisor, divisor)
            self._images[filename] = image
            return image
        except Exception as exc:
            logging.warning("Image MAEL indisponible (%s) : %s", path, exc)
            return None

    def _build_header(self) -> None:
        tk = self.tk
        header = tk.Frame(self.root, bg=self.BLUE, height=38, highlightthickness=0)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)
        # Keep the side controls at their requested widths; let the title take the remaining space.
        header.grid_columnconfigure(0, weight=0)
        header.grid_columnconfigure(1, weight=1)
        header.grid_columnconfigure(2, weight=0)
        header.grid_rowconfigure(0, weight=1)
        left = tk.Frame(header, bg=self.BLUE, bd=0, highlightthickness=0)
        left.grid(row=0, column=0, sticky="w", padx=2, pady=3)
        language = self._load_image("langues_32px.png")
        if language:
            tk.Label(left, image=language, bg=self.BLUE, bd=0).pack(side="left")
        title = tk.Label(header, text="MAEL Scan", bg=self.BLUE, fg="white",
                         font=("Arial", 18, "bold"), bd=0)
        title.grid(row=0, column=1, sticky="nsew")
        right = tk.Frame(header, bg=self.BLUE, bd=0, highlightthickness=0)
        right.grid(row=0, column=2, sticky="e", padx=2, pady=3)
        tk.Label(right, text="V 6.0", bg=self.BLUE, fg="white",
                 font=("Arial", 8), bd=0).pack(side="left", padx=(0, 2))
        qr = self._load_image("qr-scan-svgrepo-com.png", qr_limit=True)
        if qr:
            tk.Label(right, image=qr, bg=self.BLUE, bd=0).pack(side="left")

    def _build_body(self) -> None:
        tk = self.tk
        body = tk.Frame(self.root, bg="white", bd=0, highlightthickness=0)
        body.grid(row=1, column=0, sticky="nsew", padx=12, pady=(5, 7))
        body.grid_columnconfigure(0, weight=1)
        # Contenu en haut, puis zone centrale répartie équitablement entre les actions.
        body.grid_rowconfigure(0, weight=0)
        for row in (1, 2, 3):
            body.grid_rowconfigure(row, weight=1, uniform="actions")

        self.text = tk.Text(body, wrap="word", height=5, state="disabled",
                            bg="white", fg="black", font=("Arial", 18),
                            relief="flat", borderwidth=0, highlightthickness=1,
                            highlightbackground="#a0a0a0", highlightcolor="#a0a0a0",
                            padx=8, pady=6)
        self.text.grid(row=0, column=0, sticky="ew", pady=(0, 5))

        self.scan_button = self._make_button(body, "Scanner.png", "Scanner", self._start_scan, 1)
        self.repeat_button = self._make_button(
            body, "Reecouter.png", "Répéter", lambda: self._start_repeat(False), 2,
            state="disabled")
        self.slow_button = self._make_button(
            body, "Lent.png", "Répéter lentement", lambda: self._start_repeat(True), 3,
            state="disabled")

    def _make_button(self, parent: Any, filename: str, label: str, command: Any,
                     row: int, state: str = "normal") -> Any:
        image = self._load_image(filename)
        options = dict(command=command, state=state, bg="white", activebackground="white",
                       disabledforeground="#999999", relief="flat", borderwidth=0,
                       highlightthickness=0, bd=0, padx=0, pady=0, takefocus=0)
        if image is not None:
            options["image"] = image
        else:
            options.update(text=label, font=("Arial", 13))
        button = self.tk.Button(parent, **options)
        button.grid(row=row, column=0, sticky="nsew", pady=3)
        return button

    def _build_footer(self) -> None:
        tk = self.tk
        footer = tk.Frame(self.root, bg="white", height=38, bd=0, highlightthickness=0)
        footer.grid(row=2, column=0, sticky="ew")
        footer.grid_propagate(False)
        centered = tk.Frame(footer, bg="white", bd=0, highlightthickness=0)
        centered.place(relx=0.5, rely=0.5, anchor="center")
        logo = self._load_image("logo_lvh_32px.png")
        if logo:
            tk.Label(centered, image=logo, bg="white", bd=0).pack(side="left", padx=(0, 5))
        tk.Label(centered, text="Auteur : Yonnel Bécognée - Licence GNU GPL V3",
                 bg="white", fg="black", font=("Arial", 8), bd=0).pack(side="left")

    def _show_text(self, message: str) -> None:
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.insert("1.0", message)
        self.text.configure(state="disabled")
        self._resize_text_to_content()

    def _resize_text_to_content(self) -> None:
        # Tk compte les lignes d'affichage après application du wrap réel du widget.
        self.text.update_idletasks()
        try:
            counted = self.text.count("1.0", "end-1c", "displaylines")
            lines = counted[0] if counted else 1
        except (self.tk.TclError, TypeError):
            lines = max(1, self.text.get("1.0", "end-1c").count("\n") + 1)
        self.text.configure(height=max(5, lines))
        self.text.master.update_idletasks()

    def _set_busy(self, busy: bool) -> None:
        self._busy = busy
        self.scan_button.configure(state="disabled" if busy else "normal")
        repeat_state = "normal" if self.controller.can_repeat and not busy else "disabled"
        self.repeat_button.configure(state=repeat_state)
        self.slow_button.configure(state=repeat_state)

    def _start_scan(self) -> None:
        if self._busy:
            return
        self._set_busy(True)
        self._show_text("Lecture du code QR…")
        self._run_background("scan", self.controller.on_scan)

    def _start_repeat(self, slow: bool) -> None:
        if self._busy or not self.controller.can_repeat:
            return
        self._set_busy(True)
        self._run_background("repeat", lambda: self.controller.on_repeat(slow))

    def _run_background(self, kind: str, action: Any) -> None:
        def work() -> None:
            try:
                self._events.put((kind, action()))
            except Exception as exc:
                self._events.put(("error", f"Erreur : {exc}"))
        threading.Thread(target=work, name=f"MAEL-{kind}", daemon=True).start()

    def _poll_events(self) -> None:
        try:
            while True:
                kind, value = self._events.get_nowait()
                if kind in {"scan", "error"}:
                    self._show_text(value)
                self._set_busy(False)
        except queue.Empty:
            pass
        self.root.after(80, self._poll_events)

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    from mael_scan import MaelScan
    from tts_player_gtts import GttsPlayer

    MaelGui(MaelController(MaelScan(tts_player=GttsPlayer()))).run()


if __name__ == "__main__":
    main()
