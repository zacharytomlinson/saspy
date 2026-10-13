from ._observed import ObservedFields


class AftStatements(ObservedFields):
    """Client-owned observations for AftStatements."""

    fields = (
        'registration_status',
        'asset_number',
        'registration_key',
        'POS_ID',
        'transaction_buffer_position',
        'transfer_status',
        'receipt_status',
        'transfer_type',
        'cashable_amount',
        'restricted_amount',
        'nonrestricted_amount',
        'transfer_flags',
        'transaction_ID_lenght',
        'transaction_ID',
        'transaction_date',
        'transaction_time',
        'expiration',
        'pool_ID',
        'cumulative_casable_amount_meter_size',
        'cumulative_casable_amount_meter',
        'cumulative_restricted_amount_meter_size',
        'cumulative_restricted_amount_meter',
        'cumulative_nonrestricted_amount_meter_size',
        'cumulative_nonrestricted_amount_meter',
        'game_lock_status',
        'avilable_transfers',
        'host_cashout_status',
        'AFT_status',
        'max_buffer_index',
        'current_cashable_amount',
        'current_restricted_amount',
        'current_non_restricted_amount',
        'restricted_expiration',
        'restricted_pool_ID',
    )
