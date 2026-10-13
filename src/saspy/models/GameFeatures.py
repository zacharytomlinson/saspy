from ._observed import ObservedFields


class GameFeatures(ObservedFields):
    """Client-owned observations for GameFeatures."""

    fields = (
        'game_number',
        'jackpot_multiplier',
        'AFT_bonus_awards',
        'legacy_bonus_awards',
        'tournament',
        'validation_extensions',
        'validation_style',
        'ticket_redemption',
    )
