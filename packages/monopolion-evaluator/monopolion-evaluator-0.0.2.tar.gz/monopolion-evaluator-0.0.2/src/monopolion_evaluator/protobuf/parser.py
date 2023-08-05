import gzip
import itertools
from typing import Generator
from typing import List

import pandas as pd
from google.protobuf.internal.decoder import _DecodeVarint32

from monopolion_evaluator.protobuf import game_outcome_pb2

PROPERTY_STATE_PREFIX = 'property'
PLAYER_PREFIX = 'player'

GAME_OUTCOME_COLUMNS = ('winningPlayer', )
GAME_STATE_COLUMNS = ('die1', 'die2', 'state')
PLAYER_COLUMNS = ('position', 'cash', 'isInJail', 'remainingTurnsInJail')
PROPERTY_STATE_COLUMNS = ('owner', 'buildingCount')


def parse_delimited_file(filename: str, decompress: bool = True) -> game_outcome_pb2.GameOutcome:
    """
    Parse a delimited protobuf file with game outcomes, which specify a game state and which player won.

    :param filename: Path to GameOutcome protobuf file
    :param decompress: Set to True if the file is gzip'ed
    :return: Protobuf GameOutcome object
    """
    game_outcomes = []
    open_function = gzip.open if decompress else open

    with open_function(filename, "rb") as f:
        buf = f.read()
        n = 0
        while n < len(buf):
            msg_len, new_pos = _DecodeVarint32(buf, n)
            n = new_pos
            msg_buf = buf[n:n + msg_len]
            n += msg_len
            game_outcome = game_outcome_pb2.GameOutcome()
            game_outcome.ParseFromString(msg_buf)
            game_outcomes.append(game_outcome)

    return game_outcomes


def to_data_frame(game_outcomes: List[game_outcome_pb2.GameOutcome]) -> pd.DataFrame:
    """
    Convert parsed protobuf objects to a flat Pandas DataFrame.

    :param game_outcomes: List of GameOutcome protobuf objects
    :return: Flat pandas DataFrame.
    """
    if not game_outcomes:
        raise ValueError('game_outcome must not be empty')

    column_names = __get_df_column_names(game_outcomes)

    return pd.DataFrame(
        data=__game_outcomes_to_list(game_outcomes),
        columns=column_names)


def __get_df_column_names(game_outcomes):
    player_count = len(game_outcomes[0].gameState.players)
    property_count = len(game_outcomes[0].gameState.propertyStates)
    all_player_cols = itertools.product(range(player_count), PLAYER_COLUMNS)
    all_prop_cols = itertools.product(range(property_count), PROPERTY_STATE_COLUMNS)
    player_cols = [__get_col_name(c, PLAYER_PREFIX, i) for i, c in all_player_cols]
    prop_cols = [__get_col_name(c, PROPERTY_STATE_PREFIX, i) for i, c in all_prop_cols]
    columns = list(GAME_OUTCOME_COLUMNS) + list(GAME_STATE_COLUMNS) + player_cols + prop_cols
    return columns


def __get_col_name(name, prefix=None, index=None, ):
    return '_'.join(filter(None, [prefix, str(index), name]))


def __game_outcome_to_list(game_outcome: game_outcome_pb2.GameOutcome) -> List[int]:
    values = [int(getattr(game_outcome, c)) for c in GAME_OUTCOME_COLUMNS]
    values += [int(getattr(game_outcome.gameState, c)) for c in GAME_STATE_COLUMNS]
    for player in game_outcome.gameState.players:
        for col_name in PLAYER_COLUMNS:
            values.append(int(getattr(player, col_name)))

    for property_state in game_outcome.gameState.propertyStates:
        for col_name in PROPERTY_STATE_COLUMNS:
            values.append(int(getattr(property_state, col_name)))

    return values


def __game_outcomes_to_list(game_outcomes: List[game_outcome_pb2.GameOutcome]) -> Generator[List[int], None, None]:
    for game_outcome in game_outcomes:
        yield __game_outcome_to_list(game_outcome)
