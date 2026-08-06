"""Example tests for password hashing and verification."""

from core.security import hash_password, verify_password


def test_hash_roundtrip():
    encoded = hash_password('s3cret!')
    assert verify_password('s3cret!', encoded)
    assert not verify_password('wrong', encoded)


def test_hash_uses_random_salt():
    assert hash_password('same') != hash_password('same')


def test_encoded_format():
    encoded = hash_password('pw')
    assert encoded.startswith('pbkdf2_sha256$')
    assert len(encoded.split('$')) == 4


def test_verify_rejects_malformed():
    assert not verify_password('pw', 'not-a-valid-hash')
    assert not verify_password('pw', '')
