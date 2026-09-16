import json
from pathlib import Path

import init_django_orm  # noqa: F401

from db.models import Race, Skill, Player, Guild


def main() -> None:
    data_path = Path(__file__).resolve().parent / "players.json"
    with data_path.open(encoding="utf-8") as f:
        players_data = json.load(f)

    for nickname, player_data in players_data.items():
        race_data = player_data["race"]
        race, _ = Race.objects.get_or_create(
            name=race_data["name"],
            defaults={"description": race_data["description"]},
        )

        guild_data = player_data["guild"]
        if guild_data is not None:
            guild, _ = Guild.objects.get_or_create(
                name=(guild_data["name"] if guild_data["name"] else None),
                defaults={
                    "description":
                        guild_data["description"]
                        if guild_data["description"]
                        else None
                },
            )
        else:
            guild = None

        for skill in race_data["skills"]:
            Skill.objects.get_or_create(
                name=skill["name"],
                defaults={"bonus": skill["bonus"], "race": race},
            )

        Player.objects.get_or_create(
            nickname=nickname,
            defaults={
                "email": player_data["email"],
                "bio": player_data["bio"],
                "guild": guild,
                "race": race
            },
        )


if __name__ == "__main__":
    main()
