---
id: ctx-scope
title: Anwendungsbereich des ISMS
lang: de
version: 0.1.0
owner: "@isms-testorg/dev-isms-owner"
review_cycle_months: 12
classification: internal
controls: [A.5.1]
---

# Anwendungsbereich des ISMS

Dieses Dokument ist Teil des Informationssicherheits-Managementsystems von dev-test. Es wird unter Versionskontrolle gepflegt; die signierte git-Historie und die Release-Pakete sind sein Änderungsnachweis.

## 1. Zweck

Diese Erklärung definiert die Grenzen und die beabsichtigten Ergebnisse des fiktiven ISMS-Demonstrationssystems von dev-test. Sie unterstützt die einheitliche Anwendung der Informationssicherheitsrichtlinien und bildet den Kontext für Risikobehandlung, Ziele, Maßnahmen und dokumentierte Informationen. Sie stellt weder eine Zertifizierung noch einen Nachweis der Wirksamkeit im Betrieb dar.

## 2. Anwendungsbereich

Das ISMS umfasst die verteilten Beschäftigten und Auftragnehmer von dev-test sowie die Tätigkeiten Softwareentwicklung, Quellcodeverwaltung, Release-Management, Verarbeitung von Kundendaten und Betrieb unterstützender SaaS- und Cloud-Dienste. Eingeschlossen sind die GitHub-Organisation und -Repositories, CI/CD-Pipelines, der Identitätsanbieter, Endgeräte, Cloud-Hosting, SaaS-Lieferanten, die Geheimnisverwaltung, Sicherungsdienste und dieses versionierte ISMS-Repository.

Die Grenze umfasst die Arbeit aus dem Homeoffice und die Orte, von denen aus berechtigte Personen arbeiten, sowie relevante Lieferantenschnittstellen und von dev-test ausgewählte Cloud-Regionen. Der physische Rechenzentrumsbetrieb, interne Prozesse der Lieferanten und Kundensysteme außerhalb der Kontrolle von dev-test sind ausgeschlossen; ihre Sicherheit wird durch vertragliche Regelungen, Lieferantenprüfung und die gemeinsame Verantwortlichkeit adressiert. Das ISMS gilt für elektronische Informationen und relevante unterstützende Aufzeichnungen innerhalb der genannten Grenze, unabhängig vom Verarbeitungsort.

## 3. Rollen und Verantwortlichkeiten

Der Managing Director gibt die Richtung vor und genehmigt den Anwendungsbereich. Der CTO verantwortet die technische Governance, der Engineering Lead sichere Entwicklungs- und Release-Praktiken, der IT Lead Identitäten, Endgeräte, Sicherungen und Dienstabhängigkeiten. Der ISMS Owner pflegt das ISMS, koordiniert Risiko- und Compliance-Aktivitäten und berichtet den Status. Alle Beschäftigten und Auftragnehmer befolgen die geltenden Anforderungen und melden vermutete Ereignisse. Für ausgelagerte Dienste bleibt dev-test für eigene Entscheidungen verantwortlich, auch wenn die Umsetzung delegiert ist.

## 4. Anforderungen

Der Anwendungsbereich wird nach ISO/IEC 27001:2022 und den einschlägigen Referenzmaßnahmen aus Anhang A, den Pflichten aus DSGVO/GDPR, Kundenverträgen, Lieferantenverpflichtungen sowie anwendbaren kaufmännischen und gesetzlichen Aufbewahrungspflichten umgesetzt. Vertraulichkeit, Integrität und Verfügbarkeit werden risikobasiert durch dokumentierte Verantwortlichkeiten, das Prinzip der geringsten Rechte, sichere Änderungsverfahren, Resilienzmaßnahmen und den Schutz personenbezogener sowie kundenbezogener Informationen gesteuert.

## 5. Ausnahmen

Ausnahmen erfordern eine dokumentierte risikobasierte Begründung, einen benannten Owner, gegebenenfalls kompensierende Maßnahmen, ein Ablauf- oder Prüfdatum sowie die Genehmigung durch die verantwortliche Managementrolle und den ISMS Owner. Gesetzliche, vertragliche, datenschutzrechtliche und sicherheitsbezogene Pflichten dürfen durch eine operative Ausnahme nicht aufgehoben werden. Ausschlüsse vom Anwendungsbereich sind auf die oben genannten Grenzen beschränkt und werden bei Änderungen von Tätigkeiten, Systemen, Lieferanten oder Standorten überprüft.

## 6. Überwachung und Konformität

Der ISMS Owner überwacht Ziele, Risiken, Vorfälle, die Umsetzung von Maßnahmen, Dokumentenprüfungen, Lieferantenabhängigkeiten sowie Audit- und Bewertungsmaßnahmen anhand der Register und genehmigten Aufzeichnungen im Repository. Das Management prüft wesentliche Ergebnisse und überfällige Maßnahmen. Nichtkonformitäten werden erfasst und über das etablierte Verfahren für Korrekturmaßnahmen behandelt. Alle Aufzeichnungen sind fiktive Demonstrationsdaten; erzeugte Pipeline-Nachweise bleiben Aufgabe der Repository-Automatisierung und werden durch diese Erklärung nicht behauptet.

## 7. Referenzen

Wesentliche Referenzen sind ISO/IEC 27001:2022, Abschnitte 4.3, 4.4, 5.2, 6.1 und 7.5, sowie das dev-test-Risikoregister, die Anwendbarkeitserklärung, das Register der Asset-Gruppen, das Zieleregister, das Register interessierter Parteien und die genehmigten Richtlinien und Verfahren. Datenschutz- und Vertragsanforderungen werden für die jeweils relevante Verarbeitung und Dienstbeziehung ausgelegt.

## 8. Zugehörige Maßnahmen aus Anhang A

- **A.5.1** Informationssicherheitsrichtlinien
