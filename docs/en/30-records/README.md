# Records

Records are not authored here. They are produced by running the management
system, and live where they are generated:

| Record | Where it lives | Clause |
|---|---|---|
| Change approvals | Pull requests and their required reviews | 7.5.2 |
| Change history | The signed git history and the release packs | 7.5.3 |
| Review triggers and closure | Issues labelled `isms:review-due` | 7.5.3 |
| Incidents | Issues labelled `isms:incident` | 5.24 - 5.27 |
| Nonconformities and corrective actions | Issues labelled `isms:nonconformity` | 10.1 |
| Configuration evidence | `evidence/github/YYYY-MM/` | 9.1 |
| Risk assessment results | `data/risks.yml`, rendered into the pack | 8.2 |
| Risk treatment plan | `data/risks.yml` treatment fields | 8.3, 6.1.3 |
| Statement of Applicability | Rendered from `data/soa.yml` | 6.1.3 d) |
| Objectives and their measurement | `data/objectives.yml` | 6.2, 9.1 |

Internal audit results and management review minutes are the exception: they
are authored documents. Add them under this directory as they are produced,
using `make scaffold` after declaring them in `tools/scaffold.py`.

The German mirror of this file is `docs/de/30-records/README.md`. Both are
README files and are deliberately excluded from the frontmatter checks and from
the document pack.
