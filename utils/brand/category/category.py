class Category:
    """
    A class used to represent an Category

    ...

    Attributes
    ----------
    title : str
        The name of the category
    link : str
        The link of category's page
    totalBrands : int
        Total shops/brands belongs to the category (default is None)
    Methods
    -------
    get_info()
        Print the information of the author
    """
    def __init__(self, title, link, totalBrands=None):
        """
        Parameters
        ----------
        title : str
            The name of the category
        link : str
            The link of category's page
        totalBrands : int
            Total shops/brands belongs to the category (default is None)
        """
        self.title = title
        self.link = link
        self.totalBrands = totalBrands

    def __str__(self):
        """
        Get the information of the category 
        (title, link)

        Returns
        -------
        str
            The short paragraph contains the information of the category
        """
        return f" - Title: {self.title} \
                \n - Link: {self.link} \
                \n - Total brands: {self.totalBrands or ''}"
        
    def get_info(self):
        """
            Print the information of the category
        """
        print(self.__str__())
