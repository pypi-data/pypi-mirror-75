def validate_private_key(private_key: str) -> None:
    if type(private_key) is not str:
        raise TypeError('Expect {0} to be {1}, got {2}'.format(
            'private_key',
            str,
            type(private_key))
        )

    if len(private_key) < 1:
        raise ValueError('private_key is too short')