from django.core.management.base import BaseCommand
from financial.models import ContractData, ContractStatusChoices


class Command(BaseCommand):
    help = "Updates status and alert date for all non-expired contracts"

    def handle(self, *args, **options):
        contracts = ContractData.objects.exclude(status=ContractStatusChoices.DEFEATED)
        updated = 0

        for contract in contracts:
            contract.update_contract_status()
            contract.save()
            updated += 1

        self.stdout.write(self.style.SUCCESS(f"{updated} contracts updated successfully."))
