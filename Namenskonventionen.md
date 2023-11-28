# REST API Design - Best Practices

## Versionierung
- **Wichtig für die Weiterentwicklung**: API-Änderungen dürfen existierende Clients nicht beeinträchtigen.
- **Methoden**: In der URL (z.B. /v1/), im Accept-Header oder als Query-Parameter.
- **Dokumentation**: Klarstellen, welche API-Version welche Funktionen bietet.

## Namenskonventionen
- **URI-Struktur**: Klare, beschreibende Pfade (z.B. /users).
- **Verwendung von Substantiven**: Ressourcen sollten nicht verhaltensbasiert benannt werden (z.B. /orders statt /getOrders).
- **Mehrzahl vs. Einzahl**: Wenn möglich, und es sich nicht um eine einmalig vorkommende Resource handelt, mehrzahl nutzen (z.B. /users/{id}).

## Korrekter Einsatz der HTTP-Methoden
- **GET**: Abrufen von Ressourcen.
- **POST**: Erstellen einer neuen Ressource oder Trigger einer Operation (z.B. starten eines Jobs auf einem Server).
- **PUT**: Ersetzen oder Aktualisieren einer Ressource.
- **DELETE**: Löschen einer Ressource.

Quellen: 
- [Microsoft RESTful-Weg-API-Design](https://learn.microsoft.com/de-de/azure/architecture/best-practices/api-design)
- [Google 6 common REST mistakes](https://cloud.google.com/blog/products/api-management/restful-web-api-design-best-practices?hl=en)
- [Medium REST API Naming Conventions](https://medium.com/@nadinCodeHat/rest-api-naming-conventions-and-best-practices-1c4e781eb6a5)