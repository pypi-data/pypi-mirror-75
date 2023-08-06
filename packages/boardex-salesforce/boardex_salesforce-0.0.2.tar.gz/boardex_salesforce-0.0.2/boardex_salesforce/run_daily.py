from .download_ContactDetails_from_sf import download_ContactDetails_from_sf
from .download_UserDetails_from_sf import download_UserDetails_from_sf

def run_daily():
    download_ContactDetails_from_sf()
    download_UserDetails_from_sf()

if __name__ == '__main__':
        run_daily()