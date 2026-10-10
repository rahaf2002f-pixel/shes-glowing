# She's Glowing website

## Run

Use the **Start application** workflow, or run:

```sh
python3 server.py
```

The server binds to `0.0.0.0:5000`. Both `/` and `/code.html` serve the static
page. Other paths return 404 so internal workspace files are not served.

No third-party Python packages are required. Tailwind CSS, Google Fonts, and
page images load from external hosts, so the page needs an internet connection.

## Page behavior

- The collection cards are a visual showcase; this site does not take orders.
- The shade quiz runs in the browser and does not use an external service.
