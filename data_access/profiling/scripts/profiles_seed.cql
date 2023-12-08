MATCH (n)
DETACH DELETE n;
     
// Import Employees
LOAD CSV WITH HEADERS FROM 'file:///employees.csv' AS row
CREATE (:Employee {
  id: toInteger(row.id),
  name: row.name,
  level: row.level,
  job_title: row.job_title,
  department: row.department,
  title_code: row.job_title_code
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
 MATCH (e:Employee {name: 'Sherin'}), (s:Squad {name: 'Evalu Squad'})
 CREATE (e)-[:MEMBER_OF]->(s);

 MATCH (e:Employee {name: 'Jolie'}), (s:Squad {name: 'Evalu Squad'})
 CREATE (e)-[:MEMBER_OF]->(s);

 MATCH (e:Employee {name: 'Sara'}), (s:Squad {name: 'Evalu Squad'})
 CREATE (e)-[:MEMBER_OF]->(s);

 MATCH (e:Employee {name: 'Magdy'}), (s:Squad {name: 'Evalu Squad'})
 CREATE (e)-[:MEMBER_OF]->(s);

 MATCH (e:Employee {name: 'Nouran'}), (s:Squad {name: 'Evalu Squad'})
 CREATE (e)-[:MEMBER_OF]->(s);

 // Connect Employees to Team
 MATCH (e:Employee {name: 'Sherin'}), (t:Team {name: 'Engineering Team'})
 CREATE (e)-[:BELONGS_TO]->(t);

 MATCH (e:Employee {name: 'Jolie'}), (t:Team {name: 'Engineering Team'})
 CREATE (e)-[:BELONGS_TO]->(t);

 MATCH (e:Employee {name: 'Sara'}), (t:Team {name: 'Engineering Team'})
 CREATE (e)-[:BELONGS_TO]->(t);

 MATCH (e:Employee {name: 'Magdy'}), (t:Team {name: 'Engineering Team'})
 CREATE (e)-[:BELONGS_TO]->(t);

 MATCH (e:Employee {name: 'Nouran'}), (t:Team {name: 'Product Team'})
 CREATE (e)-[:BELONGS_TO]->(t);

// Connect Squads to Projects
MATCH (s:Squad {name: 'Evalu Squad'}), (p:Project {name: 'Evalu'})
CREATE (s)-[:OWNS]->(p);

CREATE (f:Feedback {id: toInteger(1), feedback: "Feed back" ,evaluator_id : 2});
MATCH (e:Employee {id: 5}) , (f:Feedback{evaluator_id: 2})
CREATE (e)-[:HAVE]->(f);


CREATE (:Evaluation {id: toInteger(1), question: "Consistently delivering high-quality work.", kpi: "Productivity" ,is_sufficient : "false", score: 0, evaluator_id:toInteger(1),employee_id:toInteger(2)});

CREATE (:Evaluation {id: toInteger(2), question: "Managing multiple tasks and responsibilities effectively.", kpi: "Productivity" ,is_sufficient : "false", score: 0, evaluator_id:toInteger(1),employee_id:toInteger(2)});

CREATE (:Evaluation {id: toInteger(3), question: "Contributing to team discussions and decisions constructively.", kpi: "Teamwork" ,is_sufficient : "false", score: 0, evaluator_id:toInteger(1),employee_id:toInteger(2)});

CREATE (:Evaluation {id: toInteger(4), question: "Collaborating effectively with team members and demonstrating a positive attitude.", kpi: "Teamwork" ,is_sufficient : "false", score: 0, evaluator_id:toInteger(1),employee_id:toInteger(2)});


