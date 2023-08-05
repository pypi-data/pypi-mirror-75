from monopolion_evaluator.protobuf import parser


def test_parse_delimited_file():
    game_outcomes = parser.parse_delimited_file('tests/fixtures/toy_data_2player.gz')

    for game_outcome in game_outcomes:
        assert game_outcome.winningPlayer in [0, 1]

        assert len(game_outcome.gameState.players) == 2
        for player in game_outcome.gameState.players:
            assert 0 <= player.cash <= 10 ** 4

        assert len(game_outcome.gameState.propertyStates) == 28
        for property_state in game_outcome.gameState.propertyStates:
            if property_state.isOwned:
                assert property_state.owner in [0, 1]
                assert 0 <= property_state.buildingCount <= 5


def test_to_data_frame():
    game_outcomes = parser.parse_delimited_file('tests/fixtures/toy_data_2player.gz')

    df = parser.to_data_frame(game_outcomes)

    assert df.shape == (3, 68)
    for index, row in df.iterrows():
        game_outcome = game_outcomes[index]
        assert game_outcome.winningPlayer == int(row['winningPlayer'])

        for player_index, player in enumerate(game_outcome.gameState.players):
            assert player.cash == int(row[f'{parser.PLAYER_PREFIX}_{player_index}_cash'])

        for property_index, property_state in enumerate(game_outcome.gameState.propertyStates):
            assert property_state.owner == int(row[f'{parser.PROPERTY_STATE_PREFIX}_{property_index}_owner'])
