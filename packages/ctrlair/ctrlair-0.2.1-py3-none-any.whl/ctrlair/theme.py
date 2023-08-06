from functools import partial
from typing import Callable, Dict, List, Union

import altair as alt  # type: ignore

from .utils import print_dict

COLORS: Dict[str, str] = {
    "white": "#FFFFFF",
    "light_gray": "#EBEBEB",
    "black": "#44475A",
}
LOCALE: Dict[str, Union[str, List[int], List[str]]] = {
    "decimal": ".",
    "thousands": ",",
    "grouping": [3],
    "currency": ["", "€"],
}
I18N_EN: Dict[str, str] = {"PNG_ACTION": "Save as PNG", "SVG_ACTION": "Save as SVG"}
I18N_PT_PT: Dict[str, str] = {
    "PNG_ACTION": "Guardar como PNG",
    "SVG_ACTION": "Guardar como SVG",
    "EDITOR_ACTION": "Abrir no Vega Editor",
}


def lcontrast_theme_tooltip() -> None:
    from IPython.display import HTML, display  # type: ignore

    # More info: https://github.com/vega/vega-tooltip/blob/master/vega-tooltip.scss
    display(
        HTML(
            f"""
            <style>
                #vg-tooltip-element.vg-tooltip.lcontrast-theme {{
                    color: {COLORS["black"]};
                    border: 1px solid {COLORS["light_gray"]};
                    font-family: Roboto;
                    font-size: 11px;
                }}
                #vg-tooltip-element.vg-tooltip.lcontrast-theme td.key {{
                    color: {COLORS["black"]};
                    font-weight: bold;
                }}
            </style>
            """
        )
    )


def lcontrast_theme(width: int, height: int) -> Dict[str, Dict[str, object]]:
    font = "Roboto"

    return {
        "config": {
            "title": {"font": font, "color": COLORS["black"]},
            "axisX": {
                "labelFont": font,
                "titleFont": font,
                "gridColor": COLORS["light_gray"],
                "labelColor": COLORS["black"],
                "tickColor": COLORS["black"],
                "titleColor": COLORS["black"],
                "domainColor": COLORS["black"],
                "labelAngle": 0,
                "titleBaseline": "top",
            },
            "axisY": {
                "labelFont": font,
                "titleFont": font,
                "gridColor": COLORS["light_gray"],
                "labelColor": COLORS["black"],
                "tickColor": COLORS["black"],
                "titleColor": COLORS["black"],
                "domainColor": COLORS["black"],
                "titleAngle": 0,
                "titleAlign": "left",
                "titleY": -5,
                "titleX": 0,
                "titleBaseline": "bottom",
            },
            "header": {
                "labelFont": font,
                "titleFont": font,
                "labelColor": COLORS["black"],
                "titleColor": COLORS["black"],
            },
            "legend": {
                "labelFont": font,
                "titleFont": font,
                "labelColor": COLORS["black"],
                "titleColor": COLORS["black"],
            },
            "text": {"font": font, "color": COLORS["black"]},
            "rule": {"color": COLORS["black"]},
            "background": COLORS["white"],
            "view": {
                "fill": COLORS["white"],
                "stroke": COLORS["light_gray"],
                "strokeWidth": 1,
                "height": height,
                "width": width,
            },
        }
    }


THEMES: Dict[str, Callable[[int, int], Dict[str, Dict[str, object]]]] = {
    "lcontrast": lcontrast_theme
}
DEFAULT_TOOLTIP_THEMES: Dict[str, str] = {
    "light": "light",
    "dark": "dark",
}
TOOLTIP_THEMES: Dict[str, Callable] = {"lcontrast": lcontrast_theme_tooltip}


def set_alt_tooltip_theme(tooltip_theme_name: str) -> str:
    if tooltip_theme_name in TOOLTIP_THEMES:
        TOOLTIP_THEMES[tooltip_theme_name]()
        return tooltip_theme_name
    elif tooltip_theme_name in DEFAULT_TOOLTIP_THEMES:
        return tooltip_theme_name
    else:
        raise Exception(
            f"The {repr(tooltip_theme_name)} tooltip theme is not available."
        )


def set_button_lang(button_lang: str) -> Dict[str, str]:
    if button_lang.lower() == "en":
        return I18N_EN
    elif button_lang.lower() == "pt-pt":
        return I18N_PT_PT
    else:
        raise Exception(f"The {repr(button_lang)} language/locale is not available.")


def set_alt_aesthetic(
    theme_name: str = "lcontrast",
    tooltip_theme_name: str = "lcontrast",
    disable_max_rows: bool = False,
    renderer: str = "svg",
    show_button: bool = True,
    button_lang: str = "en",
    width: int = 300,
    height: int = 300,
) -> None:
    if theme_name in THEMES or theme_name in get_alt_themes(verbose=False):
        tooltip_theme = set_alt_tooltip_theme(tooltip_theme_name)

        # More info: https://github.com/vega/vega-embed
        alt.renderers.enable(
            "default",
            embed_options={
                "actions": {
                    "export": True,
                    "source": False,
                    "compiled": False,
                    "editor": True,
                }
                if show_button
                else False,
                "scaleFactor": 5,
                "i18n": set_button_lang(button_lang),
                "tooltip": {"theme": tooltip_theme},
                "renderer": renderer,
                "formatLocale": LOCALE,
                "downloadFileName": "chart",
            },
        )

        # More info: https://github.com/altair-viz/altair/blob/master/altair/utils/plugin_registry.py
        if theme_name in THEMES:
            alt.themes.register(
                theme_name, partial(THEMES[theme_name], width=width, height=height)
            )
        alt.themes.enable(theme_name)

        if disable_max_rows:
            alt.data_transformers.disable_max_rows()
    else:
        raise Exception(f"The {repr(theme_name)} theme is not available.")


def set_default_alt_aesthetic() -> None:
    alt.themes.enable("default")


def get_alt_themes(verbose: bool = True) -> List[str]:
    if verbose:
        print(f"{repr(alt.themes.active)} is the current Altair theme.")
    return alt.themes.names()


def get_alt_aesthetic() -> None:
    print_dict(alt.themes.get()())
