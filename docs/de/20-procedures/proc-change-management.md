---
id: proc-change-management
title: Verfahren für die Änderungssteuerung
lang: de
version: 0.1.0
owner: "@isms-testorg/dev-isms-owner"
review_cycle_months: 24
classification: internal
controls: []
---

# Verfahren für die Änderungssteuerung

Dieses Dokument ist Teil des Informationssicherheits-Managementsystems von dev-test. Es wird unter Versionskontrolle gepflegt; die signierte git-Historie und die Release-Pakete sind sein Änderungsnachweis.

## 1. Zweck

Dieses Verfahren stellt sicher, dass Änderungen an Code, Infrastruktur, Cloud-Konfiguration, CI/CD, Identität, SaaS-Integrationen, Sicherheitsmaßnahmen und ISMS-Inhalten genehmigt, getestet, nachvollziehbar und rücksetzbar sind.

## 2. Anwendungsbereich

Es gilt für geplante, dringende, standardmäßige und von Lieferanten durchgeführte Änderungen, die ISMS-Systeme, die Verarbeitung von Kundendaten, Releases oder ISMS-Dokumente betreffen. Die übliche Entwicklungsarbeit unterliegt weiterhin der Repository-Prüfung und den CI-Prüfungen; produktionswirksame Änderungen benötigen die hier beschriebene zusätzliche Genehmigung.

## 3. Rollen und Verantwortlichkeiten

Der Antragsteller beschreibt die Änderung und ihr Risiko. Der Engineering Lead genehmigt Code- und Release-Änderungen; der IT-Leiter genehmigt Änderungen an Identität, Endgeräten, Infrastruktur und Diensten; der CTO genehmigt wesentliche technische oder Sicherheitsrisiken; der ISMS-Verantwortliche prüft Änderungen an ISMS-Dokumenten und Aufzeichnungen. Der Managing Director genehmigt Änderungen mit wesentlichen geschäftlichen, rechtlichen, kundenseitigen oder verbleibenden Sicherheitsauswirkungen.

## 4. Anforderungen

Jede Änderung hat ein Issue, einen Pull Request oder einen genehmigten Service-Datensatz mit Zweck, Umfang, betroffenen Assets, Sicherheits- und Datenschutzwirkung, Abhängigkeiten, Umsetzungsplan, Testnachweis, Rücksetzplan, Verantwortlichem und gewünschtem Zeitpunkt. Änderungen nutzen, soweit praktikabel, Vier-Augen-Prinzip, geschützte Branches und automatisierte Prüfungen. Vor dem Deployment bestätigt der zuständige Lead Test und Genehmigung. Danach prüft der Verantwortliche erwartetes Verhalten, Monitoring, Backups und Kundenauswirkungen und dokumentiert das Ergebnis. Fehlgeschlagene Änderungen werden zurückgesetzt oder eingedämmt und eskaliert. Notfalländerungen dürfen zum Schutz von Vertraulichkeit, Integrität, Verfügbarkeit oder Sicherheit umgesetzt werden, müssen aber innerhalb von zwei Arbeitstagen nachträglich geprüft und genehmigt werden. Ausgaben sind Datensatz, aktualisierte Konfiguration oder Dokument, Deployment-Historie, Testergebnis und Erkenntnisse.

## 5. Ausnahmen

Eine Notfall- oder dringende Änderung darf nur dann von der üblichen Terminplanung abweichen, wenn eine Verzögerung ein größeres Risiko erzeugt. Der zuständige Lead dokumentiert Grund, Umfang, kompensierende Maßnahmen und Genehmiger. Sicherheitsprüfungen, Zugriffsbeschränkungen sowie gesetzliche und vertragliche Anforderungen dürfen ohne ausdrückliche Genehmigung des CTO und bei wesentlichen Auswirkungen des Managing Directors nicht entfallen.

## 6. Überwachung und Konformität

Der ISMS-Verantwortliche prüft vierteljährlich stichprobenartig Genehmigung, Vier-Augen-Prinzip, Testnachweis, Rücksetzbarkeit, Funktionstrennung und Nachprüfung. Engineering und IT überwachen fehlgeschlagene und dringende Änderungen, Rücksetzungen und überfällige Nachprüfungen. Ausnahmen und wiederholte Fehler werden zu Korrekturmaßnahmen. Das Verfahren wird alle 24 Monate oder nach einer wesentlichen Änderung von Plattform, Release oder Governance geprüft.

## 7. Referenzen

ISO/IEC 27001:2022, Abschnitte 6.3, 7.5, 8.1 und 8.2; die Richtlinien für sichere Entwicklung, Betrieb, Zugriffskontrolle und dokumentierte Information; Pull Requests und CI/CD-Aufzeichnungen; Konfigurationsaufzeichnungen; sowie das Verfahren für Nichtkonformität und Korrekturmaßnahmen.

## 8. Zugehörige Maßnahmen aus Anhang A

Keine unmittelbar. Dieses Dokument erfüllt eine Anforderung aus den Abschnitten 4 bis 10 der Norm.
