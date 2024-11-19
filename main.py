from neo4j import GraphDatabase


class GraphDatabaseManager:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_nodes_and_relationships(self):
        with self.driver.session() as session:
            # Cria alunos
            session.run("""
                CREATE (a:Aluno {matricula: '22122222', nome: 'João Silva', curso: 'C001', ano_ingresso: 2020, status: 'Ativo'})
            """)

            # Cria professores
            session.run("""
                CREATE (p:Professor {id_professor: '1', nome: 'Prof. Carlos', departamento: 'D001'})
            """)

            # Cria curso
            session.run("""
                CREATE (c:Curso {id_curso: 'C001', nome: 'Engenharia de Software'})
            """)

            # Cria deptos
            session.run("""
                CREATE (d:Departamento {id_departamento: 'D001', nome: 'Ciência da Computação'})
            """)

            # Cria disciplinas
            session.run("""
                CREATE (disc:Disciplina {id_disciplina: 'D001', nome: 'Algoritmos', creditos: 4})
            """)

            # Criar tcc
            session.run("""
                CREATE (t:TCC {id_tcc: 'TCC001', titulo: 'Aplicações de IA'})
            """)

            # Criar rlacionamentos
            session.run("""
                MATCH (a:Aluno {matricula: '22122222'}), (c:Curso {id_curso: 'C001'})
                CREATE (a)-[:ESTUDA_EM]->(c)
            """)

            session.run("""
                MATCH (c:Curso {id_curso: 'C001'}), (d:Departamento {id_departamento: 'D001'})
                CREATE (c)-[:PERTENCE_A]->(d)
            """)

            session.run("""
                MATCH (disc:Disciplina {id_disciplina: 'D001'}), (c:Curso {id_curso: 'C001'})
                CREATE (disc)-[:FAZ_PARTE {obrigatoriedade: 'obrigatória'}]->(c)
            """)

            session.run("""
                MATCH (a:Aluno {matricula: '22122222'}), (disc:Disciplina {id_disciplina: 'D001'})
                CREATE (a)-[:CURSOU {nota_final: 8.5, semestre: '2021.1', ano: 2021}]->(disc)
            """)

            session.run("""
                MATCH (p:Professor {id_professor: '1'}), (disc:Disciplina {id_disciplina: 'D001'})
                CREATE (p)-[:MINISTRA {semestre: '2021.1', ano: 2021}]->(disc)
            """)

            session.run("""
                MATCH (p:Professor {id_professor: '1'}), (d:Departamento {id_departamento: 'D001'})
                CREATE (p)-[:É_CHEFE_DE]->(d)
            """)

            session.run("""
                MATCH (a:Aluno {matricula: '22122222'}), (t:TCC {id_tcc: 'TCC001'})
                CREATE (a)-[:FAZ]->(t)
            """)

            session.run("""
                MATCH (p:Professor {id_professor: '1'}), (t:TCC {id_tcc: 'TCC001'})
                CREATE (p)-[:ORIENTA]->(t)
            """)

    def query_reports(self):
        with self.driver.session() as session:
            # Histórico escolar de um aluno
            print("\nHistórico Escolar de um Aluno:")
            result = session.run("""
                MATCH (a:Aluno {matricula: '22122222'})-[:CURSOU]->(d:Disciplina)
                RETURN d.id_disciplina, d.nome, a.curso, a.ano_ingresso
            """)
            for record in result:
                print(record)

            # Histórico de disciplinas ministradas por um professor
            print("\nHistórico de Disciplinas Ministradas por um Professor:")
            result = session.run("""
                MATCH (p:Professor {id_professor: '1'})-[:MINISTRA]->(d:Disciplina)
                RETURN d.id_disciplina, d.nome
            """)
            for record in result:
                print(record)

            # Alunos que se formaram
            print("\nAlunos Formados:")
            result = session.run("""
                MATCH (a:Aluno {status: 'formado'})
                RETURN a.nome, a.matricula
            """)
            for record in result:
                print(record)

            # Chefes de Departamento
            print("\nProfessores Chefes de Departamento:")
            result = session.run("""
                MATCH (p:Professor)-[:É_CHEFE_DE]->(d:Departamento)
                RETURN p.nome, d.nome
            """)
            for record in result:
                print(record)

            # Alunos e orientadores de TCC
            print("\nGrupos de TCC:")
            result = session.run("""
                MATCH (t:TCC)<-[:FAZ]-(a:Aluno), (t)<-[:ORIENTA]-(p:Professor)
                RETURN t.titulo, p.nome AS orientador, COLLECT(a.nome) AS alunos
            """)
            for record in result:
                print(record)


db = GraphDatabaseManager("neo4j://localhost", "neo4j", "adminadmin")

db.create_nodes_and_relationships()

db.query_reports()

db.close()
