import re
from langchain_community.document_loaders import PyPDFLoader
from langchain.docstore.document import Document

class PDFProcessor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.loader = PyPDFLoader(pdf_path)

    def load_and_split(self):
        pages = self.loader.load_and_split()
        full_text = ' '.join([page.page_content for page in pages])
        chunks = self.split_by_structure(full_text)
        return chunks

    def split_by_structure(self, text):
        chunks = []
        
        # Extraire le contenu avant l'Article 1 (Chunk 0)
        pre_article_1 = re.split(r'ARTICLE\s+PREMIER\.?', text)[0]
        chunks.append(Document(
            page_content=pre_article_1.strip(),
            metadata={
                "source": self.pdf_path,
                "title": "Préambule",
                "article_num": "0"
            }
        ))

        # Diviser le reste du texte en titres et articles
        main_text = text[len(pre_article_1):]
        title_pattern = r'Titre\s+[IVX]+\s*\n([^\n]+)'
        article_pattern = r'ARTICLE\s+(\w+(?:\-\d+)?)\.?([^A]+)(?=ARTICLE|$)'
        
        current_title = ""
        for title_match in re.finditer(title_pattern, main_text):
            title = title_match.group(0).strip()
            current_title = title
            title_end = title_match.end()
            next_title_match = re.search(title_pattern, main_text[title_end:])
            title_content = main_text[title_end:next_title_match.start() + title_end] if next_title_match else main_text[title_end:]
            
            for article_match in re.finditer(article_pattern, title_content):
                article_num = article_match.group(1)
                article_content = article_match.group(2).strip()
                
                chunk = Document(
                    page_content=f"ARTICLE {article_num}.\n{article_content}",
                    metadata={
                        "source": self.pdf_path,
                        "title": current_title,
                        "article_num": article_num
                    }
                )
                chunks.append(chunk)

        return chunks

    def process(self):
        chunks = self.load_and_split()
        print(f"Le document a été découpé en {len(chunks)} chunks.")
        
        # Afficher un aperçu des chunks pour vérification
        for i, chunk in enumerate(chunks[:4]):  # Afficher les 10 premiers chunks
            print(f"\nChunk {i}:")
            print(f"Titre: {chunk.metadata['title']}")
            print(f"Article: {chunk.metadata['article_num']}")
            print(chunk.page_content[:200] + "...")  # Afficher les 200 premiers caractères
        
        return chunks

# Exemple d'utilisation
if __name__ == "__main__":
    pdf_path = "constitution.pdf"
    processor = PDFProcessor(pdf_path)
    chunks = processor.process()