"""
    Author: Isaac T Chikutukutu
    Date: 14 Oct 2021
"""

import dataclasses
import sys

log_standing = []
points_sheet = {}


USAGE = f"Sample Usage: python3 {sys.argv[0]} [--help] | input_filename output_filename]"


@dataclasses.dataclass
class Arguments:
    input_filename: str = 'inputs.txt'
    output_filename: str = 'outputs.txt'


def extract_team_scores(scores: list):
    team1 = ''.join(filter(str.isalpha, scores[0]))
    t1_score = int(''.join(filter(str.isdigit, scores[0])))
    team2 = ''.join(filter(str.isalpha, scores[1]))
    t2_score = int(''.join(filter(str.isdigit, scores[1])))

    if t1_score > t2_score:
        points_sheet[team1] = points_sheet.get(team1, 0) + 3
        points_sheet[team2] = points_sheet.get(team2, 0) + 0
    elif t2_score > t1_score:
        points_sheet[team2] = points_sheet.get(team2, 0) + 3
        points_sheet[team1] = points_sheet.get(team1, 0) + 0
    else:
        points_sheet[team1] = points_sheet.get(team1, 0) + 1
        points_sheet[team2] = points_sheet.get(team2, 0) + 1


def calculate_rankings():
    prev_team_position = 0
    prev_team_points = 0
    sheet_not_empty = bool(points_sheet)

    while sheet_not_empty:
        top_team = max(points_sheet, key=points_sheet.get)
        top_team_points = points_sheet.get(top_team, 0)
        top_team_position = 0

        if top_team_points < prev_team_points:
            top_team_position = prev_team_position + 1
        elif prev_team_points < top_team_points or prev_team_points == 0:
            top_team_position = 1
        elif prev_team_points == top_team_points:
            # Draw / Tie
            top_team_position = prev_team_position

        prev_team_points = top_team_points
        prev_team_position = top_team_position

        log_standing.append({'team': top_team, 'points': top_team_points, 'position': top_team_position})
        points_sheet.pop(top_team)
        sheet_not_empty = bool(points_sheet)


def validate(args: list):
    try:
        arguments = Arguments(*args)
        return arguments
    except TypeError:
        raise SystemExit(USAGE)


def main() -> None:
    args = sys.argv[1:]

    if not args:
        print("No Arguments supplied, using defaults input_filename & output_filename \n")

    if args and args[0] == "--help":
        print(USAGE)
    else:
        arguments = validate(args)
        input_file = getattr(arguments, 'input_filename')
        output_file = getattr(arguments, 'output_filename')

        try:
            input_file_obj = open(input_file)
        except Exception as e:
            raise e

        for x, line in enumerate(input_file_obj.readlines()):
            extract_team_scores(line.split(','))

        input_file_obj.close()

        calculate_rankings()

        lines = []
        for entry in log_standing:
            output = f"{entry['position']}. {entry['team']}, {entry['points']}"
            lines.append(output + '\n')
            print(output)

        try:
            output_file_obj = open(output_file, 'w')
            output_file_obj.writelines(lines)
            output_file_obj.close()
        except Exception as e:
            raise e


if __name__ == '__main__':
    main()
