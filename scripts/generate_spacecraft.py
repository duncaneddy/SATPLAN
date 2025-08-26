import sys
import json
import numpy as np
import plotly.graph_objects as go
from dataclasses import dataclass
from loguru import logger

import brahe as bh
from satplan.constants import (
    NUM_SATELLITES,
    SATELLITE_ALTITUDE_KM,
    SATELLITE_ECCENTRICITY,
    SATELLITE_ARG_PERIGEE,
    SATELLITE_INCLINATIONS_DEG,
    WALKER_CONFIGURATIONS,
    EPOCH,
)
from satplan.utils import get_data_path

# Setup logging
logger.remove()
logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> <level>{message}</level>",
    level="DEBUG",
)


@dataclass
class OrbitalElements:
    """Osculating orbital elements in standard units"""

    sma: float  # Semi-major axis [km]
    ecc: float  # Eccentricity [dimensionless]
    inc: float  # Inclination [degrees]
    raan: float  # Right Ascension of Ascending Node [degrees]
    arg_perigee: float  # Argument of perigee [degrees]
    mean_anomaly: float  # Mean anomaly [degrees]


def generate_orbital_elements(
    inclination: float, total_sats: int, num_planes: int, relative_spacing: int
) -> list[tuple[int, OrbitalElements, str, str]]:
    """
    Generate Orbital elements for all satellites in a Walker constellation configuration.

    Arguments:
    - inclination: Inclination angle of the satellites [degrees]
    - total_sats: Total number of satellites (t)
    - num_planes: Number of orbital planes (p)
    - relative_spacing: Relative spacing parameter (f)

    Returns:
    - List of (sat_id, OrbitalElements, tle_line1, tle_line2) for each satellite
    """

    if total_sats % num_planes != 0:
        raise ValueError(
            "Total number of satellites must be divisible by the number of planes."
        )

    # Constants for Creation
    epoch = bh.Epoch(EPOCH)
    sma = SATELLITE_ALTITUDE_KM * 1e3 + bh.R_EARTH
    ecc = SATELLITE_ECCENTRICITY
    argp = SATELLITE_ARG_PERIGEE
    sats_per_plane = total_sats // num_planes

    # List of Spacecraft Elements
    elements = []
    sat_id = 1

    # RAAN spacing between planes [degrees]
    raan_spacing = 360.0 / num_planes

    # Mean anomaly spacing within each plane [degrees]
    ma_spacing = 360.0 / sats_per_plane

    # Phase offset between adjacent planes [degrees]
    phase_offset = relative_spacing * 360.0 / total_sats

    for plane_idx in range(num_planes):
        # RAAN for this plane
        raan = plane_idx * raan_spacing

        # Base mean anomaly offset for this plane
        base_ma_offset = plane_idx * phase_offset

        for sat_idx in range(sats_per_plane):
            # Mean anomaly for this satellite
            mean_anomaly = (sat_idx * ma_spacing + base_ma_offset) % 360.0

            orbital_element = OrbitalElements(
                sma=sma,
                ecc=ecc,
                inc=inclination,
                raan=raan,
                arg_perigee=argp,  # Standard for constellation orbits
                mean_anomaly=mean_anomaly,
            )

            # Create TLE from elements
            tle_line1, tle_line2 = bh.tle_string_from_elements(
                epoch,
                np.array(
                    [
                        bh.mean_motion(sma, use_degrees=True) * 86400 / 360,
                        # Convert sma into mean motion rev/day
                        ecc,
                        inclination,
                        raan,
                        argp,
                        mean_anomaly,
                        0.0,
                        0.0,
                        0.0,
                    ]
                ),
                norad_id=int(sat_id),
            )

            elements.append((sat_id, orbital_element, tle_line1, tle_line2))

    return elements


