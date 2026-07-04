import fastf1


def load_race_session(year: int, gp: str, session_type: str = "R"):
    session = fastf1.get_session(year, gp, session_type)
    session.load()
    return session