"""
Create a simple test EPUB file for testing the translator
"""
from ebooklib import epub

def create_test_epub(output_path: str):
    """Create a simple test EPUB file"""
    
    # Create book
    book = epub.EpubBook()
    
    # Set metadata
    book.set_identifier('test-epub-001')
    book.set_title('Test Book')
    book.set_language('en')
    book.add_author('Test Author')
    
    # Create chapter 1
    c1 = epub.EpubHtml(title='Chapter 1', file_name='chap_01.xhtml', lang='en')
    c1.content = '''
    <html>
    <head>
        <title>Chapter 1</title>
    </head>
    <body>
        <h1>Chapter 1: Introduction</h1>
        <p>This is the first paragraph of the test book.</p>
        <p>This is the second paragraph with more content.</p>
        <p>Here is a third paragraph to make it more interesting.</p>
    </body>
    </html>
    '''
    
    # Create chapter 2
    c2 = epub.EpubHtml(title='Chapter 2', file_name='chap_02.xhtml', lang='en')
    c2.content = '''
    <html>
    <head>
        <title>Chapter 2</title>
    </head>
    <body>
        <h1>Chapter 2: Main Content</h1>
        <p>This chapter contains the main content of the book.</p>
        <p>We have multiple paragraphs to translate.</p>
        <div>This is a div element with text.</div>
        <p>And this is the final paragraph.</p>
    </body>
    </html>
    '''
    
    # Add chapters to book
    book.add_item(c1)
    book.add_item(c2)
    
    # Define Table of Contents - use actual chapter items instead of Links
    book.toc = (c1, c2)
    
    # Add navigation files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    
    # Define spine
    book.spine = ['nav', c1, c2]
    
    # Write to file
    epub.write_epub(output_path, book, {})
    print(f"Test EPUB created: {output_path}")

if __name__ == '__main__':
    create_test_epub('test_input.epub')
