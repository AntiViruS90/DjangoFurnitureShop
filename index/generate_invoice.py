from InvoiceGenerator.api import Invoice, Item, Client, Provider, Creator
from InvoiceGenerator.pdf import ProformaInvoice, SimpleInvoice
import datetime


def create_invoice(provider_name, provider_address, provider_postcode, client_name, client_address, client_postcode,
                   items_list):
    provider = Provider(provider_name, provider_address, provider_postcode, bank_account='2600420569', bank_code='2010')
    creator = Creator('')
    client = Client(client_name, client_address, client_postcode)

    invoice = Invoice(client, provider, creator)
    invoice.currency_locale = 'en_US.UTF-8'
    invoice.use_tax = False
    for i in range(0, len(items_list), 3):
        item_count = items_list[i]
        item_price = items_list[i + 1]
        item_name = items_list[i + 2]
        invoice.add_item(Item(item_count, item_price, description=item_name))
    pdf = ProformaInvoice(invoice)
    pdf.gen("Proforma.pdf", generate_qr_code=False)
