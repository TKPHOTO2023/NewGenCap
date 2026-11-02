# Site builder

The eight HTML pages are generated from these files, so shared parts (header, footer, media,
services, settings awaiting confirmation) are changed in one place.

```
cd tools/site-builder
python3 pages.py ../..
```

- `shared.py`: navigation, services, deal sizes, response time, image slots, header and footer.
- `pages.py`: the content of each page, the case study details and the readiness questions.
- `images.json`: the widths available for each web image in `assets/img/site/`.
