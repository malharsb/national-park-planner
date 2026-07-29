import folium

from config.airports import MAJOR_AIRPORTS, Airport
from config.parks import NATIONAL_PARKS, NationalPark
from config.visited import MALHAR_VISITED

_USA_CENTER = [39.5, -98.35]
_DEFAULT_ZOOM = 4

_PARK_COLOR = "#e74c3c"
_PARK_VISITED_COLOR = "#2ecc71"
_AIRPORT_COLOR = "#3498db"
_PIN_SIZE = 8


def _build_park_popup(park: NationalPark) -> folium.Popup:
    html = f"""
        <div style="font-family: sans-serif; min-width: 150px;">
            <b style="font-size: 14px;">{park.name}</b><br>
            <span style="color: #555;">{park.state}</span>
        </div>
    """
    return folium.Popup(html, max_width=200)


def _build_airport_popup(airport: Airport) -> folium.Popup:
    html = f"""
        <div style="font-family: sans-serif; min-width: 150px;">
            <b style="font-size: 14px;">{airport.code}</b><br>
            <span style="color: #555;">{airport.name}</span><br>
            <span style="color: #555;">{airport.state}</span>
        </div>
    """
    return folium.Popup(html, max_width=220)


def _make_dot_icon(color: str) -> folium.DivIcon:
    half = _PIN_SIZE // 2
    return folium.DivIcon(
        html=f'<div style="width:{_PIN_SIZE}px;height:{_PIN_SIZE}px;background:{color};border-radius:50%;"></div>',
        icon_size=(_PIN_SIZE, _PIN_SIZE),
        icon_anchor=(half, half),
    )


def _make_plane_icon() -> folium.DivIcon:
    size = (_PIN_SIZE + 4) * 2
    return folium.DivIcon(
        html=f'<div style="font-size:{size}px;color:{_AIRPORT_COLOR};line-height:1;">✈</div>',
        icon_size=(size, size),
        icon_anchor=(size // 2, size // 2),
    )


def _add_airport_marker(map_: folium.Map, airport: Airport) -> None:
    folium.Marker(
        location=[airport.lat, airport.lon],
        popup=_build_airport_popup(airport),
        tooltip=f"{airport.code} — {airport.name}",
        icon=_make_plane_icon(),
    ).add_to(map_)


def _base_map() -> folium.Map:
    return folium.Map(location=_USA_CENTER, zoom_start=_DEFAULT_ZOOM, tiles="CartoDB dark_matter")


def build_raw_map() -> folium.Map:
    parks_map = _base_map()
    for park in NATIONAL_PARKS:
        color = _PARK_VISITED_COLOR if park.name in MALHAR_VISITED else _PARK_COLOR
        folium.Marker(
            location=[park.lat, park.lon],
            popup=_build_park_popup(park),
            tooltip=park.name,
            icon=_make_dot_icon(color),
        ).add_to(parks_map)
    for airport in MAJOR_AIRPORTS:
        _add_airport_marker(parks_map, airport)
    return parks_map


def build_clustered_map(park_colors: dict[str, str]) -> folium.Map:
    parks_map = _base_map()
    for park in NATIONAL_PARKS:
        color = park_colors.get(park.name, "#aaaaaa")
        folium.Marker(
            location=[park.lat, park.lon],
            popup=_build_park_popup(park),
            tooltip=park.name,
            icon=_make_dot_icon(color),
        ).add_to(parks_map)
    for airport in MAJOR_AIRPORTS:
        _add_airport_marker(parks_map, airport)
    return parks_map
