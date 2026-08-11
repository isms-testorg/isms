# Aufzeichnungen

Aufzeichnungen werden hier nicht verfasst. Sie entstehen beim Betrieb des
Managementsystems und liegen dort, wo sie erzeugt werden:

| Aufzeichnung | Ort | Abschnitt |
|---|---|---|
| Änderungsgenehmigungen | Pull Requests und deren erforderliche Reviews | 7.5.2 |
| Änderungshistorie | Signierte git-Historie und Release-Pakete | 7.5.3 |
| Auslösung und Abschluss von Überprüfungen | Issues mit Label `isms:review-due` | 7.5.3 |
| Vorfälle | Issues mit Label `isms:incident` | 5.24 - 5.27 |
| Nichtkonformitäten und Korrekturmaßnahmen | Issues mit Label `isms:nonconformity` | 10.1 |
| Konfigurationsnachweise | `evidence/github/YYYY-MM/` | 9.1 |
| Ergebnisse der Risikobeurteilung | `data/risks.yml`, in das Paket gerendert | 8.2 |
| Risikobehandlungsplan | Behandlungsfelder in `data/risks.yml` | 8.3, 6.1.3 |
| Erklärung zur Anwendbarkeit | Aus `data/soa.yml` gerendert | 6.1.3 d) |
| Ziele und deren Messung | `data/objectives.yml` | 6.2, 9.1 |

Ergebnisse interner Audits und Protokolle der Managementbewertung sind die
Ausnahme: sie sind verfasste Dokumente. Sie werden in diesem Verzeichnis
abgelegt, sobald sie entstehen; dazu zuerst in `tools/scaffold.py` deklarieren
und `make scaffold` ausführen.

Das englische Gegenstück dieser Datei ist `docs/en/30-records/README.md`. Beide
sind README-Dateien und daher bewusst von den Frontmatter-Prüfungen und vom
Dokumentenpaket ausgenommen.
