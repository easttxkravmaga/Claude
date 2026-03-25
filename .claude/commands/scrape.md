Run the ETKM contact scraper on the URL(s) provided in $ARGUMENTS.

Steps:
1. Run this command:
   ```
   python3 /home/user/Claude/scripts/scrape_contacts.py $ARGUMENTS
   ```
2. Read the output file at `/home/user/Claude/output/scrape_contacts.xlsx` and report what was found.
3. Show a clean summary table of all contacts extracted: Name, Title, Email, Phone, Source URL.
4. If zero contacts were found on a URL, retry with the `--crawl` flag if available, or note the failure.
5. Confirm the file is saved at `output/scrape_contacts.xlsx`.

No need to ask which flags to use — just run it and report results.
