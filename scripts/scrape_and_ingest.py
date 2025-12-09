from dotenv import load_dotenv
import os
import time

load_dotenv()

from app.services.web_scraper import scrape_urls
from app.services.pinecone_ingest import upsert_to_pinecone, load_scraping_data

# List of target URLs provided by the user
URLS = [
    "https://www.hardchews.me/hard-chews-tsl-1-sub-163?f=6dbq9s",
    "https://www.hardchews.me/hard-chews-tsl-1-sub-163?f=6dbq9s#about",
    "https://www.hardchews.me/hard-chews-tsl-1-sub-163?f=6dbq9s#ingredients",
    "https://www.hardchews.me/hard-chews-tsl-1-sub-163?f=6dbq9s#buynow",
    "https://hardchews.me/dynamic-hc-vsl-1-page-163?b=263",
    "https://hardchews.me/hard-chews-tsl-1-sub-163",
    "https://orders.clickbank.net/?cbfid=61689&cbitems=hc6-sub&corid=800040f9-8dce-4e93-a395-506b5c198b30&oaref=01.248ED1CBDFCA137F0948BE2CE67D1020242F02676E4C48ACBF39128809B7F1BC66DCB804&template=hc6-sub&time=1765018920&vvvv=hardchews&vvar=__click_id%3Dfg3z58AC1swMwolB49YNw6IK%26cbfid%3D61689%26cbitems%3Dhc6-sub%26pfnid%3D1%26template%3Dhc6-sub",
    "https://orders.clickbank.net/?cbfid=61691&cbitems=hc1-sub&corid=b0af70c9-af73-4cf0-8081-bd5cb43b3ba3&oaref=01.248ED1CBDFCA137F0948BE2CE67D1020242F02676E4C48ACBF39128809B7F1BC66DCB804&template=hc1-sub&time=1765018949&vvvv=hardchews&vvar=__click_id%3DlIyTFNeszP63jI5jMRdOYOJF%26cbfid%3D61691%26cbitems%3Dhc1-sub%26pfnid%3D1%26template%3Dhc1-sub",
    "https://orders.clickbank.net/?cbfid=61690&cbitems=hc3-sub&corid=05192949-3c85-42ab-b71c-e6a4fdce7650&oaref=01.248ED1CBDFCA137F0948BE2CE67D1020242F02676E4C48ACBF39128809B7F1BC66DCB804&template=hc3-sub&time=1765018973&vvvv=hardchews&vvar=__click_id%3DYHF9Z7AXFUQcf1AxAfCImri%26cbfid%3D61690%26cbitems%3Dhc3-sub%26pfnid%3D1%26template%3Dhc3-sub",
    "https://www.hardchews.me/contact",
    "https://www.hardchews.me/privacy-policy",
    "https://www.hardchews.me/terms-of-service",
    "https://www.hardchews.me/shipping-terms",
    "https://www.hardchews.me/returns-and-refunds",
    "https://hardchews.shop/",
    "https://account.hardchews.shop/authentication/login?client_id=352b719d-fd88-448a-b26f-c8a78de36c2e&locale=en&redirect_uri=%2Fauthentication%2Foauth%2Fauthorize%3Fclient_id%3D352b719d-fd88-448a-b26f-c8a78de36c2e%26locale%3Den%26nonce%3D92cbe42f-2549-45e1-9d7e-f7ed3b1ca845%26redirect_uri%3Dhttps%253A%252F%252Faccount.hardchews.shop%252Fcallback%253Fsource%253Dcore%26region_country%3DUS%26response_type%3Dcode%26scope%3Dopenid%2Bemail%2Bcustomer-account-api%253Afull%26state%3DhWN67Cb1Kz0GSywHlFxBNISP",
    "https://www.clickbank.com/",
    "https://www.hardchews.me/f/6dbq9s/",
    "https://www.hardchews.me/f/wtgpxj/",
    "https://www.hardchews.me/hc-main-163?bottles=263&f=wtgpxj&fnid=2",
    "https://www.hardchews.me/hc-main-163?bottles=263&sub=yes&toggle=yes",
    "https://hardchews.me/dynamic-hc-vsl-1-page-163?b=263",
    "https://hardchews.me/hard-chews-tsl-1-sub-163",
]


def main():
    print("Starting scraping of provided URLs...")
    scraped = scrape_urls(URLS)
    print(f"Scraped {len(scraped.get('pages', []))} pages. Waiting 2s before ingestion...")
    time.sleep(2)

    # Now run the existing ingestion which reads app/kb/cache/scraped_data.json
    print("Loading scraping data and upserting to Pinecone...")
    scraping_items = load_scraping_data()
    print(f"Loaded {len(scraping_items)} scraping items")
    if scraping_items:
        upsert_to_pinecone(scraping_items, namespace="scraping")
        print("Upsert complete.")
    else:
        print("No scraping items found to upsert.")


if __name__ == '__main__':
    main()
