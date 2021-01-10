# Enron email dataset - Neo4j

This repository contains a Dockerfile that can be started to populate a
[Neo4j database](https://neo4j.com/) with emails and recipients of emails.

## Mails responses

You can create a relationship between emails with their responses by running the following cypher 
query against the database populated with this repository.

```cypher
MATCH p=(a1:Recipient)-[:SENT]->(m1:Mail)<-[:RECEIVED]-(i:Recipient)-[:SENT]->(m2:Mail)<-[:RECEIVED]-(a1) 
WHERE a1.mail          <>    i.mail 
  AND m1.message_id    <>    m2.message_id 
  AND m2.body       CONTAINS m1.body
  AND m1.date          <     m2.date
CREATE (m2)-[r:RESPONSE_TO]->(m1)
```

This query is far from perfect (it has some issues related to email threads) but has the
advantage to be pretty simple and straightforward.