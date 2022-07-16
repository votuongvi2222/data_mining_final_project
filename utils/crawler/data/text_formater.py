import re
def format_text(txt=None):
    """
        Formating the input text by remove all unnecessary characters 
        (such as duplicated spaces, new line, trailing spaces)

        If the argument `txt` isn't passed in, the default txt is used

        Parameters
        ----------
        text : str, optional
            The text needed to be formated (default is None)

        Raises
        ------
        NotImplementedError
            If no txt is set or passed in as a parameter.
    """
    if txt is None:
        raise NotImplementedError('The empty text is not allowed')
    return re.sub(' +', ' ', txt.replace('\n', ' ')).strip()
