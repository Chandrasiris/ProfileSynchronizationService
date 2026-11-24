class LegacyContactProtector:
    """Fail closed until byte-for-byte C# compatibility is verified."""
    def email_hash(self, normalized: str) -> str:
        raise NotImplementedError('Legacy email hash contract required')
    def phone_hash(self, normalized: str) -> str:
        raise NotImplementedError('Legacy phone hash contract required')
    def encrypt(self, value: str) -> str:
        raise NotImplementedError('Legacy encryption contract required')
