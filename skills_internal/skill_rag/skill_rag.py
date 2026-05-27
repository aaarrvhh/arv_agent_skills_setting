# ./.agent/skills_internal/skill_rag/skill_rag.py
# Standalone RAG Skill CLI supporting SQLite and ChromaDB

import os
import json
import argparse
import sqlite3
import docx
import chromadb
from sentence_transformers import SentenceTransformer

class DocumentParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

    def load_and_split(self, chunk_size: int = 800, chunk_overlap: int = 100):
        """Parse docx paragraphs and tables, maintaining hierarchy and chunking."""
        doc = docx.Document(self.file_path)
        elements = []
        
        # Traverse body elements to preserve order of paragraphs and tables
        current_headings = {}
        for element in doc.element.body:
            if element.tag.endswith('p'):
                p = docx.text.paragraph.Paragraph(element, doc)
                text = p.text.strip()
                if not text:
                    continue
                
                # Check style name for headings
                style_name = p.style.name if p.style else ""
                heading_level = self._get_heading_level(style_name)
                
                if heading_level is not None:
                    # Clear lower level headings
                    for level in list(current_headings.keys()):
                        if level >= heading_level:
                            del current_headings[level]
                    current_headings[heading_level] = text
                
                # Build heading path context
                heading_path = " > ".join([current_headings[lvl] for lvl in sorted(current_headings.keys())])
                
                elements.append({
                    'type': 'paragraph',
                    'text': text,
                    'heading_path': heading_path
                })
                
            elif element.tag.endswith('tbl'):
                t = docx.table.Table(element, doc)
                rows_data = []
                for row in t.rows:
                    row_data = []
                    for cell in row.cells:
                        cell_text = cell.text.strip().replace('\n', ' ')
                        # Avoid duplicating adjacent merged cells in the same row
                        if not row_data or row_data[-1] != cell_text:
                            row_data.append(cell_text)
                    rows_data.append(row_data)
                
                if rows_data:
                    # Construct markdown table structure
                    md_lines = []
                    for idx, row in enumerate(rows_data):
                        md_lines.append("| " + " | ".join(row) + " |")
                        if idx == 0:
                            md_lines.append("| " + " | ".join(["---"] * len(row)) + " |")
                    
                    heading_path = " > ".join([current_headings[lvl] for lvl in sorted(current_headings.keys())])
                    elements.append({
                        'type': 'table',
                        'text': "\n".join(md_lines),
                        'heading_path': heading_path
                    })

        # Chunking phase
        chunks = []
        current_chunk_text = ""
        current_heading_path = ""
        
        for el in elements:
            text_to_add = f"\n[Section: {el['heading_path']}]\n{el['text']}" if el['heading_path'] else el['text']
            
            if len(current_chunk_text) + len(text_to_add) > chunk_size and current_chunk_text:
                chunks.append({
                    'text': current_chunk_text.strip(),
                    'metadata': {
                        'source': os.path.basename(self.file_path),
                        'heading_path': current_heading_path
                    }
                })
                # Handle overlap
                current_chunk_text = current_chunk_text[-chunk_overlap:] + "\n" + text_to_add
                current_heading_path = el['heading_path']
            else:
                if current_chunk_text:
                    current_chunk_text += "\n" + text_to_add
                else:
                    current_chunk_text = text_to_add
                current_heading_path = el['heading_path']
                
        if current_chunk_text:
            chunks.append({
                'text': current_chunk_text.strip(),
                'metadata': {
                    'source': os.path.basename(self.file_path),
                    'heading_path': current_heading_path
                }
            })
            
        return chunks

    def _get_heading_level(self, style_name: str):
        """Parse heading level from style name (e.g. 'Heading 1' -> 1)."""
        if not style_name or not style_name.startswith('Heading'):
            return None
        parts = style_name.split()
        if len(parts) > 1 and parts[1].isdigit():
            return int(parts[1])
        return None


