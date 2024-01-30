from pathlib import PosixPath

from rich.markdown import Markdown
from rich.table import Table


def dict2Table_Hor(item: list) -> Table:
    dt = Table()
    for elem in item[0].keys():
        dt.add_column(elem)
    for elem in item:
        dt.add_row(*[str(value) for key, value in elem.items()])
    return dt


def conv(txt: str):
    return ' '.join(txt.split('_')).title()


def dict2Table(item: dict, sep: str = '=') -> Table:
    dt = Table.grid()
    dt.add_column(style="bold", justify='right')
    dt.add_column()
    dt.add_column()
    for elem in item.keys():
        if isinstance(item[elem],list):
            if isinstance(item[elem][0], str):
                dt.add_row(conv(elem), f" {sep} ", Markdown(item[elem][0]))
                for subElem in item[elem][1:]:
                    dt.add_row("", f" {sep} ", Markdown(subElem))
            elif isinstance(item[elem][0], int) or isinstance(item[elem][0], bool):
                dt.add_row(conv(elem), f" {sep} ", str(item[elem][0]))
                for subElem in item[elem][1:]:
                    dt.add_row("", f" {sep} ", str(subElem))
            elif isinstance(item[elem][0],dict):
                dt.add_row(
                    elem,
                    " ",
                    dict2Table_Hor(item[elem]),
                )
                # for subElem in item[elem][1:]:
                #     dt.add_row('','' ,dict2Table(subElem))
        elif type(item[elem]) is int:
            dt.add_row(conv(elem), f" {sep} ",
                       f"[cyan]{str(item[elem])}[/cyan]")
        elif type(item[elem]) is bool:
            dt.add_row(conv(elem), f" {sep} ", f"[red]{str(item[elem])}[/red]")
        elif type(item[elem]) is dict:
            stb = dict2Table(item[elem])
            dt.add_row(conv(elem), f" {sep} ", stb)
        elif type(item[elem]) is PosixPath:
            dt.add_row(conv(elem), f" {sep} ", str(item[elem]))
        elif item[elem] is None:
            dt.add_row(conv(elem), f" {sep} ", "[blue]None[/blue]")
        else:
            dt.add_row(conv(elem), f" {sep} ", f"[green]{item[elem]}[/green]")
    return dt
