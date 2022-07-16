from datetime import datetime, date

def str_to_date(dob_str=None, format='%B %d, %Y'):
    """
        Convert string type with given format to date type

        ie: March 14, 1879

        Parameters
        ----------
        dob_str : str
            The date in string type (default is None)
        format : str
            The format of given string in date type (default is `%B %d, %Y`)

        Returns
        -------
        datetime
            The converted date in given format
        
        Raises
        ------
        NotImplementedError
            If no dob_str is set or passed in as a parameter.
        ValueError
            If the dob_str is not in given format
    """
    if dob_str is None:
        raise NotImplementedError("Can't convert empty string to date type")
    try:
        converted_dob = datetime.strptime(dob_str, format).date()
        return converted_dob
    except ValueError:
        raise ValueError('The input dob not in the format!')

def compute_age(dob=None):
    """
        Compute age from given date

        If dob is not datetime type, convert it by str_to_date()

        Parameters
        ----------
        dob : datetime
            The given date of birth (default is None)
        
        Returns
        -------
        int
            The positive integer which is the computed age from 
            given date
        
        Raises
        ------
        NotImplementedError
            If no dob is set or passed in as a parameter
    """
    if dob is None:
        raise NotImplementedError("Can't compute age from None type value")
    if not isinstance(dob, date):
        dob = str_to_date(dob)
    return (date.today().year - dob.year - \
        ((date.today().month, date.today().day) < (dob.month, dob.day)))