def plot_constellation_3d(
    elements: list[tuple[int, OrbitalElements, str, str]],
    inclination: float,
    total_sats: int,
    num_planes: int,
    relative_spacing: int,
    num_orbit_points: int = 100,
) -> go.Figure:
    """
    Plot the Walker constellation in 3D using plotly.

    Arguments:
    - elements: List of orbital elements for each satellite
    - inclination: Inclination angle of the satellites [degrees]
    - total_sats: Total number of satellites (t)
    - num_planes: Number of orbital planes (p)
    - relative_spacing: Relative spacing parameter (f)
    - num_orbit_points: Number of points per orbit for visualization

    Returns:
        Plotly 3D figure
    """
    fig = go.Figure()

    # Add Earth sphere
    u = np.linspace(0, 2 * np.pi, 50)
    v = np.linspace(0, np.pi, 50)
    x_earth = bh.R_EARTH / 1e3 * np.outer(np.cos(u), np.sin(v))
    y_earth = bh.R_EARTH / 1e3 * np.outer(np.sin(u), np.sin(v))
    z_earth = bh.R_EARTH / 1e3 * np.outer(np.ones(np.size(u)), np.cos(v))

    fig.add_trace(
        go.Surface(
            x=x_earth,
            y=y_earth,
            z=z_earth,
            colorscale=[[0, "lightblue"], [1, "lightblue"]],
            showscale=False,
            name="Earth",
            opacity=0.8,
        )
    )

    # Generate orbit traces for each satellite
    colors = [
        "red",
        "blue",
        "green",
        "orange",
        "purple",
        "brown",
        "pink",
        "gray",
        "olive",
        "cyan",
    ]
    sats_per_plane = total_sats // num_planes

    for sat_idx, element_data in enumerate(elements):
        element = element_data[1]

        plane_idx = sat_idx // sats_per_plane
        color = colors[plane_idx % len(colors)]

        # Generate mean anomaly values for complete orbit
        mean_anomalies = np.linspace(0, 360, num_orbit_points)

        orbit_x, orbit_y, orbit_z = [], [], []

        for ma in mean_anomalies:
            # Create temporary orbital elements with varying mean anomaly
            temp_elements = (
                element.sma,
                element.ecc,
                element.inc,
                element.raan,
                element.arg_perigee,
                ma,
            )

            x, y, z = bh.sOSCtoCART(temp_elements, use_degrees=True)[0:3] / 1e3
            orbit_x.append(x)
            orbit_y.append(y)
            orbit_z.append(z)

        # Add orbit trace
        fig.add_trace(
            go.Scatter3d(
                x=orbit_x,
                y=orbit_y,
                z=orbit_z,
                mode="lines",
                line=dict(color=color, width=3),
                name=f"Plane {plane_idx + 1}, Sat {sat_idx % sats_per_plane + 1}",
                showlegend=True,
            )
        )

        # Add satellite position marker
        sat_x, sat_y, sat_z = (
            bh.sOSCtoCART(
                [
                    element.sma,
                    element.ecc,
                    element.inc,
                    element.raan,
                    element.arg_perigee,
                    element.mean_anomaly,
                ],
                use_degrees=True,
            )[0:3]
            / 1e3
        )

        fig.add_trace(
            go.Scatter3d(
                x=[sat_x],
                y=[sat_y],
                z=[sat_z],
                mode="markers",
                marker=dict(color=color, size=8, symbol="diamond"),
                name=f"Sat {sat_idx + 1} Position",
                showlegend=False,
            )
        )

    # Configure layout
    max_range = (bh.R_EARTH / 1e3 + SATELLITE_ALTITUDE_KM) * 1.5
    fig.update_layout(
        title=f"Walker Constellation {inclination}°:{total_sats}/{num_planes}/{relative_spacing}",
        scene=dict(
            xaxis=dict(range=[-max_range, max_range], title="X [km]"),
            yaxis=dict(range=[-max_range, max_range], title="Y [km]"),
            zaxis=dict(range=[-max_range, max_range], title="Z [km]"),
            aspectmode="cube",
        ),
        width=800,
        height=800,
    )

    return fig