class SQLiteStore:
    def __init__(self, db_dir: str):
        self.db_dir = db_dir
        os.makedirs(db_dir, exist_ok=True)
        self.db_path = os.path.join(db_dir, "chunks_sqlite.db")
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS spec_chunks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source TEXT,
                    heading_path TEXT,
                    content TEXT
                )
            """)
            conn.commit()

    def clear(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM spec_chunks")
            conn.commit()

    def add_chunks(self, chunks):
        with sqlite3.connect(self.db_path) as conn:
            for chunk in chunks:
                conn.execute(
                    "INSERT INTO spec_chunks (source, heading_path, content) VALUES (?, ?, ?)",
                    (chunk['metadata']['source'], chunk['metadata']['heading_path'], chunk['text'])
                )
            conn.commit()

    def query(self, question: str, top_k: int = 5):
        """Perform simple keyword matching query over content."""
        words = [w.strip() for w in question.split() if w.strip()]
        if not words:
            return []
            
        # Build SQL condition matching any of the query keywords
        conditions = " OR ".join(["content LIKE ?" for _ in words])
        params = [f"%{word}%" for word in words]
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            query_sql = f"SELECT source, heading_path, content FROM spec_chunks WHERE {conditions} LIMIT ?"
            cursor.execute(query_sql, params + [top_k])
            rows = cursor.fetchall()
            
        results = []
        for row in rows:
            results.append({
                'source': row[0],
                'heading_path': row[1],
                'content': row[2]
            })
        return results


class ChromaStore:
    def __init__(self, db_dir: str):
        self.db_dir = db_dir
        os.makedirs(db_dir, exist_ok=True)
        # PersistentClient maintains database in the directory
        self.client = chromadb.PersistentClient(path=os.path.join(db_dir, "chroma"))
        # Load local lightweight embedding model
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.collection = self.client.get_or_create_collection(
            name="spec_chunks"
        )

    def clear(self):
        try:
            self.client.delete_collection("spec_chunks")
        except Exception:
            pass
        self.collection = self.client.get_or_create_collection(name="spec_chunks")

    def add_chunks(self, chunks):
        if not chunks:
            return
        
        documents = [c['text'] for c in chunks]
        embeddings = self.embedding_model.encode(documents).tolist()
        ids = [f"chunk_{i}" for i in range(len(chunks))]
        metadatas = [c['metadata'] for c in chunks]
        
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )

    def query(self, question: str, top_k: int = 5):
        query_embedding = self.embedding_model.encode([question]).tolist()
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k
        )
        
        formatted_results = []
        if results and 'documents' in results and results['documents']:
            docs = results['documents'][0]
            metas = results['metadatas'][0]
            for doc, meta in zip(docs, metas):
                formatted_results.append({
                    'source': meta.get('source', 'Unknown'),
                    'heading_path': meta.get('heading_path', ''),
                    'content': doc
                })
        return formatted_results


class ProjectRAGSkill:
    def __init__(self, config_file_path: str, db_type: str = "chroma"):
        if not os.path.exists(config_file_path):
            raise FileNotFoundError(f"Configuration file not found at: {config_file_path}")
            
        with open(config_file_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)
            
        self.project_name = self.config["project_name"]
        self.spec_folder = self.config["spec_folder"]
        self.spec_files = self.config["spec_files"]
        self.db_path = self.config["output_db_path"]
        self.db_type = db_type.lower()
        
        if self.db_type == "chroma":
            self.store = ChromaStore(self.db_path)
            self.sqlite_store = SQLiteStore(self.db_path)
        else:
            self.store = SQLiteStore(self.db_path)
            self.sqlite_store = None

    def build_database(self):
        """Parse all specifications and populate the chosen database backend."""
        all_chunks = []
        
        for file_name in self.spec_files:
            full_spec_path = os.path.normpath(os.path.join(self.spec_folder, file_name))
            if not os.path.exists(full_spec_path):
                print(f"Warning: Spec file missing: {full_spec_path}")
                continue
                
            print(f"[{self.project_name}] Ingesting: {file_name}...")
            parser = DocumentParser(file_path=full_spec_path)
            chunks = parser.load_and_split()
            all_chunks.extend(chunks)

        if not all_chunks:
            print(f"[{self.project_name}] Error: No chunks extracted to index.")
            return

        print(f"[{self.project_name}] Building {self.db_type.upper()} database at: {self.db_path}")
        self.store.clear()
        self.store.add_chunks(all_chunks)
        
        if self.db_type == "chroma" and self.sqlite_store:
            print(f"[{self.project_name}] Also building SQLITE database at: {self.db_path}")
            self.sqlite_store.clear()
            self.sqlite_store.add_chunks(all_chunks)
            
        print(f"[{self.project_name}] Database build completed successfully.\n")

    def query_database(self, question: str):
        """Query the database and format output for Agent ingestion."""
        results = self.store.query(question, top_k=5)
        
        output = [
            f"=== Retrieval Results for [{self.project_name}] using {self.db_type.upper()} ===",
            f"Question: {question}\n"
        ]
        
        for idx, res in enumerate(results):
            output.append(f"[{idx + 1}] Source: {res['source']}")
            if res['heading_path']:
                output.append(f"Section: {res['heading_path']}")
            output.append(f"Content:\n{res['content']}")
            output.append("-" * 40)
            
        return "\n".join(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Custom RAG Skill CLI supporting ChromaDB & SQLite")
    parser.add_argument("--config", type=str, required=True, help="Path to project config JSON")
    parser.add_argument("--db-type", type=str, default="chroma", choices=["chroma", "sqlite"], help="Backend database type ('chroma' will also build SQLite database)")
    parser.add_argument("--build", action="store_true", help="Build or refresh the vector database")
    parser.add_argument("--query", type=str, help="Ask a question against the project specs")

    args = parser.parse_args()
    
    rag_skill = ProjectRAGSkill(config_file_path=args.config, db_type=args.db_type)
    
    if args.build:
        rag_skill.build_database()
        
    if args.query:
        answer = rag_skill.query_database(args.query)
        print(answer)