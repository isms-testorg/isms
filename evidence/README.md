# Evidence

Records demonstrating that controls actually operate, as opposed to documents
describing what should happen.

```
github/YYYY-MM/   written by .github/workflows/evidence-collect.yml
                  do not edit; a snapshot of what the API returned
manual/           anything collected by hand
```

Every file here must have an entry in `data/evidence-index.yml`. `make check`
warns about unindexed files and fails on index entries that match nothing.

**Never commit credentials, personal data, or secret scanning alert details.**
This directory ships inside the release pack that goes to external auditors.
The collector stores counts and configuration only, deliberately.

Freshness is read from the `YYYY-MM` directory name, not the file timestamp: a
fresh clone resets every mtime to checkout time, which would make expired
evidence look brand new. File manual evidence under a dated directory to get
the same expiry check.