def main() -> None:
    """
    Generate all constellations for SATPLAN benchmarks and save to JSON files.

    Additionally generate plots of constellations and save off
    """

    base_spacecraft_path = get_data_path() / "spacecraft"

    for incl_param in SATELLITE_INCLINATIONS_DEG:
        inclination = SATELLITE_INCLINATIONS_DEG[incl_param]

        if incl_param == "SSO":
            # Compute Parameter for SSO
            sma = SATELLITE_ALTITUDE_KM * 1e3 + bh.R_EARTH  # in [m]
            ecc = SATELLITE_ECCENTRICITY
            inclination = bh.sun_sync_inclination(sma, ecc, use_degrees=True)

        for num_sats in NUM_SATELLITES:
            if num_sats not in WALKER_CONFIGURATIONS:
                logger.warning(
                    f"Skipping {num_sats} satellites, no walker configuration defined."
                )
                continue

            # Lookup walker configuration
            t, p, f = WALKER_CONFIGURATIONS[num_sats]

            sat_data = generate_orbital_elements(inclination, t, p, f)

            spacecraft_configuration = {
                "num_satellites": num_sats,
                "num_planes": p,
                "plane_phasing": f,
                "walker_config": [t, p, f],
                "inclination": incl_param,
                "altitude_km": SATELLITE_ALTITUDE_KM,
                "eccentricity": SATELLITE_ECCENTRICITY,
                "arg_perigee": SATELLITE_ARG_PERIGEE,
                "spacecraft": [],
            }

            constellation_spacecraft = []

            for sat_id, orbital_element, tle_line1, tle_line2 in sat_data:
                constellation_spacecraft.append(
                    {
                        "id": sat_id,
                        "name": f"Satellite {sat_id}",
                        "tle_line1": tle_line1,
                        "tle_line2": tle_line2,
                        "semimajor_axis": orbital_element.sma,
                        "eccentricity": orbital_element.ecc,
                        "inclination_deg": orbital_element.inc,
                        "raan_deg": orbital_element.raan,
                        "arg_perigee_deg": orbital_element.arg_perigee,
                        "mean_anomaly_deg": orbital_element.mean_anomaly,
                    }
                )

            spacecraft_configuration["spacecraft"] = constellation_spacecraft

            json_file_path = (
                base_spacecraft_path
                / incl_param.lower()
                / f"spacecraft_{num_sats}_{incl_param.lower()}.json"
            )

            if not json_file_path.parent.exists():
                json_file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(json_file_path, "w") as json_file:
                json.dump(spacecraft_configuration, json_file, indent=4)

            logger.info(
                f"Saved {incl_param} - {num_sats} constellation to {json_file_path}"
            )

            # Plot Constellation
            fig = plot_constellation_3d(sat_data, inclination, num_sats, p, f)

            # Save figure to image
            image_file_path = (
                base_spacecraft_path.parent.parent.parent.parent
                / "images"
                / "satellites"
                / incl_param.lower()
                / f"spacecraft_{num_sats}_{incl_param.lower()}.png"
            )

            # Ensure save directory exists
            if not image_file_path.parent.exists():
                image_file_path.parent.mkdir(parents=True, exist_ok=True)

            # Save as PNG, PDF, SVG, and HTML
            pdf_file_path = image_file_path.with_suffix(".pdf")
            svg_file_path = image_file_path.with_suffix(".svg")
            html_file_path = image_file_path.with_suffix(".html")

            fig.write_image(image_file_path)
            fig.write_image(pdf_file_path)
            fig.write_image(svg_file_path)
            fig.write_html(html_file_path)

            logger.info(
                f"Saved {incl_param} - {num_sats} constellation plot to {image_file_path}"
            )


if __name__ == "__main__":
    main()
