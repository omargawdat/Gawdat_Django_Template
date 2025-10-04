from django.conf import settings
from django.core.management.base import BaseCommand
from djmoney.money import Money

from apps.location.domain.utils import CountryInfoUtil
from apps.location.models.country import Country


class Command(BaseCommand):
    help = "Load supported countries from settings.SUPPORTED_COUNTRY_CODES into the database"

    def handle(self, *args, **options):
        supported_codes = settings.SUPPORTED_COUNTRY_CODES
        created_count = 0
        existing_count = 0
        deactivated_count = 0
        failed_count = 0

        self.stdout.write(
            self.style.SUCCESS(f"Loading {len(supported_codes)} supported countries...")
        )

        for country_code in supported_codes:
            try:
                # Get currency for this country
                currency = CountryInfoUtil.get_currency_code(country_code)

                # Prepare default values
                defaults = {
                    "is_active": True,
                    "app_install_money_inviter": Money(0, currency),
                    "app_install_money_invitee": Money(0, currency),
                    "order_money_inviter": Money(0, currency),
                    "order_money_invitee": Money(0, currency),
                }

                # Create or get the country
                country, created = Country.objects.get_or_create(
                    code=country_code, defaults=defaults
                )

                if created:
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"  ✓ Created: {country.name} ({country_code})"
                        )
                    )
                else:
                    # Ensure existing country is active
                    if not country.is_active:
                        country.is_active = True
                        country.save()
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"  ↻ Reactivated: {country.name} ({country_code})"
                            )
                        )
                    existing_count += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f"  - Already exists: {country.name} ({country_code})"
                        )
                    )

            except Exception as e:
                failed_count += 1
                self.stdout.write(
                    self.style.ERROR(f"  ✗ Failed to load {country_code}: {e!s}")
                )

        # Deactivate countries not in supported list
        self.stdout.write("\nChecking for unsupported countries...")
        unsupported_countries = Country.objects.exclude(code__in=supported_codes)
        for country in unsupported_countries:
            if country.is_active:
                country.is_active = False
                country.save()
                deactivated_count += 1
                self.stdout.write(
                    self.style.WARNING(
                        f"  ⊗ Deactivated: {country.name} ({country.code})"
                    )
                )

        # Final summary
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write(self.style.SUCCESS(f"✓ Created: {created_count}"))
        self.stdout.write(self.style.WARNING(f"- Already existed: {existing_count}"))
        if deactivated_count > 0:
            self.stdout.write(self.style.WARNING(f"⊗ Deactivated: {deactivated_count}"))
        if failed_count > 0:
            self.stdout.write(self.style.ERROR(f"✗ Failed: {failed_count}"))
        self.stdout.write("=" * 50 + "\n")
