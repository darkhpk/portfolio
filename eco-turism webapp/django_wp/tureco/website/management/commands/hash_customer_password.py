from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password, identify_hasher
from website.models import User as CustomerUser

def looks_hashed(value: str) -> bool:
    try:
        identify_hasher(value)
        return True
    except Exception:
        return False

class Command(BaseCommand):
    help = "Hash any plaintext passwords stored in booking.models.User."

    def handle(self, *args, **options):
        upgraded = 0
        skipped = 0
        qs = CustomerUser.objects.all().only("id", "password")
        for u in qs.iterator():
            pwd = u.password or ""
            if not pwd:
                skipped += 1
                continue
            if looks_hashed(pwd):
                skipped += 1
                continue
            # Treat as plaintext and upgrade
            u.password = make_password(pwd)
            u.save(update_fields=["password"])
            upgraded += 1

        self.stdout.write(self.style.SUCCESS(
            f"Done. Upgraded {upgraded} password(s), skipped {skipped}."
        ))
