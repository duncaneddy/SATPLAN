# Benchmark Definitions
NUM_SATELLITES: list[int] = [1, 2, 5, 10, 20, 50, 100]
SATELLITE_INCLINATIONS: list[str] = ["MIO", "SSO"]  # 53, and sun synchronous
NUM_REQUESTS: list[int] = [100, 200, 500, 1000, 2000, 5000, 10000]

# Benchmark Generation Constants
SATELLITE_ALTITUDE_KM: float = 550.0
SATELLITE_ECCENTRICITY: float = 0.001
SATELLITE_ARG_PERIGEE: float = 0.0
RANDOM_REWARD_RANGE: tuple[float, float] = (1.0, 10.0)

SATELLITE_INCLINATIONS_DEG = {
    "MIO": 53.0,
    "SSO": 0.0,  # Computed at generation time
}

WALKER_CONFIGURATIONS = {
    1: (1, 1, 0),
    2: (2, 2, 0),
    5: (5, 5, 0),
    10: (10, 5, 0),
    20: (20, 5, 0),
    50: (50, 10, 0),
    100: (100, 25, 0),
}

EPOCH = "2025-01-01T00:00:00Z"
PLANNING_HORIZON = 24 * 60 * 60  # 24 hours in seconds
