from typing import List
from models.schemas import DocumentChunk

def format_table_as_markdown(table: List[List[str]]) -> str:
    if not table or not table[0]:
        return ""
    
    # Filter out None values
    clean_table = [[str(cell).strip() if cell is not None else "" for cell in row] for row in table]
    
    header = clean_table[0]
    markdown = f"| {' | '.join(header)} |\n"
    markdown += f"| {' | '.join(['---'] * len(header))} |\n"
    
    for row in clean_table[1:]:
        markdown += f"| {' | '.join(row)} |\n"
        
    return markdown

def format_table_as_text(table: List[List[str]]) -> str:
    if not table:
        return ""
        
    clean_table = [[str(cell).strip() if cell is not None else "" for cell in row] for row in table]
    return "\n".join(["\t".join(row) for row in clean_table])

def extract_tables_from_page(page, page_number: int, document_name: str) -> List[DocumentChunk]:
    if not hasattr(page, "extract_tables"):
        return []
        
    chunks = []
    try:
        tables = page.extract_tables() or []
        for i, table in enumerate(tables):
            markdown_table = format_table_as_markdown(table)
            text_table = format_table_as_text(table)
            
            chunk = DocumentChunk(
                content=markdown_table,
                metadata={
                    "page_number": page_number,
                    "document_name": document_name,
                    "table_index": i,
                    "text_representation": text_table
                },
                chunk_type="table",
                page_number=page_number,
                document_name=document_name
            )
            chunks.append(chunk)
    except Exception:
        pass
        
    return chunks
