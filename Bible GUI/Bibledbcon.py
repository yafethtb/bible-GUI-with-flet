import sqlite3

class Bible:
    """Bible class to connect user to the bible database"""
    def __init__(self, bibletype) -> None:
        self.bibletype = bibletype
        self.con = sqlite3.connect(r'assets\openbible.db', check_same_thread = False)
        self.cur = self.con.cursor()

    def book_list(self): #OK
        """Getting all books names in Bible"""
        if self.bibletype == 'kjv':
            self.cur.execute(
                '''
                SELECT book_name FROM bookName;
                '''
            )
        elif self.bibletype == 'TB':
            self.cur.execute(
                '''
                SELECT book_name FROM bookNameIndo;
                '''
            )        
        result = [book[0] for book in self.cur.fetchall()]
        return result

    def bookindex(self, bookname): #OK
        """Get the index of the book in database"""
        booklist = self.book_list()
        if bookname in booklist:
            return booklist.index(bookname) + 1
                    
    def chaptermax(self, bookname): #OK
        """Get the last chapter of a book"""
        index = self.bookindex(bookname)
        # if index  == "Book not found. Make sure the name is typed correctly.":
        #     return "Book not found."
        # else:
        if self.bibletype == 'kjv':
            self.cur.execute(
                '''
                SELECT MAX(chapter) FROM kjvbible WHERE book_id = ?;
                ''',
                (index, )
            )                
        elif self.bibletype == 'TB':
            self.cur.execute(
                '''
                SELECT MAX(chapter) FROM indoBible WHERE book_id = ?;
                ''',
                (index, )
            )
        max_chap = self.cur.fetchone()[0]
        return max_chap
    
    def versemax(self, bookname, chapter): #OK
        """Get the last verse number of a chapter of a book"""
        # ch = self.chaptermax(bookname)

        # if ch != 'Book not found.':
        book_index = self.bookindex(bookname)
        if self.bibletype == 'kjv':
            self.cur.execute(
                '''
                SELECT MAX(verse) FROM kjvbible WHERE book_id = ? AND chapter = ?;
                ''',
                (book_index, chapter)
            )                    
        elif self.bibletype == 'TB':
            self.cur.execute(
                '''
                SELECT MAX(verse) FROM indoBible WHERE book_id = ? AND chapter = ?;
                ''',
                (book_index, chapter)
            )
        max_verse  = self.cur.fetchone()[0]
        return max_verse
        # else:
        #     return 'We cannot find the chapter and book you search.'
    
    def verse_id(self, bookname, chapter, verse): #OK
        """Get ID of the verse"""
        bibletype = self.bibletype
        book_index = self.bookindex(bookname)
        
        if bibletype == 'kjv':
            self.cur.execute(
                '''
                SELECT id FROM kjvbible
                WHERE book_id = ? AND chapter = ? AND verse = ?
                ''',
                (book_index, chapter, verse)
            )                    
        elif bibletype == 'TB':
            self.cur.execute(
            '''
            SELECT id FROM indoBible WHERE book_id = ? AND chapter = ? AND verse = ?;
            ''',
            (book_index, chapter, verse)
            )
        return self.cur.fetchone()[0]
    
    def get_verse(self, bookname, chapter, verse): #OK
        """Get a verse text"""   
        verseid = self.verse_id(bookname, chapter, verse)
        bibletype = self.bibletype

        if isinstance(verseid, int):
            if bibletype == 'kjv':
                self.cur.execute(
                    '''
                    SELECT verse_text FROM kjvbible
                    WHERE id = ?;
                    ''',
                    (verseid,)
                )                
            elif bibletype == 'TB':
                self.cur.execute(
                    '''
                    SELECT verse_text FROM indoBible
                    WHERE id = ?;
                    ''',
                    (verseid,)
                )
                
        return self.cur.fetchone()[0]
    
    def get_more_verses(self, first, last): #OK
        """Get all text from first verse to last verse."""
        verseidfirst = self.verse_id(first[0], first[1], first[2])
        verseidlast = self.verse_id(last[0], last[1], last[2])
        bibletype = self.bibletype

        if isinstance(verseidfirst, int) and isinstance(verseidlast, int):
            if bibletype == 'kjv':
                self.cur.execute(
                    '''
                    SELECT verse_text
                    FROM kjvbible
                    WHERE id BETWEEN ? AND ?;
                    ''',
                    (verseidfirst, verseidlast)
                )
            elif bibletype == 'TB':
                self.cur.execute(
                    '''
                    SELECT verse_text
                    FROM indoBible
                    WHERE id BETWEEN ? AND ?;
                    ''',
                    (verseidfirst, verseidlast)
                )
            all_verses = [verse[0] for verse in self.cur.fetchall()]
            
            return all_verses
        else:
            return "Cannot load verses."           

    def closebook (self): #ok
        """Close the connection"""
        self.con.close()


# Test part

# bible = Bible('kjv')
# maxchap = bible.chaptermax('Genesis')
# print(maxchap)
# # print(type(maxchap))
# verse = bible.get_verse('Genesis', 2, 5)
# print(verse)
# bible.bibletype = 'TB'
# verseTB = bible.get_verse('Kejadian', 2, 5)
# print(verseTB)
# bible.closebook()