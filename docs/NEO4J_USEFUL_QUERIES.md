# Queries Úteis para o Grafo Neo4j

Gerado em: 2025-11-16T19:28:09.548890

## All Agent Dependencies

```cypher

                    MATCH (a:Agent)-[r:IMPORTS|DEPENDS_ON|USES]->(b)
                    RETURN a.name as agent, type(r) as relationship, b.name as dependency
                    ORDER BY a.name, type(r)
                
```

## Service Communication Flow

```cypher

                    MATCH path = (s1:Service)-[:CALLS|QUERIES|CONNECTS_TO*]->(s2:Service)
                    RETURN s1.name as source, s2.name as target, length(path) as hops
                    ORDER BY hops
                
```

## Agent Capabilities

```cypher

                    MATCH (a:Agent)
                    RETURN a.name as agent, a.capabilities as capabilities, a.type as type
                    ORDER BY a.name
                
```

## Configuration Usage

```cypher

                    MATCH (a:Agent)-[:USES_CONFIG|REQUIRES]->(c:Config)
                    RETURN a.name as agent, c.name as config, c.value as value
                    ORDER BY a.name
                
```

