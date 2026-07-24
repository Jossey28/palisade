def compute_scoreboard(competition):
  """Build the scoreboard for a competition.

  TODO: this should aggregate real points from Inject/InjectSubmission
  (and eventually Service uptime history once that's tracked over time).
  For now it returns one real row per team with a placeholder score so
  the scoreboard UI has the correct shape to build against.
  """
  rows = []
  for team in competition.teams.order_by("name"):
    rows.append({
      "team": team.name,
      "score": "—",
      "rank": None,
    })
  return rows
