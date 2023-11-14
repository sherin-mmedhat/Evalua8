 // Import Employees
LOAD CSV WITH HEADERS FROM 'file:///employees.csv' AS row
CREATE (:Employee {
  id: toInteger(row.id),
  name: row.name,
  level: row.level,
  job_title: row.job_title,
  department: row.department
});

 // Import Squads
 LOAD CSV WITH HEADERS FROM 'file:///squads.csv' AS row
 CREATE (:Squad {id: toInteger(row.id),name: row.name});
 // Import Projects
 LOAD CSV WITH HEADERS FROM 'file:///projects.csv' AS row
 CREATE (:Project {id: toInteger(row.id),name: row.name});

 // Import departments
 LOAD CSV WITH HEADERS FROM 'file:///departments.csv' AS row
 CREATE (:Team {id: toInteger(row.id),name: row.name});

 // Import Relationships
 LOAD CSV WITH HEADERS FROM 'file:///relationships.csv' AS row
 MATCH (mentor:Employee {name: row.mentor})
 MATCH (mentee:Employee {name: row.mentee})
 CREATE (mentor)-[:MENTOR]->(mentee);

 // Connect Employees to Squads
 MATCH (e:Employee {name: 'Hadeer'}), (s:Squad {name: '.NET Squad'})
 CREATE (e)-[:MEMBER_OF]->(s);

 MATCH (e:Employee {name: 'Ziad'}), (s:Squad {name: '.NET Squad'})
 CREATE (e)-[:MEMBER_OF]->(s);

 MATCH (e:Employee {name: 'Sara'}), (s:Squad {name: '.NET Squad'})
 CREATE (e)-[:MEMBER_OF]->(s);

 MATCH (e:Employee {name: 'Huda'}), (s:Squad {name: '.NET Squad'})
 CREATE (e)-[:MEMBER_OF]->(s);

 MATCH (e:Employee {name: 'Menna'}), (s:Squad {name: '.NET Squad'})
 CREATE (e)-[:MEMBER_OF]->(s);

 MATCH (e:Employee {name: 'Yara'}), (s:Squad {name: '.NET Squad'})
 CREATE (e)-[:MEMBER_OF]->(s);

 // Connect Employees to Team
 MATCH (e:Employee {name: 'Hadeer'}), (t:Team {name: 'Engineering Team'})
 CREATE (e)-[:BELONGS_TO]->(t);

 MATCH (e:Employee {name: 'Ziad'}), (t:Team {name: 'Engineering Team'})
 CREATE (e)-[:BELONGS_TO]->(t);

 MATCH (e:Employee {name: 'Sara'}), (t:Team {name: 'Engineering Team'})
 CREATE (e)-[:BELONGS_TO]->(t);

 MATCH (e:Employee {name: 'Huda'}), (t:Team {name: 'Engineering Team'})
 CREATE (e)-[:BELONGS_TO]->(t);

 MATCH (e:Employee {name: 'Menna'}), (t:Team {name: 'Quality Team'})
 CREATE (e)-[:BELONGS_TO]->(t);

 MATCH (e:Employee {name: 'Yara'}), (t:Team {name: 'Product Team'})
 CREATE (e)-[:BELONGS_TO]->(t);

 MATCH (e:Employee {name: 'Esraa'}), (t:Team {name: 'Product Team'})
 CREATE (e)-[:BELONGS_TO]->(t);

 MATCH (e:Employee {name: 'Mai'}), (t:Team {name: 'Quality Team'})
 CREATE (e)-[:BELONGS_TO]->(t);

// Connect Squads to Projects
MATCH (s:Squad {name: '.NET Squad'}), (p:Project {name: 'BBO'})
CREATE (s)-[:OWNS]->(p);