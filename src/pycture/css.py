ULTRA_DARK_GRAY = "rgb(14, 16, 17)"
DARK_GRAY = "rgb(24, 26, 27)"
MEDIUM_GRAY = "rgb(36, 38, 40)"
LIGHT_GRAY = "rgb(45, 48, 49)"
DARK_WHITE = "rgb(200, 195, 188)"

PYCTURE_CSS = f"""
* {{
    color: {DARK_WHITE};
    background: {DARK_GRAY};
}}

QMainWindow::separator {{
    background: {MEDIUM_GRAY};
    width: 5; /* when vertical */
    height: 5; /* when horizontal */
}}

QMainWindow::separator:hover {{
    background: {LIGHT_GRAY};
}}

QMenuBar {{
    background: {ULTRA_DARK_GRAY};
}}

QMenuBar::item:selected, QMenu::item::selected {{
    background: {MEDIUM_GRAY};
}}

QMenuBar::item:pressed, QMenu::item::pressed {{
    background: {LIGHT_GRAY};
}}

QScrollArea {{
    border: 0px;
}}
"""
