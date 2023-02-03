import flet as ft
from Bibledbcon import Bible

bible = Bible('kjv')

def main(page: ft.Page):
    """Connect GUI with bible database"""
    # Basic parameters for page
    page.title = 'Bilingual Bible App'
    page.window_height = 900
    page.window_width = 750
    page.window_maximizable = False        

    # Event Functions
    def showbook(e):
        """Show a book list of bible depends on what type of bible the user choose"""
        bible.bibletype = e.control.value
        book_list = bible.book_list()
        bookname.options = [
            ft.dropdown.Option(book) for book in book_list
        ]
        bottomnavbar.update()        

    def showchap(e):
        """Event for getting list of chapters of a book in bible"""
        book_name = bookname.value
        max_ch = bible.chaptermax(book_name) or 1 # This will ensure no threading issue raised because max_ch is None
        max_ch_list = [i for i in range(1, (max_ch + 1))]
        chapter.options = [
            ft.dropdown.Option(ch) for ch in max_ch_list
        ]       
        bottomnavbar.update()

    def showverse(e):
        """Events for get a list of verses from a chapter of a book"""
        book_name = bookname.value
        chap = chapter.value
        maxverse = bible.versemax(bookname = book_name, chapter = chap) or 1
        verse_list = [i for i in range(1, (maxverse + 1))]
        verse.options = [
            ft.dropdown.Option(ver) for ver in verse_list
        ]
        bottomnavbar.update()
    
    def viewverse(e):
        """Show the verse text"""
        verse_text = bible.get_verse(bookname.value, chapter.value, verse.value)
        body.controls = [
            ft.Text(
                f"{bookname.value} {chapter.value}: {verse.value}",
                style = 'labelLarge',
                size = int((page.height) * 0.05),
                weight = 'w900',
                text_align = 'center',
                selectable = True
            ),
            ft.Text(
                f'"{verse_text}"',
                style = 'bodyLarge',
                size = 18,
                weight = 'w900',
                text_align = 'center',
                selectable = True
            )
        ]
        body.update()

    # Widget wrappers
    # >> For Body
    body = ft.Column(
        controls = [
            ft.Text(
                "Pease choose 'kjv' in dropdown menu below for English\n or 'TB' for Bahasa Indonesia.",
                style = 'labelLarge',
                size = 24,
                weight = 'w900',
                text_align = 'center'
            )
        ],
        alignment = 'center'
    )
    # >> For Bottom Navbar
    bibletype = ft.Dropdown(
        label = "Type",
        label_style= ft.TextStyle(color = ft.colors.WHITE, weight = 'w300'),
        border_color= ft.colors.WHITE,
        color = ft.colors.BLACK,
        border_width = 3,
        options= [
            ft.dropdown.Option(text = "kjv"),
            ft.dropdown.Option(text = "TB")
        ],
        on_focus = showbook,
        width = 100
    )

    bookname = ft.Dropdown(
        label= 'Book Name',
        label_style= ft.TextStyle(color = ft.colors.WHITE, weight = 'w300'),
        border_color= ft.colors.WHITE,
        color = ft.colors.BLACK,
        border_width = 3,
        options = [],
        on_focus = showchap,
        width = 350
    )

    chapter = ft.Dropdown(
        label= 'ch', 
        label_style= ft.TextStyle(color = ft.colors.WHITE, weight = 'w300'),
        border_color= ft.colors.WHITE,
        color = ft.colors.BLACK,
        border_width = 3,
        options = [],
        on_focus = showverse,
        width = 70
    )

    verse = ft.Dropdown(
        label= 'ver',
        label_style= ft.TextStyle(color = ft.colors.WHITE, weight = 'w300'),
        border_color= ft.colors.WHITE,
        color = ft.colors.BLACK,
        border_width = 3,
        options = [],
        width = 70
    )

    submitbtn = ft.ElevatedButton(
        text = "SHOW ME THE VERSE",
        bgcolor = ft.colors.BLUE_GREY_200,
        color = ft.colors.WHITE,
        width = 500,
        height = 30,
        on_click = viewverse,    
    )

    bottomnavbar = ft.Column(
        controls = [
            ft.Text(
                "Enter The Verse",
                color = ft.colors.WHITE,
                weight = 'w900', 
                style = 'titleLarge',
                text_align = 'center'
            ),
            ft.Row(
                [
                    bibletype,
                    bookname,
                    chapter,
                    verse
                ],                    
                alignment = 'center',
                vertical_alignment = 'center'
            ),
            submitbtn
        ],
        alignment = 'center',
        horizontal_alignment = 'center'
    ) 

    # Base wrapper
    basegui = ft.Column(
        controls=[
            ft.Container(
                expand= 1, 
                content = ft.Column([
                    ft.Image(
                    src = f'assets/Bilingual bible.png',
                    fit = 'cover',
                    height = 150,
                    width = 750
                    )
                ],
                tight = True
                ),
                alignment= ft.alignment.center,                
                border_radius= 15
                ),
            ft.Container(
                expand= 3, 
                bgcolor= ft.colors.BLUE_GREY_100,
                content = body,
                alignment= ft.alignment.center,
                border_radius= 15,
                height = (900/3),
                padding = 30
                ),
            ft.Container(
                expand= 1, 
                bgcolor= ft.colors.BLUE_GREY_400,
                content = bottomnavbar, 
                alignment= ft.alignment.center,
                border_radius= 15
                ),            
        ],
        alignment = 'center',
        height= 800,
        width= 700
    )

    # Wrap them all
    page.add(basegui)


if __name__ == '__main__':
    ft.app(target = main, assets_dir = 'assets')
    bible.closebook()