from .download_company_from_sf import download_company_from_sf
from .download_contact_from_sf import download_contact_from_sf
from .download_ContactDetails_from_sf import download_ContactDetails_from_sf
from .download_UserDetails_from_sf import download_UserDetails_from_sf
from .upload_to_salesforce import upload_to_sf

def run_monthly():
    upload_to_sf()
    download_company_from_sf()
    download_contact_from_sf()
    download_ContactDetails_from_sf()
    download_UserDetails_from_sf()
if __name__ == '__main__':
        run_monthly()