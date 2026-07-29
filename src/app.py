import streamlit as st
from streamlit_folium import st_folium

from clustering import cluster_parks
from config.parks import NATIONAL_PARKS
from map_builder import build_clustered_map, build_raw_map

_PAGE_TITLE = "US National Parks"
_MAP_HEIGHT = 800

_CSS = """
    <style>
        .block-container { padding-top: 0.5rem !important; }
    </style>
"""

_MODE_RAW = "Malhar"
_MODE_CLUSTER = "HDBSCAN"


def _configure_page() -> None:
    st.set_page_config(
        page_title=_PAGE_TITLE,
        page_icon="🏕️",
        layout="wide",
    )
    st.markdown(_CSS, unsafe_allow_html=True)


def _render_header() -> None:
    st.title(_PAGE_TITLE)
    st.caption(f"{len(NATIONAL_PARKS)} national parks — click a pin to learn more.")


def _render_mode_selector() -> str:
    return st.radio("View", [_MODE_RAW, _MODE_CLUSTER], horizontal=True, label_visibility="collapsed")


def _render_map(mode: str) -> None:
    if mode == _MODE_CLUSTER:
        park_colors = cluster_parks()
        parks_map = build_clustered_map(park_colors)
    else:
        parks_map = build_raw_map()
    st_folium(parks_map, use_container_width=True, height=_MAP_HEIGHT, returned_objects=[])


def main() -> None:
    _configure_page()
    _render_header()
    mode = _render_mode_selector()
    _render_map(mode)


if __name__ == "__main__":
    main()
